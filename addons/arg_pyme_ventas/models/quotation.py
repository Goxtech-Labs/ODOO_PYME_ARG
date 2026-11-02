from odoo.addons.arg_pyme_base.tools.quantity import quantity_rounding
import hashlib
import json
import math
import uuid
from odoo import api, fields, models, Command, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.float_utils import float_compare

_INTERNAL = object()
GENERATION_TOKEN = object()


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,default=str,separators=(',',':')).encode()).hexdigest()


class Quotation(models.Model):
    _name = 'arg.pyme.quotation'
    _inherit = ['arg.pyme.document.mixin']
    _description = 'Presupuesto ARG'
    _rec_name = 'arg_number'
    _order = 'id desc'
    _check_company_auto = True

    company_id = fields.Many2one('res.company',required=True,default=lambda s:s.env.company,index=True)
    partner_id = fields.Many2one('res.partner',string='Cliente',check_company=True)
    invoice_partner_id = fields.Many2one('res.partner',string='Facturar a',check_company=True)
    delivery_partner_id = fields.Many2one('res.partner',string='Entregar a',check_company=True)
    date = fields.Date(string='Fecha',required=True,default=fields.Date.context_today)
    valid_until = fields.Date(string='Válido hasta')
    currency_id = fields.Many2one('res.currency',required=True,default=lambda s:s.env.company.currency_id,string='Moneda')
    pricelist_id = fields.Many2one('product.pricelist',check_company=True,string='Lista')
    payment_term_id = fields.Many2one('account.payment.term',check_company=True,string='Condición de pago')
    fiscal_position_id = fields.Many2one('account.fiscal.position',check_company=True,string='Posición fiscal')
    document_tax_mode = fields.Selection([('tax_excluded','Precio sin impuestos'),('tax_included','Precio con impuestos')],
        required=True,default=lambda s:s.env.company.account_price_include or 'tax_excluded',string='Precios')
    state = fields.Selection([('draft','Borrador'),('issued','Emitido'),('partially_confirmed','Confirmado parcialmente'),
        ('confirmed','Confirmado'),('rejected','Rechazado'),('expired','Vencido'),('canceled','Cancelado')],
        default='draft',required=True,readonly=True,index=True,copy=False,string='Estado')
    is_expired = fields.Boolean(compute='_compute_is_expired')
    line_ids = fields.One2many('arg.pyme.quotation.line','quotation_id',string='Detalle',copy=True)
    notes = fields.Text(string='Observaciones y condiciones')
    allow_zero_price = fields.Boolean(string='Aceptar precios cero expresamente')
    defaults_snapshot = fields.Json(default=lambda s:{'currency_id':s.env.company.currency_id.id},copy=False,groups='base.group_user')
    accepted_snapshot = fields.Json(readonly=True,copy=False,groups='base.group_user')
    confirmed_at = fields.Datetime(readonly=True,copy=False)
    confirmed_by = fields.Many2one('res.users',readonly=True,copy=False)
    commercial_root_id = fields.Many2one('arg.pyme.quotation',readonly=True,copy=False,index=True,ondelete='restrict',check_company=True)
    previous_revision_id = fields.Many2one('arg.pyme.quotation',readonly=True,copy=False,ondelete='restrict',check_company=True)
    current_revision_id = fields.Many2one('arg.pyme.quotation',readonly=True,copy=False,ondelete='restrict',check_company=True)
    revision_number = fields.Integer(default=1,readonly=True,copy=False)
    carried_commitments = fields.Json(readonly=True,copy=False,groups='base.group_user')
    order_ids = fields.One2many('sale.order','arg_quotation_id',readonly=True)
    acceptance_ids = fields.One2many('arg.pyme.quotation.acceptance','quotation_id',readonly=True)
    amount_untaxed = fields.Monetary(compute='_compute_amounts',string='Neto del saldo')
    amount_tax = fields.Monetary(compute='_compute_amounts',string='Impuestos del saldo')
    amount_total = fields.Monetary(compute='_compute_amounts',string='Total del saldo')
    _revision_unique = models.Constraint('UNIQUE(commercial_root_id,revision_number)','La revisión ya existe.')

    def _arg_document_code(self): return 'PRE'

    def _authorize(self):
        self._arg_check_document_access()
        self.check_access('write')
        if not (self.env.user.has_group('arg_pyme_base.group_ventas') or self.env.user.has_group('arg_pyme_base.group_admin')):
            raise AccessError(_('Se requiere operación Ventas ARG.'))

    def _require_manager(self):
        if not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Confirmar o revertir requiere responsable ARG.'))

    def _mutate(self, values):
        return super(Quotation,self).write(values)

    @api.model_create_multi
    def create(self, vals_list):
        prepared=[]
        protected={'state','accepted_snapshot','confirmed_at','confirmed_by','commercial_root_id',
                   'previous_revision_id','current_revision_id','revision_number','carried_commitments'}
        for raw in vals_list:
            values=dict(raw)
            if self.env.context.get('_arg_internal') is not _INTERNAL:
                defaults=self.default_get(list(protected))
                defaults.update(values)
                values=defaults
            if self.env.context.get('_arg_internal') is not _INTERNAL and any(values.get(k) and not (k=='state' and values[k]=='draft') and not (k=='revision_number' and values[k]==1) for k in protected):
                raise AccessError(_('La revisión y la confirmación se administran mediante sus acciones.'))
            company=self.env['res.company'].browse(values.get('company_id') or self.env.company.id)
            if company not in self.env.companies:raise AccessError(_('Compañía no habilitada.'))
            if values.get('partner_id'):
                partner=self.env['res.partner'].browse(values['partner_id']).with_company(company)
                known=partner._arg_document_defaults('sale')
                for name in ['currency_id','pricelist_id','payment_term_id','invoice_partner_id','delivery_partner_id']:
                    values.setdefault(name,known.get(name))
                position=self.env['account.fiscal.position'].with_company(company)._get_fiscal_position(partner,self.env['res.partner'].browse(known['delivery_partner_id']))
                values.setdefault('fiscal_position_id',position.id)
                values.setdefault('notes',known.get('conditions_note'))
                values.setdefault('defaults_snapshot',known)
            prepared.append(values)
        records=super().create(prepared)
        for record in records:
            if not record.commercial_root_id:
                record._mutate({'commercial_root_id':record.id,'current_revision_id':record.id})
        return records

    def write(self, values):
        protected={'state','accepted_snapshot','confirmed_at','confirmed_by','commercial_root_id',
                   'previous_revision_id','current_revision_id','revision_number','carried_commitments'}
        if protected & values.keys():raise AccessError(_('Use las acciones documentales para modificar estado o revisión.'))
        conditions={'company_id','partner_id','invoice_partner_id','delivery_partner_id','date','valid_until',
                    'currency_id','pricelist_id','payment_term_id','fiscal_position_id','document_tax_mode',
                    'line_ids','notes','allow_zero_price','arg_reference'}
        if conditions & values.keys():
            for record in self.sorted(lambda q:q.commercial_root_id.id or q.id):
                if record.commercial_root_id:record._lock_root()
            for record in self:
                if record.carried_commitments and any(name in values and values[name]!=record[name].id for name in ('currency_id','partner_id')):
                    raise UserError(_('Los compromisos previos conservan cliente y moneda. Abra otro presupuesto para otro negocio.'))
        if conditions & values.keys() and any(q.state not in ('draft','issued') or q.accepted_snapshot for q in self):
            raise UserError(_('Las condiciones aceptadas se conservan. Cree una revisión nueva.'))
        return super().write(values)

    @api.onchange('partner_id')
    def _onchange_partner(self):
        if not self.partner_id:return
        known=self.partner_id.with_company(self.company_id)._arg_document_defaults('sale')
        known['fiscal_position_id']=self.env['account.fiscal.position'].with_company(self.company_id)._get_fiscal_position(self.partner_id,self.env['res.partner'].browse(known['delivery_partner_id'])).id
        prior=self.defaults_snapshot or {}
        for name in ['currency_id','pricelist_id','payment_term_id','invoice_partner_id','delivery_partner_id','fiscal_position_id']:
            current=self[name].id
            if not current or current==prior.get(name):self[name]=known.get(name)
        if not self.notes or self.notes==prior.get('conditions_note'):self.notes=known.get('conditions_note')
        self.defaults_snapshot=known

    @api.depends('valid_until','state')
    def _compute_is_expired(self):
        today=fields.Date.context_today(self)
        for quote in self:quote.is_expired=bool(quote.valid_until and quote.valid_until<today)

    @api.depends('line_ids.target_quantity_total','line_ids.carried_committed_quantity','line_ids.price_unit',
                 'line_ids.discount','line_ids.tax_ids','currency_id','company_id','document_tax_mode','accepted_snapshot')
    def _compute_amounts(self):
        tax=self.env['account.tax']
        for quote in self:
            frozen=quote.accepted_snapshot or {}
            if frozen:
                values=frozen['totals']
            else:
                bases=[line._base_line() for line in quote.line_ids if line.product_id]
                tax._add_tax_details_in_base_lines(bases,quote.company_id)
                tax._round_base_lines_tax_details(bases,quote.company_id)
                summary=tax._get_tax_totals_summary(bases,quote.currency_id,quote.company_id)
                values={'untaxed':summary['base_amount_currency'],'tax':summary['tax_amount_currency'],'total':summary['total_amount_currency']}
            quote.amount_untaxed=values['untaxed'];quote.amount_tax=values['tax'];quote.amount_total=values['total']

    def _lock_root(self):
        self._authorize()
        root=self.commercial_root_id
        root.check_access('write')
        root.flush_recordset(['write_date','write_uid'])
        self.env.cr.execute('UPDATE arg_pyme_quotation SET write_date=clock_timestamp(),write_uid=%s WHERE id=%s',[self.env.uid,root.id])
        root.invalidate_recordset(['write_date','write_uid'])
        return root

    def _check_current(self, check_carries=True):
        if self.commercial_root_id.current_revision_id!=self:
            raise UserError(_('Hay una revisión posterior. Continúe desde la revisión vigente.'))
        if not check_carries:return
        for carry in self.carried_commitments or []:
            if carry['currency_id']!=self.currency_id.id or carry['partner_id']!=self.partner_id.id:
                raise UserError(_('El compromiso previo conserva cliente y moneda.'))
            line=self.env['sale.order.line'].browse(carry['line_id']).exists()
            if not line or line.order_id.arg_commitment_released or float_compare(line.product_uom_qty,carry['quantity'],precision_rounding=quantity_rounding(self.env))!=0:
                raise UserError(_('Cambió un compromiso arrastrado. Cree una revisión para acordar el saldo actualizado.'))

    def _committed_lines(self):
        return self.env['sale.order.line'].search([('arg_commercial_root_id','=',self.commercial_root_id.id),
                                                  ('order_id.arg_quotation_id.commercial_root_id','=',self.commercial_root_id.id),
                                                  ('order_id.arg_commitment_released','=',False)])

    def _committed_map(self):
        result={}
        for line in self._committed_lines():
            key=line.arg_commercial_line_key
            result[key]=result.get(key,0)+line.product_uom_qty
        return result

    def _validate_terms(self):
        self.ensure_one()
        if not self.partner_id or not self.currency_id or not self.line_ids:
            raise UserError(_('Complete cliente, moneda y al menos una línea.'))
        if self.pricelist_id and self.pricelist_id.currency_id!=self.currency_id:
            raise UserError(_('La moneda no coincide con la lista seleccionada.'))
        term=self.payment_term_id
        if term.early_discount and term.early_pay_discount_computation=='mixed':
            raise UserError(_('El descuento fiscal mixto necesita un adaptador específico antes de aceptar este presupuesto.'))
        if self.valid_until and self.valid_until<fields.Date.context_today(self):
            raise UserError(_('El presupuesto venció. Emita una nueva revisión.'))
        for line in self.line_ids:
            if not line.product_id or line.product_id.type not in ('consu','service') or not line.uom_id or line.uom_id!=line.product_id.uom_id:
                raise UserError(_('Complete producto y unidad base compatible en cada línea.'))
            if not all(math.isfinite(value) for value in (line.target_quantity_total,line.price_unit,line.discount)):
                raise UserError(_('Revise cantidades, precios y descuentos finitos.'))
            if float_compare(line.target_quantity_total,line.carried_committed_quantity,precision_rounding=quantity_rounding(self.env))<0:
                raise UserError(_('La cantidad objetivo no puede ser menor al compromiso previo.'))
            if float_compare(line.target_quantity_total,0,precision_rounding=quantity_rounding(self.env))<=0 or not math.isclose(line.target_quantity_total/quantity_rounding(self.env),round(line.target_quantity_total/quantity_rounding(self.env)),rel_tol=0,abs_tol=1e-7) or line.price_unit<0:
                raise UserError(_('Revise cantidades y precios no negativos.'))
            if not 0<=line.discount<=100:raise UserError(_('El descuento debe estar entre cero y cien.'))
            if line.price_unit==0 and not self.allow_zero_price:
                raise UserError(_('Acepte expresamente los precios cero o corrija la línea.'))
            if any(t.company_id!=self.company_id for t in line.tax_ids):raise UserError(_('Los impuestos deben corresponder a la compañía.'))

    def action_update_prices(self):
        self._lock_root();self._check_current()
        if self.accepted_snapshot or self.state not in ('draft','issued'):
            raise UserError(_('Los precios aceptados se conservan. Cree una revisión nueva.'))
        for line in self.line_ids.filtered('product_id'):
            known=line._product_defaults(self,line.product_id,max(1,line.target_quantity_total-line.carried_committed_quantity))
            line.write({'price_unit':known['price_unit'],'tax_ids':known['tax_ids']})
        return True

    def action_issue(self):
        self._lock_root();self._check_current();self._validate_terms()
        if self.state!='draft':raise UserError(_('Sólo un borrador puede emitirse.'))
        self._mutate({'state':'issued'})
        return True

    def action_reject(self):
        self._lock_root();self._check_current()
        if self.accepted_snapshot:raise UserError(_('Conserve la aceptación y revise el saldo mediante una nueva revisión.'))
        self._mutate({'state':'rejected'});return True

    def action_cancel(self):
        self._require_manager()
        self._lock_root();self._check_current()
        if self.accepted_snapshot or self._committed_lines():raise UserError(_('Hay aceptación o compromisos. Conserve el historial y use revisión/reversión.'))
        self._mutate({'state':'canceled'});return True

    def _selection(self, selected):
        if not isinstance(selected,list) or len(selected)>500:raise ValidationError(_('Selección no válida.'))
        result=[];seen=set()
        for raw in selected:
            if not isinstance(raw,dict) or type(raw.get('line_id')) is not int or type(raw.get('quantity')) not in (int,float):raise ValidationError(_('Línea o cantidad no válida.'))
            if raw['line_id'] in seen:raise ValidationError(_('Una línea sólo puede aparecer una vez.'))
            seen.add(raw['line_id']);quantity=float(raw['quantity'])
            line=self.line_ids.filtered(lambda l:l.id==raw['line_id'])
            if not line or not math.isfinite(quantity) or quantity<0:raise ValidationError(_('Línea o cantidad no válida.'))
            if quantity:
                rounding=quantity_rounding(self.env) or 0.01
                if float_compare(quantity,0,precision_rounding=rounding)<=0 or not math.isclose(quantity/rounding,round(quantity/rounding),rel_tol=0,abs_tol=1e-7):
                    raise ValidationError(_('La cantidad debe respetar el paso de la unidad.'))
                result.append((line,quantity))
        if not result:raise UserError(_('Seleccione al menos una cantidad positiva.'))
        return sorted(result,key=lambda item:item[0].id)

    def _operation_hash(self,key,selected):
        if not isinstance(key,str) or not 16<=len(key)<=80:raise ValidationError(_('Clave de operación no válida.'))
        return digest([{'line_id':line.id,'quantity':qty} for line,qty in selected])

    def _party_snapshot(self,partner):
        partner=partner.with_context(lang='es_AR')
        return {'id':partner.id,'name':partner.name or '', 'vat':partner.vat or '',
                'address':partner.contact_address or '', 'country':partner.country_id.code or ''} if partner else {}

    def _conditions_definition(self):
        def read(record,names):
            return record.with_context(lang='en_US').read([n for n in names if n in record._fields])
        term=self.payment_term_id
        position=self.fiscal_position_id
        raw={'quantity_precision':self.env['decimal.precision'].precision_get('Product Unit'),'payment_term':read(term,['name','write_date','early_discount','discount_percentage','early_pay_discount_computation','discount_days']),
             'payment_term_lines':read(term.line_ids.sorted('id'),['value','value_amount','nb_days','delay_type','days_next_month','months','write_date']),
             'fiscal_position':read(position,['name','write_date','country_id','state_ids','vat_required']),
             'fiscal_taxes':read(position.tax_ids.sorted('id'),['tax_src_id','tax_dest_id','write_date']),
             'fiscal_accounts':read(position.account_ids.sorted('id'),['account_src_id','account_dest_id','write_date']),
             'currency':read(self.currency_id,['name','rounding','decimal_places','write_date'])}
        return json.loads(json.dumps(raw,default=str))

    def _make_snapshot(self):
        self.ensure_one()
        company=self.company_id
        rate_evidence=company.currency_id._arg_require_conversion(self.currency_id,company,self.date)
        return {'rate_evidence':rate_evidence,'company':{'id':company.id,'name':company.name},'partner':self._party_snapshot(self.partner_id),'invoice_partner':self._party_snapshot(self.invoice_partner_id or self.partner_id),
                'delivery_partner':self._party_snapshot(self.delivery_partner_id or self.partner_id),
                'payment_term':{'id':self.payment_term_id.id,'name':self.payment_term_id.display_name or ''},
                'fiscal_position':{'id':self.fiscal_position_id.id,'name':self.fiscal_position_id.display_name or ''},
                'pricelist':{'id':self.pricelist_id.id,'name':self.pricelist_id.display_name or ''},
                'currency':{'id':self.currency_id.id,'name':self.currency_id.name,'rounding':self.currency_id.rounding},
                'rate':self.env['res.currency']._get_conversion_rate(company.currency_id,self.currency_id,company,self.date),
                'date':str(self.date),'document_tax_mode':self.document_tax_mode,'notes':self.notes or '',
                'lines':{str(line.id):line._snapshot() for line in self.line_ids},
                'totals':{'untaxed':self.amount_untaxed,'tax':self.amount_tax,'total':self.amount_total},
                'carried_commitments':self.carried_commitments or [],'conditions_definition':self._conditions_definition()}

    def _accept(self,key,values):
        self._require_manager()
        self._lock_root()
        selected=self._selection(values);payload_hash=self._operation_hash(key,selected)
        events=self.env['arg.pyme.quotation.acceptance']
        prior=events.search([('quotation_id','=',self.id),('operation_key','=',key)],limit=1)
        if prior:
            if prior.payload_hash!=payload_hash:raise ValidationError(_('La clave corresponde a otra aceptación.'))
            return prior
        self._check_current();self._validate_terms()
        if self.state not in ('issued','partially_confirmed'):raise UserError(_('Emita primero el presupuesto.'))
        self._check_frozen_taxes()
        for line,qty in selected:
            if float_compare(qty,line.target_quantity_total-line.accepted_target_total,precision_rounding=quantity_rounding(self.env))>0:
                raise UserError(_('La cantidad supera el pendiente de aceptación.'))
        if not self.accepted_snapshot:
            self._mutate({'accepted_snapshot':self._make_snapshot(),'confirmed_at':fields.Datetime.now(),'confirmed_by':self.env.uid})
        changes=[]
        for line,qty in selected:
            target=line.accepted_target_total+qty
            changes.append({'line_id':line.id,'quantity':qty,'accepted_target_total':target})
            line._mutate({'accepted_target_total':target})
        complete=all(float_compare(l.accepted_target_total,l.target_quantity_total,precision_rounding=quantity_rounding(self.env))>=0 for l in self.line_ids)
        self._mutate({'state':'confirmed' if complete else 'partially_confirmed'})
        return events.sudo().create({'company_id':self.company_id.id,'quotation_id':self.id,'operation_key':key,
            'payload_hash':payload_hash,'user_id':self.env.uid,'changes':changes})

    def _check_frozen_taxes(self):
        if not self.accepted_snapshot:return
        if self.accepted_snapshot['conditions_definition']!=self._conditions_definition():
            raise UserError(_('Cambió la configuración de pago, posición fiscal o moneda. Prepare una revisión compatible.'))
        for line in self.line_ids:
            snapshot=self.accepted_snapshot['lines'][str(line.id)]
            unit=json.loads(json.dumps(line.uom_id.with_context(lang='en_US').read([n for n in ['name','factor','relative_factor','relative_uom_id','write_date'] if n in line.uom_id._fields]),default=str))
            if snapshot['tax_signature']!=line._tax_signature() or snapshot['unit_definition']!=unit:
                raise UserError(_('Cambió la definición de un impuesto. Conserve el acuerdo y prepare una revisión compatible.'))

    def action_accept_quantities(self): return self._open_operation('accept')
    def action_generate_order(self): return self._open_operation('generate')

    def _open_operation(self,mode):
        self._authorize()
        wizard=self.env['arg.pyme.quotation.operation'].create({'quotation_id':self.id,'mode':mode})
        return {'type':'ir.actions.act_window','res_model':wizard._name,'res_id':wizard.id,'view_mode':'form','target':'new'}

    def action_new_revision(self):
        root=self._lock_root();self._check_current(check_carries=False)
        if self.state=='draft':raise UserError(_('Termine o descarte el borrador vigente antes de otra revisión.'))
        committed=self._committed_map();carries=[]
        for native in self._committed_lines():
            carries.append({'line_id':native.id,'order_id':native.order_id.id,'number':native.order_id.arg_number,
                'key':native.arg_commercial_line_key,'quantity':native.product_uom_qty,'unit':native.product_uom_id.display_name,
                'currency_id':native.currency_id.id,'partner_id':native.order_id.partner_id.id,
                'description':native.name,'price_unit':native.price_unit,'subtotal':native.price_subtotal,
                'total':native.price_total,'tax':native.price_total-native.price_subtotal})
        commands=[]
        for line in self.line_ids:
            carried=committed.get(line.commercial_line_key,0)
            commands.append(Command.create({'commercial_line_key':line.commercial_line_key,'sequence':line.sequence,
                'product_id':line.product_id.id,'description':line.description,'uom_id':line.uom_id.id,
                'target_quantity_total':max(line.target_quantity_total,carried),'carried_committed_quantity':carried,
                'accepted_target_total':carried,'price_unit':line.price_unit,'discount':line.discount,'tax_ids':[Command.set(line.tax_ids.ids)]}))
        values={name:self[name].id for name in ['company_id','partner_id','invoice_partner_id','delivery_partner_id','currency_id','pricelist_id','payment_term_id','fiscal_position_id']}
        values.update({'date':fields.Date.context_today(self),'document_tax_mode':self.document_tax_mode,'notes':self.notes,
            'commercial_root_id':root.id,'previous_revision_id':self.id,'revision_number':self.revision_number+1,
            'carried_commitments':carries,'allow_zero_price':self.allow_zero_price,'line_ids':commands})
        revision=self.with_context(_arg_internal=_INTERNAL).create(values)
        root._mutate({'current_revision_id':revision.id})
        return {'type':'ir.actions.act_window','res_model':self._name,'res_id':revision.id,'view_mode':'form'}

    @api.depends('write_date','line_ids.accepted_target_total','line_ids.target_quantity_total','order_ids.state','order_ids.arg_commitment_released','order_ids.order_line.product_uom_qty')
    def _compute_arg_completion_axes(self):
        super()._compute_arg_completion_axes()

    def _arg_get_completion_axes(self):
        committed=self._committed_map() if self.id and self.commercial_root_id else {}
        acceptance=[];generation=[]
        for line in self.line_ids:
            rounding=quantity_rounding(self.env) or 0.01
            base={'label':line.description or line.product_id.display_name,'unit':line.uom_id.display_name,'rounding':rounding}
            acceptance.append({**base,'target':line.target_quantity_total,'done':line.accepted_target_total,
                'closed':max(0,line.target_quantity_total-line.accepted_target_total) if self.state in ('canceled','rejected','expired') else 0})
            generation.append({**base,'target':line.accepted_target_total,'done':committed.get(line.commercial_line_key,0)})
        return [self._arg_axis('Confirmación',acceptance),self._arg_axis('Generación de pedidos',generation)]

    def _arg_document_relations(self):
        relations=[{'label':'Pedidos de esta revisión','records':self.order_ids}]
        if self.previous_revision_id:relations.append({'label':'Revisión anterior','records':self.previous_revision_id})
        if self.commercial_root_id.current_revision_id!=self:relations.append({'label':'Revisión vigente','records':self.commercial_root_id.current_revision_id})
        return relations

    def _arg_document_line_relations(self):
        return [{'source_document':self,'source_line':line.arg_quotation_line_id,'target_document':line.order_id,
                 'target_line':line,'quantity':line.product_uom_qty,'unit':line.product_uom_id.display_name}
                for line in self.order_ids.order_line if line.arg_quotation_line_id]

    def _arg_report_payload(self):
        snapshot=self.accepted_snapshot or self._make_snapshot()
        rows=[]
        for carry in snapshot['carried_commitments']:
            rows.append({'description':'Compromiso previo '+carry['number']+' · '+carry['description'],
                'quantity':carry['quantity'],'unit':carry['unit'],'unit_price':carry['price_unit'],'total':carry['total']})
        for line in self.line_ids:
            item=snapshot['lines'][str(line.id)]
            rows.append({'description':item['description'],'quantity':item['proposal_quantity'],'unit':item['unit'],
                         'unit_price':item['price_unit'],'total':item['total']})
        totals=snapshot['totals'];prior=sum(c['total'] for c in snapshot['carried_commitments'])
        return {'title':'Presupuesto ARG','company':snapshot['company']['name'],'date':snapshot['date'],'state_label':dict(self._fields['state']._description_selection(self.env)).get(self.state),
            'partner_name':snapshot['partner'].get('name',''),'partner_address':snapshot['partner'].get('address',''),
            'external_reference':self.arg_reference,'currency':snapshot['currency']['name'],'lines':rows,'notes':snapshot['notes'],
            'totals':[{'label':'Compromisos previos','amount':prior},{'label':'Neto del saldo','amount':totals['untaxed']},
                      {'label':'Impuestos del saldo','amount':totals['tax']},{'label':'Total del saldo','amount':totals['total']},
                      {'label':'Total comprometido y propuesto','amount':prior+totals['total']}]}


class QuotationLine(models.Model):
    _name='arg.pyme.quotation.line'
    _description='Línea de presupuesto ARG'
    _rec_name='description'
    _order='sequence,id'
    _check_company_auto=True

    quotation_id=fields.Many2one('arg.pyme.quotation',required=True,ondelete='cascade',index=True,check_company=True)
    company_id=fields.Many2one(related='quotation_id.company_id',store=True)
    currency_id=fields.Many2one(related='quotation_id.currency_id')
    sequence=fields.Integer(default=10)
    commercial_line_key=fields.Char(required=True,default=lambda s:uuid.uuid4().hex,readonly=True,copy=False,index=True)
    product_id=fields.Many2one('product.product',string='Producto / servicio',check_company=True)
    description=fields.Char(string='Descripción')
    uom_id=fields.Many2one('uom.uom',string='Unidad')
    target_quantity_total=fields.Float(string='Cantidad objetivo total',default=1,digits='Product Unit')
    carried_committed_quantity=fields.Float(string='Compromiso previo',readonly=True,default=0,digits='Product Unit')
    accepted_target_total=fields.Float(string='Confirmado acumulado',readonly=True,default=0,digits='Product Unit')
    ordered_quantity_net=fields.Float(compute='_compute_committed',string='Comprometido neto',digits='Product Unit')
    price_unit=fields.Float(string='Precio unitario',digits='Product Price')
    discount=fields.Float(string='Descuento %',default=0)
    tax_ids=fields.Many2many('account.tax',string='Impuestos',check_company=True)
    amount_untaxed=fields.Monetary(compute='_compute_line_amounts',string='Neto del saldo')
    amount_tax=fields.Monetary(compute='_compute_line_amounts',string='Impuestos del saldo')
    amount_total=fields.Monetary(compute='_compute_line_amounts',string='Total del saldo')
    _line_key_unique=models.Constraint('UNIQUE(quotation_id,commercial_line_key)','La línea comercial ya existe en esta revisión.')

    def _mutate(self,values):return super(QuotationLine,self).write(values)

    @api.model_create_multi
    def create(self,vals_list):
        for values in vals_list:
            if self.env.context.get('_arg_internal') is not _INTERNAL and any(values.get(k) or self.env.context.get('default_'+k) for k in ('commercial_line_key','carried_committed_quantity','accepted_target_total')):
                raise AccessError(_('La identidad y aceptación de línea se administran automáticamente.'))
            quote=self.env['arg.pyme.quotation'].browse(values['quotation_id'])
            quote.check_access('write')
            if quote.commercial_root_id:quote._lock_root()
            if quote.state not in ('draft','issued') or quote.accepted_snapshot:raise UserError(_('No se agregan líneas a un presupuesto aceptado.'))
            if values.get('product_id'):
                known=self._product_defaults(quote,self.env['product.product'].browse(values['product_id']),max(1,values.get('target_quantity_total',1)-values.get('carried_committed_quantity',0)))
                for name,value in known.items():values.setdefault(name,value)
        return super().create(vals_list)

    def write(self,values):
        if {'quotation_id','commercial_line_key','carried_committed_quantity','accepted_target_total'} & values.keys():raise AccessError(_('No se cambia la identidad ni aceptación de línea.'))
        for quote in self.quotation_id.sorted(lambda q:q.commercial_root_id.id or q.id):
            if quote.commercial_root_id:quote._lock_root()
        for line in self:
            line.quotation_id.check_access('write')
            if line.quotation_id.state not in ('draft','issued') or line.quotation_id.accepted_snapshot:raise UserError(_('Las líneas aceptadas se conservan. Cree una revisión.'))
            if line.carried_committed_quantity and {'product_id','uom_id'} & values.keys():raise UserError(_('Una línea con compromiso previo conserva producto y unidad.'))
        return super().write(values)

    def unlink(self):
        for quote in self.quotation_id.sorted(lambda q:q.commercial_root_id.id or q.id):
            if quote.commercial_root_id:quote._lock_root()
        if any(l.quotation_id.state not in ('draft','issued') or l.quotation_id.accepted_snapshot or l.carried_committed_quantity for l in self):raise UserError(_('Conserve las líneas emitidas o comprometidas.'))
        return super().unlink()

    @api.model
    def _product_defaults(self,quote,product,quantity):
        quote=quote.with_company(quote.company_id)
        product=product.with_company(quote.company_id)
        product.check_access('read')
        product_taxes=product.taxes_id._filter_taxes_by_company(quote.company_id)
        taxes=quote.fiscal_position_id.map_tax(product_taxes) if quote.fiscal_position_id else product_taxes
        if quote.pricelist_id:
            when=fields.Datetime.to_datetime(quote.date)
            price,rule_id=quote.pricelist_id._get_product_price_rule(product,quantity,date=when,uom=product.uom_id)
            self.env['arg.pyme.pricelist.matrix'].with_company(quote.company_id)._require_rule_rates(
                product,quote.pricelist_id,self.env['product.pricelist.item'].browse(rule_id),when,quantity,set())
        else:
            product.currency_id._arg_require_conversion(quote.currency_id,quote.company_id,quote.date)
            price=product.currency_id._convert(product.list_price,quote.currency_id,quote.company_id,quote.date,round=False)
        price=product._get_tax_included_unit_price_from_price(price,product_taxes=product_taxes,
            fiscal_position=quote.fiscal_position_id,document_tax_mode=quote.document_tax_mode)
        price=product._adapt_price_unit_to_document_tax_mode(price,product_taxes,product.uom_id,quote.document_tax_mode)
        return {'description':product.display_name,'uom_id':product.uom_id.id,'tax_ids':[Command.set(taxes.ids)],'price_unit':price}

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.update(self._product_defaults(self.quotation_id,self.product_id,max(1,self.target_quantity_total-self.carried_committed_quantity)))

    def _base_line(self,quantity=None):
        self.ensure_one();quote=self.quotation_id
        quantity=max(0,self.target_quantity_total-self.carried_committed_quantity) if quantity is None else quantity
        quote.company_id.currency_id._arg_require_conversion(quote.currency_id,quote.company_id,quote.date)
        return self.env['account.tax']._prepare_base_line_for_taxes_computation(self,
            product_id=self.product_id,product_uom_id=self.uom_id,price_unit=self.price_unit,discount=self.discount,
            quantity=quantity,tax_ids=self.tax_ids,currency_id=quote.currency_id,partner_id=quote.partner_id,
            document_tax_mode=quote.document_tax_mode,rate=self.env['res.currency']._get_conversion_rate(quote.company_id.currency_id,quote.currency_id,quote.company_id,quote.date),extra_tax_data={})

    @api.depends('target_quantity_total','carried_committed_quantity','price_unit','discount','tax_ids','quotation_id.accepted_snapshot','quotation_id.document_tax_mode','quotation_id.currency_id')
    def _compute_line_amounts(self):
        tax=self.env['account.tax']
        for line in self:
            frozen=(line.quotation_id.accepted_snapshot or {}).get('lines',{}).get(str(line.id))
            if frozen:values=frozen
            else:
                base=line._base_line();tax._add_tax_details_in_base_line(base,line.company_id);tax._round_base_lines_tax_details([base],line.company_id)
                detail=base['tax_details'];values={'untaxed':detail['total_excluded_currency'],'total':detail['total_included_currency']}
            line.amount_untaxed=values['untaxed'];line.amount_total=values['total'];line.amount_tax=values['total']-values['untaxed']

    @api.depends('quotation_id.order_ids.order_line.product_uom_qty','quotation_id.order_ids.arg_commitment_released')
    def _compute_committed(self):
        for line in self:line.ordered_quantity_net=line.quotation_id._committed_map().get(line.commercial_line_key,0) if line.quotation_id.commercial_root_id else 0

    def _tax_signature(self):
        fields_to_read=['name','amount','amount_type','price_include','sequence','include_base_amount','is_base_affected','children_tax_ids','tax_group_id','tax_exigibility','type_tax_use','company_id','write_date']
        taxes=self.tax_ids.flatten_taxes_hierarchy() | self.tax_ids
        tax_data=taxes.with_context(lang='en_US').sorted('id').read([name for name in fields_to_read if name in taxes._fields])
        repartitions=taxes.invoice_repartition_line_ids | taxes.refund_repartition_line_ids
        rep_fields=['factor_percent','repartition_type','account_id','tag_ids','use_in_tax_closing','document_type','write_date']
        return digest({'taxes':tax_data,'repartition':repartitions.with_context(lang='en_US').sorted('id').read([n for n in rep_fields if n in repartitions._fields])})

    def _snapshot(self):
        return {'line_id':self.id,'key':self.commercial_line_key,'product_id':self.product_id.id,
            'description':self.description or self.product_id.display_name,'unit_id':self.uom_id.id,'unit':self.uom_id.display_name,
            'target_quantity_total':self.target_quantity_total,'carried_quantity':self.carried_committed_quantity,
            'proposal_quantity':max(0,self.target_quantity_total-self.carried_committed_quantity),
            'price_unit':self.price_unit,'discount':self.discount,'tax_ids':self.tax_ids.ids,'tax_signature':self._tax_signature(),
            'tax_definitions':self.tax_ids.read(['name','amount','amount_type','price_include']),
            'unit_definition':json.loads(json.dumps(self.uom_id.with_context(lang='en_US').read([n for n in ['name','factor','relative_factor','relative_uom_id','write_date'] if n in self.uom_id._fields]),default=str)),
            'untaxed':self.amount_untaxed,'tax':self.amount_tax,'total':self.amount_total}


class Acceptance(models.Model):
    _name='arg.pyme.quotation.acceptance'
    _description='Aceptación de presupuesto ARG'
    _order='id desc'
    company_id=fields.Many2one('res.company',required=True,index=True)
    quotation_id=fields.Many2one('arg.pyme.quotation',required=True,index=True,ondelete='restrict')
    operation_key=fields.Char(required=True,index=True)
    payload_hash=fields.Char(required=True)
    user_id=fields.Many2one('res.users',required=True)
    changes=fields.Json(required=True)
    _acceptance_unique=models.Constraint('UNIQUE(company_id,quotation_id,operation_key)','La aceptación ya está registrada.')
    @api.model_create_multi
    def create(self,vals_list):
        if not self.env.su:raise AccessError(_('La aceptación se registra desde el presupuesto autorizado.'))
        return super().create(vals_list)
    def write(self,values):raise UserError(_('La aceptación registrada es inmutable.'))
    def unlink(self):raise UserError(_('La aceptación registrada se conserva.'))
