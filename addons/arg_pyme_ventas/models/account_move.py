from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from .sale_order import INVOICE_TOKEN

_ACCOUNT_LIFECYCLE = object()


class AccountMove(models.Model):
    _name='account.move'
    _inherit=['account.move','arg.pyme.document.mixin']
    arg_header_snapshot=fields.Json(readonly=True,copy=False,groups='base.group_user')

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        move_type = values.get('move_type', self.env.context.get('default_move_type'))
        if ('invoice_date' in fields_list and move_type in ('out_invoice', 'out_refund')
                and not values.get('invoice_date') and 'default_invoice_date' not in self.env.context):
            values['invoice_date'] = fields.Date.context_today(self)
        return values

    def _arg_document_code(self):
        if self.move_type=='out_invoice':return 'FAC'
        if self.move_type=='out_refund':return 'NCV'
        return super()._arg_document_code()

    @api.model_create_multi
    def create(self,vals_list):
        internal=self.env.context.get('_arg_invoice_token') is INVOICE_TOKEN
        for values in vals_list:
            move_type=values.get('move_type',self.env.context.get('default_move_type','entry'))
            if move_type in ('out_invoice','out_refund'):values.setdefault('state','draft')
            if move_type in ('out_invoice','out_refund') and values.get('state','draft')!='draft':
                raise AccessError(_('La factura nace en borrador. Use Publicar con los permisos correspondientes.'))
            if ('arg_header_snapshot' in values or self.env.context.get('default_arg_header_snapshot')) and not internal:
                raise AccessError(_('La evidencia comercial se recibe desde el pedido autorizado.'))
            if values.get('move_type')=='out_refund' and values.get('reversed_entry_id'):
                original=self.browse(values['reversed_entry_id']);original.check_access('read')
                if original.arg_header_snapshot:values['arg_header_snapshot']=original.arg_header_snapshot
        return super().create(vals_list)

    def write(self,values):
        if 'move_type' in values and any(move.move_type!=values['move_type'] for move in self):
            raise UserError(_('Cada tipo conserva su identidad. Cree una factura o nota nueva mediante el circuito correspondiente.'))
        if 'state' in values and self.filtered(lambda m:m.move_type in ('out_invoice','out_refund')) and self.env.context.get('_arg_account_lifecycle') is not _ACCOUNT_LIFECYCLE:
            raise AccessError(_('Use las acciones de publicar, cancelar o volver a borrador del documento.'))
        if 'arg_header_snapshot' in values:raise AccessError(_('La evidencia comercial no se modifica manualmente.'))
        for move in self.filtered('arg_header_snapshot'):
            if any(name in values and values[name]!=move[name].id for name in ('company_id','partner_id','currency_id')):
                raise UserError(_('El documento conserva compañía, tercero y moneda de origen. Use una corrección vinculada.'))
        return super().write(values)

    def _post(self,*args,**kwargs):
        documents=self.filtered(lambda move:move.move_type in ('out_invoice','out_refund'))
        if documents and not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Publicar una factura o nota requiere responsable ARG y los permisos contables nativos.'))
        for move in documents:
            move.company_id.currency_id._arg_require_conversion(move.currency_id,move.company_id,move._get_invoice_currency_rate_date())
            orders=move.invoice_line_ids.sale_line_ids.order_id.filtered('arg_quotation_id')
            for order in orders:
                order._arg_lock_roots()
                if order.arg_commitment_released:raise UserError(_('El pedido fue liberado. No se puede volver a facturar su compromiso anterior.'))
                order.arg_quotation_id._check_frozen_taxes()
            if not move.arg_header_snapshot:
                partner=move.partner_id
                payload={'partner':{'id':partner.id,'name':partner.name or '', 'vat':partner.vat or '', 'address':partner.contact_address or ''},
                         'company':{'id':move.company_id.id,'name':move.company_id.name},'notes':''}
                super(AccountMove,move).write({'arg_header_snapshot':payload})
        posted=super(AccountMove,self.with_context(_arg_account_lifecycle=_ACCOUNT_LIFECYCLE))._post(*args,**kwargs)
        return posted.with_context(_arg_account_lifecycle=None)

    def button_cancel(self):
        if self.filtered(lambda m:m.move_type in ('out_invoice','out_refund')) and not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Cancelar requiere responsable ARG y permisos contables nativos.'))
        return super(AccountMove,self.with_context(_arg_account_lifecycle=_ACCOUNT_LIFECYCLE)).button_cancel()

    def button_draft(self):
        if self.filtered(lambda m:m.move_type in ('out_invoice','out_refund')) and not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Revertir requiere responsable ARG y permisos contables nativos.'))
        return super(AccountMove,self.with_context(_arg_account_lifecycle=_ACCOUNT_LIFECYCLE)).button_draft()

    @api.depends('write_date','state','amount_total','amount_residual','currency_id','move_type')
    def _compute_arg_completion_axes(self):super()._compute_arg_completion_axes()

    def _arg_get_completion_axes(self):
        if self.move_type not in ('out_invoice','out_refund') or self.state!='posted':return super()._arg_get_completion_axes()
        label='Cancelación de deuda' if self.move_type=='out_invoice' else 'Aplicación de crédito'
        return [self._arg_axis(label,[{'label':self.arg_number or self.name,'unit':self.currency_id.name,
            'rounding':self.currency_id.rounding,'target':abs(self.amount_total),
            'done':max(0,abs(self.amount_total)-abs(self.amount_residual))}])]

    def _arg_document_relations(self):
        result=super()._arg_document_relations()
        if self.move_type not in ('out_invoice','out_refund'):return result
        result.append({'label':'Pedidos origen','records':self.invoice_line_ids.sale_line_ids.order_id})
        if self.reversed_entry_id:result.append({'label':'Comprobante corregido','records':self.reversed_entry_id})
        if self.reversal_move_ids:result.append({'label':'Correcciones vinculadas','records':self.reversal_move_ids})
        return result

    def _arg_document_line_relations(self):
        result=super()._arg_document_line_relations()
        if self.move_type not in ('out_invoice','out_refund'):return result
        for invoice_line in self.invoice_line_ids:
            for order_line in invoice_line.sale_line_ids:
                result.append({'source_document':order_line.order_id,'source_line':order_line,
                    'target_document':self,'target_line':invoice_line,
                    'quantity':invoice_line.quantity if len(invoice_line.sale_line_ids)==1 else None,
                    'unit':invoice_line.product_uom_id.display_name})
        return result

    def action_arg_treasury(self):
        self._arg_check_document_access()
        if 'arg.pyme.treasury.document' not in self.env:
            raise UserError(_('Los cobros y pagos se incorporan con Administración ARG. La deuda cancelada puede incluir notas de crédito y ajustes.'))
        return self.env['arg.pyme.treasury.document']._arg_action_new_from_debt(self)

    def _arg_report_payload(self):
        if self.move_type not in ('out_invoice','out_refund'):return super()._arg_report_payload()
        snapshot=self.arg_header_snapshot or {}
        partner=snapshot.get('partner') or {'name':self.partner_id.name or '', 'address':self.partner_id.contact_address or ''}
        title='Factura de venta ARG' if self.move_type=='out_invoice' else 'Nota de crédito venta ARG'
        return {'title':title,'company':snapshot.get('company',{}).get('name') or self.company_id.name,
            'date':str(self.invoice_date or self.date),'state_label':dict(self._fields['state']._description_selection(self.env)).get(self.state),
            'partner_name':partner['name'],'partner_address':partner['address'],'external_reference':self.ref or self.arg_reference,
            'currency':self.currency_id.name,'lines':[{'description':l.name,'quantity':l.quantity,'unit':l.product_uom_id.display_name,
                 'unit_price':l.price_unit,'total':l.price_total} for l in self.invoice_line_ids if l.display_type=='product'],
            'totals':[{'label':'Neto','amount':self.amount_untaxed},{'label':'Impuestos','amount':self.amount_tax},
                      {'label':'Total','amount':self.amount_total},{'label':'Pendiente de aplicación','amount':self.amount_residual}],
            'notes':snapshot.get('notes') or ''}
