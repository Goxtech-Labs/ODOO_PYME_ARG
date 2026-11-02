from odoo.addons.arg_pyme_base.tools.quantity import quantity_rounding
import uuid
from markupsafe import escape
from odoo import api, fields, models, Command, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.float_utils import float_compare
from .quotation import GENERATION_TOKEN, digest

_LIFECYCLE = object()
INVOICE_TOKEN = object()


class QuotationGeneration(models.Model):
    _inherit='arg.pyme.quotation'

    def _generate_order(self,key,values):
        self._lock_root()
        selected=self._selection(values);payload_hash=self._operation_hash(key,selected)
        orders=self.env['sale.order'].with_company(self.company_id)
        prior=orders.search([('arg_quotation_id','=',self.id),('arg_generation_key','=',key)],limit=1)
        if prior:
            if prior.arg_generation_hash!=payload_hash:raise ValidationError(_('La clave corresponde a otro pedido.'))
            return prior
        self._check_current()
        if not self.accepted_snapshot or self.state not in ('partially_confirmed','confirmed'):
            raise UserError(_('Confirme primero las cantidades del presupuesto.'))
        self._check_frozen_taxes()
        committed=self._committed_map()
        for line,qty in selected:
            available=line.accepted_target_total-committed.get(line.commercial_line_key,0)
            if float_compare(qty,available,precision_rounding=quantity_rounding(self.env))>0:
                raise UserError(_('La cantidad supera el confirmado disponible para generar.'))
        snapshot=self.accepted_snapshot
        for field,keyname in [('partner_id','partner'),('invoice_partner_id','invoice_partner'),('delivery_partner_id','delivery_partner')]:
            if self._party_snapshot(self[field] or self.partner_id)!=snapshot[keyname]:
                raise UserError(_('Cambió la identidad o domicilio del cliente. Prepare una revisión antes de generar el pedido.'))
        pricelist=self.pricelist_id or self.env['product.pricelist'].search([
            ('company_id','in',[False,self.company_id.id]),('currency_id','=',self.currency_id.id)],limit=1)
        if not pricelist:raise UserError(_('Configure una lista compatible con la moneda antes de generar el pedido.'))
        commands=[];bases=[]
        for line,qty in selected:
            frozen=snapshot['lines'][str(line.id)]
            commands.append(Command.create({'product_id':frozen['product_id'],'name':frozen['description'],
                'product_uom_id':frozen['unit_id'],'product_uom_qty':qty,'price_unit':frozen['price_unit'],
                'discount':frozen['discount'],'tax_ids':[Command.set(frozen['tax_ids'])],
                'arg_quotation_line_id':line.id,'arg_commercial_line_key':line.commercial_line_key}))
            bases.append(line._base_line(qty))
        tax=self.env['account.tax']
        tax._add_tax_details_in_base_lines(bases,self.company_id);tax._round_base_lines_tax_details(bases,self.company_id)
        expected=tax._get_tax_totals_summary(bases,self.currency_id,self.company_id)
        # No action_confirm: a separate native PED draft is the result of this explicit action.
        order=orders.with_context(_arg_generation_token=GENERATION_TOKEN).create({
            'company_id':self.company_id.id,'partner_id':self.partner_id.id,
            'partner_invoice_id':(self.invoice_partner_id or self.partner_id).id,
            'partner_shipping_id':(self.delivery_partner_id or self.partner_id).id,
            'pricelist_id':pricelist.id,'currency_id':self.currency_id.id,
            'payment_term_id':self.payment_term_id.id,'fiscal_position_id':self.fiscal_position_id.id,
            'document_tax_mode':snapshot['document_tax_mode'],'note':str(escape(snapshot['notes'])).replace('\n','<br/>'),
            'arg_quotation_id':self.id,'arg_generation_key':key,'arg_generation_hash':payload_hash,
            'arg_quote_snapshot':snapshot,'order_line':commands})
        if order.state not in ('draft','sent') or order.currency_id!=self.currency_id:
            raise UserError(_('La configuración nativa modificó el estado o la moneda. Revise la composición antes de continuar.'))
        if len(order.order_line.filtered(lambda l:not l.display_type))!=len(selected):
            raise UserError(_('La configuración agregó líneas no previstas. Revise el presupuesto y su adaptación.'))
        for actual,desired in [(order.amount_untaxed,expected['base_amount_currency']),
                               (order.amount_tax,expected['tax_amount_currency']),(order.amount_total,expected['total_amount_currency'])]:
            if self.currency_id.compare_amounts(actual,desired):
                raise UserError(_('Los importes nativos difieren del acuerdo aceptado. No se generó el pedido; prepare una revisión compatible.'))
        return order.with_context(_arg_generation_token=None)


class SaleOrder(models.Model):
    _name='sale.order'
    _inherit=['sale.order','arg.pyme.document.mixin']

    arg_quotation_id=fields.Many2one('arg.pyme.quotation',readonly=True,copy=False,index=True,check_company=True,groups='base.group_user')
    arg_generation_key=fields.Char(readonly=True,copy=False,index=True,groups='base.group_user')
    arg_generation_hash=fields.Char(readonly=True,copy=False,groups='base.group_user')
    arg_quote_snapshot=fields.Json(readonly=True,copy=False,groups='base.group_user')
    arg_commitment_released=fields.Boolean(readonly=True,copy=False,default=False,groups='base.group_user')
    _arg_generation_unique=models.Constraint('UNIQUE(company_id,arg_quotation_id,arg_generation_key)','El pedido de esta operación ya existe.')

    def _arg_document_code(self):return 'PED'

    @api.model_create_multi
    def create(self,vals_list):
        generated=self.env.context.get('_arg_generation_token') is GENERATION_TOKEN
        for values in vals_list:
            values.setdefault('state','draft')
            if not generated and any(self.env.context.get('default_'+key) for key in ('arg_quotation_id','arg_generation_key','arg_generation_hash','arg_quote_snapshot','arg_commitment_released')):
                raise AccessError(_('Los vínculos de origen se reciben únicamente desde la generación autorizada.'))
            if values.get('state','draft') not in ('draft','sent'):
                raise AccessError(_('Un pedido se crea en borrador; confirme mediante su acción.'))
            if any(k.startswith('arg_') and k not in {'arg_reference'} and v for k,v in values.items()) and not generated:
                raise AccessError(_('Los vínculos y condiciones ARG sólo se crean desde un presupuesto autorizado.'))
            if not generated and not self.env.user.has_group('arg_pyme_base.group_manager'):
                raise AccessError(_('Genere el pedido desde un presupuesto confirmado. Los pedidos directos requieren responsable ARG.'))
        return super().create(vals_list)

    def write(self,values):
        protected={'arg_quotation_id','arg_generation_key','arg_generation_hash','arg_quote_snapshot','arg_commitment_released'}
        if protected & values.keys():raise AccessError(_('La relación y el compromiso se administran desde sus acciones.'))
        generated=self.filtered('arg_quotation_id')
        if generated and {'partner_id','partner_invoice_id','partner_shipping_id','company_id','currency_id',
                          'pricelist_id','payment_term_id','fiscal_position_id','document_tax_mode','note'} & values.keys():
            raise UserError(_('El pedido conserva las condiciones aceptadas. Corrija mediante cancelación, liberación y revisión.'))
        if 'state' in values and self.env.context.get('_arg_lifecycle') is not _LIFECYCLE:
            raise AccessError(_('Use Confirmar, Cancelar o Volver a borrador; no modifique el estado directamente.'))
        return super().write(values)

    def _arg_lock_roots(self):
        quotes=self.filtered('arg_quotation_id').arg_quotation_id.sorted(lambda q:q.commercial_root_id.id)
        for quote in quotes:quote._lock_root()

    def _arg_require_manager(self):
        if not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Confirmar o revertir requiere responsable ARG.'))

    def action_confirm(self):
        self._arg_require_manager();self._arg_lock_roots()
        if any(self.mapped('arg_commitment_released')):raise UserError(_('Un compromiso liberado no puede reactivarse. Genere otro pedido desde la revisión vigente.'))
        return super(SaleOrder,self.with_context(_arg_lifecycle=_LIFECYCLE)).action_confirm()

    def action_cancel(self):
        self._arg_require_manager();self._arg_lock_roots()
        return super(SaleOrder,self.with_context(_arg_lifecycle=_LIFECYCLE)).action_cancel()

    def _action_cancel(self):
        self._arg_require_manager();self._arg_lock_roots()
        return super(SaleOrder,self.with_context(_arg_lifecycle=_LIFECYCLE))._action_cancel()

    def action_draft(self):
        self._arg_require_manager();self._arg_lock_roots()
        if any(self.mapped('arg_commitment_released')):raise UserError(_('Conserve el pedido liberado como cancelado.'))
        return super(SaleOrder,self.with_context(_arg_lifecycle=_LIFECYCLE)).action_draft()

    def _prepare_invoice(self):
        values=super()._prepare_invoice()
        if self.arg_quote_snapshot:
            values['arg_header_snapshot']=self.arg_quote_snapshot
        return values

    def _create_invoices(self,*args,**kwargs):
        linked=self.filtered('arg_quotation_id')
        if linked and len(self)>1:
            raise UserError(_('En el circuito básico facture un pedido por vez para conservar su acuerdo y trazabilidad.'))
        for order in linked:order.arg_quotation_id._check_frozen_taxes()
        invoices=super(SaleOrder,self.with_context(_arg_invoice_token=INVOICE_TOKEN))._create_invoices(*args,**kwargs)
        return invoices.with_context(_arg_invoice_token=None)

    def action_arg_invoice(self):
        self._arg_check_document_access()
        action=self.env['ir.actions.actions']._for_xml_id('sale.action_view_sale_advance_payment_inv')
        action['context']={'active_model':self._name,'active_ids':self.ids,'active_id':self.id,'default_advance_payment_method':'delivered'}
        return action

    def action_arg_release(self):
        self._arg_check_document_access();self.check_access('write')
        wizard=self.env['arg.pyme.quotation.release.wizard'].create({'order_id':self.id})
        return {'type':'ir.actions.act_window','res_model':wizard._name,'res_id':wizard.id,'view_mode':'form','target':'new'}

    def _arg_release_commitment(self,key,reason):
        self._arg_require_manager()
        self._arg_check_document_access();self.check_access('write')
        if not self.arg_quotation_id:raise UserError(_('Este pedido no viene de un presupuesto ARG.'))
        quote=self.arg_quotation_id;quote._lock_root()
        if not isinstance(key,str) or not 16<=len(key)<=80 or not isinstance(reason,str) or not reason.strip():
            raise ValidationError(_('Indique una clave válida y el motivo de liberación.'))
        events=self.env['arg.pyme.quotation.release']
        prior=events.search([('order_id','=',self.id),('operation_key','=',key)],limit=1)
        payload_hash=digest({'order_id':self.id,'reason':reason.strip()})
        if prior:
            if prior.payload_hash!=payload_hash:raise ValidationError(_('La clave corresponde a otra liberación.'))
            return prior
        if self.arg_commitment_released:raise UserError(_('Este pedido ya fue liberado mediante otra operación.'))
        if self.state!='cancel':raise UserError(_('Cancele primero el pedido y resuelva sus derivados.'))
        for line in self.order_line.filtered(lambda l:not l.display_type):
            if float_compare(abs(line.qty_delivered),0,precision_rounding=quantity_rounding(self.env)) or float_compare(abs(line.qty_invoiced),0,precision_rounding=quantity_rounding(self.env)):
                raise UserError(_('Quedan entregas o facturación activas. Corrija los derivados antes de liberar.'))
        if self.invoice_ids.filtered(lambda move:move.state=='draft'):
            raise UserError(_('Resuelva las facturas borrador antes de liberar.'))
        changes=[{'line_id':line.arg_quotation_line_id.id,'key':line.arg_commercial_line_key,'quantity':line.product_uom_qty}
                 for line in self.order_line if line.arg_quotation_line_id]
        super(SaleOrder,self).write({'arg_commitment_released':True})
        return events.sudo().create({'company_id':self.company_id.id,'order_id':self.id,'quotation_id':quote.id,
            'operation_key':key,'payload_hash':payload_hash,'user_id':self.env.uid,'reason':reason.strip(),'changes':changes})

    def _arg_document_relations(self):
        result=[]
        if self.arg_quotation_id:result.append({'label':'Presupuesto origen','records':self.arg_quotation_id})
        result.append({'label':'Facturas y notas','records':self.invoice_ids})
        return result

    def _arg_document_line_relations(self):
        result=[]
        for line in self.order_line:
            if line.arg_quotation_line_id:
                result.append({'source_document':self.arg_quotation_id,'source_line':line.arg_quotation_line_id,
                    'target_document':self,'target_line':line,'quantity':line.product_uom_qty,'unit':line.product_uom_id.display_name})
            for invoice_line in line.invoice_lines:
                result.append({'source_document':self,'source_line':line,'target_document':invoice_line.move_id,
                    'target_line':invoice_line,'quantity':invoice_line.quantity if len(invoice_line.sale_line_ids)==1 else None,'unit':invoice_line.product_uom_id.display_name})
        return result

    @api.depends('write_date','state','order_line.qty_invoiced_posted','order_line.product_uom_qty',
                 'invoice_ids.amount_residual','invoice_ids.amount_total','invoice_ids.state','arg_commitment_released')
    def _compute_arg_completion_axes(self):super()._compute_arg_completion_axes()

    def _arg_get_completion_axes(self):
        rows=[]
        for line in self.order_line.filtered(lambda l:not l.display_type and not l.is_downpayment):
            rows.append({'label':line.name,'unit':line.product_uom_id.display_name,'rounding':quantity_rounding(self.env),
                'target':line.product_uom_qty,'done':line.qty_invoiced_posted,
                'closed':max(0,line.product_uom_qty-line.qty_invoiced_posted) if self.state=='cancel' else 0})
        invoices=self.invoice_ids.filtered(lambda move:move.move_type=='out_invoice' and move.state=='posted')
        scope_reason=self._arg_invoice_scope_reason(invoices, 'sale_line_ids')
        money=[]
        for invoice in invoices if not scope_reason else self.env['account.move']:
            money.append({'label':invoice.arg_number or invoice.name,'unit':invoice.currency_id.name,'rounding':invoice.currency_id.rounding,
                          'target':abs(invoice.amount_total),'done':max(0,abs(invoice.amount_total)-abs(invoice.amount_residual))})
        axes=[self._arg_axis('Facturación del pedido',rows),
              self._arg_unknown_axis('Cancelación de deuda facturada',scope_reason) if scope_reason else self._arg_axis('Cancelación de deuda facturada',money)]
        cash_axis=self._arg_cash_application_axis()
        if cash_axis:axes.append(cash_axis)
        return axes

    def _arg_cash_application_axis(self):
        adapter = getattr(self.env['account.move'], '_arg_money_axis', None)
        if not adapter:
            return False
        invoices=self.invoice_ids.filtered(lambda move:move.move_type=='out_invoice' and move.state=='posted')
        reason=self._arg_invoice_scope_reason(invoices, 'sale_line_ids')
        if reason:
            return self._arg_unknown_axis('Dinero cobrado sobre lo facturado',reason)
        return invoices._arg_money_axis('Dinero cobrado sobre lo facturado')

    def _arg_report_payload(self):
        snapshot=self.arg_quote_snapshot or {}
        partner=snapshot.get('partner') or {'name':self.partner_id.name,'address':self.partner_id.contact_address}
        return {'title':'Pedido de cliente ARG','company':snapshot.get('company',{}).get('name') or self.company_id.name,'date':str(self.date_order),'state_label':dict(self._fields['state']._description_selection(self.env)).get(self.state),
            'partner_name':partner['name'],'partner_address':partner['address'],'external_reference':self.client_order_ref or self.arg_reference,
            'currency':self.currency_id.name,'lines':[{'description':l.name,'quantity':l.product_uom_qty,'unit':l.product_uom_id.display_name,
                'unit_price':l.price_unit,'total':l.price_total} for l in self.order_line if not l.display_type],
            'totals':[{'label':'Neto','amount':self.amount_untaxed},{'label':'Impuestos','amount':self.amount_tax},{'label':'Total','amount':self.amount_total}],
            'notes':snapshot.get('notes') or ''}


class SaleOrderLine(models.Model):
    _inherit='sale.order.line'
    arg_quotation_line_id=fields.Many2one('arg.pyme.quotation.line',readonly=True,copy=False,index=True,check_company=True,groups='base.group_user')
    arg_commercial_line_key=fields.Char(readonly=True,copy=False,index=True,groups='base.group_user')
    arg_commercial_root_id=fields.Many2one(related='arg_quotation_line_id.quotation_id.commercial_root_id',store=True,index=True,groups='base.group_user')

    @api.model_create_multi
    def create(self,vals_list):
        internal=self.env.context.get('_arg_generation_token') is GENERATION_TOKEN
        for values in vals_list:
            order=self.env['sale.order'].browse(values.get('order_id') or self.env.context.get('default_order_id'))
            if not internal and (order.arg_quotation_id or any(k.startswith('arg_') for k in values)
                    or any(k.startswith('default_arg_') and value for k,value in self.env.context.items())):
                raise AccessError(_('Las líneas derivadas se generan desde el presupuesto; no se agregan manualmente.'))
        return super().create(vals_list)

    def write(self,values):
        if any(k.startswith('arg_') for k in values):raise AccessError(_('La trazabilidad de línea es inmutable.'))
        terms={'order_id','product_id','name','product_uom_id','product_uom_qty','price_unit','discount','tax_ids',
               'product_no_variant_attribute_value_ids','product_custom_attribute_value_ids'}
        if terms & values.keys() and any(self.order_id.mapped('arg_quotation_id')):
            raise UserError(_('Conserve las condiciones del pedido derivado; cambie el saldo mediante una revisión.'))
        return super().write(values)

    def unlink(self):
        if any(self.order_id.mapped('arg_quotation_id')):raise UserError(_('Conserve las líneas vinculadas; cancele y libere el pedido si corresponde.'))
        return super().unlink()


class CommitmentRelease(models.Model):
    _name='arg.pyme.quotation.release'
    _description='Liberación de compromiso ARG'
    _order='id desc'
    company_id=fields.Many2one('res.company',required=True,index=True)
    quotation_id=fields.Many2one('arg.pyme.quotation',required=True,index=True,ondelete='restrict')
    order_id=fields.Many2one('sale.order',required=True,index=True,ondelete='restrict')
    operation_key=fields.Char(required=True,index=True)
    payload_hash=fields.Char(required=True)
    user_id=fields.Many2one('res.users',required=True)
    reason=fields.Text(required=True)
    changes=fields.Json(required=True)
    _release_unique=models.Constraint('UNIQUE(company_id,order_id,operation_key)','La liberación ya existe.')
    @api.model_create_multi
    def create(self,vals_list):
        if not self.env.su:raise AccessError(_('La liberación se registra desde el pedido autorizado.'))
        return super().create(vals_list)
    def write(self,values):raise UserError(_('La liberación registrada es inmutable.'))
    def unlink(self):raise UserError(_('La liberación se conserva.'))
