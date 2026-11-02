import re
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class PartnerRole(models.Model):
    _name = 'arg.pyme.partner.role'
    _description = 'Rol de tercero ARG'
    name = fields.Char(required=True, string='Rol')
    code = fields.Char(required=True, index=True, string='Código')
    active = fields.Boolean(default=True)
    _code_unique = models.Constraint('UNIQUE(code)', 'El código de rol ya existe.')

    @api.constrains('code')
    def _check_code(self):
        for rec in self:
            if not re.fullmatch(r'[a-z][a-z0-9_]{1,39}', rec.code or ''):
                raise ValidationError(_('Usá un código de rol simple, en minúsculas.'))

    def write(self, values):
        if 'code' in values and self.env['res.partner'].sudo().search_count([('arg_role_ids','in',self.ids)]):
            raise UserError(_('No cambies el código de un rol utilizado; conservá su significado.'))
        return super().write(values)

    def unlink(self):
        if self.env['res.partner'].sudo().search_count([('arg_role_ids','in',self.ids)]):
            raise UserError(_('Este rol está utilizado. Podés archivarlo.'))
        return super().unlink()

class ResPartner(models.Model):
    _inherit = 'res.partner'
    arg_role_ids = fields.Many2many('arg.pyme.partner.role', string='Roles de gestión', groups='base.group_user')
    arg_currency_id = fields.Many2one('res.currency', company_dependent=True, string='Moneda preferida ARG', groups='base.group_user')
    arg_conditions_note = fields.Text(company_dependent=True, string='Condiciones conocidas ARG', groups='base.group_user')
    arg_tax_search_key = fields.Char(compute='_compute_arg_tax_key', store=True, index=True, copy=False, groups='base.group_user')
    arg_duplicate_count = fields.Integer(compute='_compute_arg_duplicates', string='Posibles coincidencias', groups='base.group_user')

    @api.depends('vat', 'country_id')
    def _compute_arg_tax_key(self):
        for partner in self:
            raw = re.sub(r'[^A-Z0-9]', '', (partner.vat or '').upper())
            country = partner.country_id.code or ''
            if country and raw.startswith(country):raw = raw[len(country):]
            partner.arg_tax_search_key = (country + ':' + raw) if raw and raw not in {'NA'} else False

    @api.depends('arg_tax_search_key')
    def _compute_arg_duplicates(self):
        for partner in self:
            partner.arg_duplicate_count = self.search_count([
                ('arg_tax_search_key','=',partner.arg_tax_search_key), ('id','!=',partner._origin.id or 0),
                ('parent_id','=',False)]) if partner.arg_tax_search_key else 0

    @api.onchange('vat', 'country_id')
    def _onchange_arg_duplicate(self):
        if self.arg_duplicate_count:
            return {'warning':{'title':_('Revisá las coincidencias'), 'message':_('Ya hay contactos con esta identificación. Revisá su ficha antes de crear otra; no se fusiona automáticamente.')}}

    @api.model_create_multi
    def create(self, values_list):
        prepared=[]
        for values in values_list:
            values=dict(values)
            if values.get('arg_role_ids') and 'country_id' not in values:
                values['country_id']=self.env.company.country_id.id
            prepared.append(values)
        records=super().create(prepared)
        records._arg_sync_native_roles()
        return records

    def write(self, values):
        result=super().write(values)
        if 'arg_role_ids' in values:self._arg_sync_native_roles()
        return result

    def _arg_sync_native_roles(self):
        for partner in self:
            codes=set(partner.arg_role_ids.mapped('code'))
            values={}
            for code, field in [('customer','customer_rank'),('supplier','supplier_rank')]:
                if code in codes and field in partner._fields and not partner[field]:values[field]=1
            if values:partner.write(values)

    def _arg_document_defaults(self, direction='sale'):
        self.ensure_one();self.check_access('read')
        if direction not in ('sale','purchase'):raise ValidationError(_('Circuito desconocido.'))
        addresses=self.address_get(['invoice','delivery'])
        term_field='property_payment_term_id' if direction=='sale' else 'property_supplier_payment_term_id'
        pricelist = self.property_product_pricelist if 'property_product_pricelist' in self._fields and direction=='sale' else False
        native_currency = pricelist.currency_id if pricelist else (self.property_purchase_currency_id if direction=='purchase' and 'property_purchase_currency_id' in self._fields else False)
        if self.arg_currency_id and native_currency and self.arg_currency_id != native_currency:
            raise ValidationError(_('La moneda preferida no coincide con la tarifa o moneda nativa del tercero. Elegí condiciones compatibles antes de continuar.'))
        currency = native_currency or self.arg_currency_id or self.env.company.currency_id
        result={'partner_id':self.id,'currency_id':currency.id,
                'invoice_partner_id':addresses.get('invoice',self.id),'delivery_partner_id':addresses.get('delivery',self.id),
                'conditions_note':self.arg_conditions_note or False,
                'payment_term_id':self[term_field].id if term_field in self._fields else False,
                'pricelist_id':pricelist.id if pricelist else False}
        return result

    def action_arg_duplicates(self):
        self.ensure_one();self.check_access('read')
        action=self.env['ir.actions.actions']._for_xml_id('arg_pyme_terceros.action_all_partners')
        action['domain']=[('arg_tax_search_key','=',self.arg_tax_search_key),('id','!=',self.id)] if self.arg_tax_search_key else [('id','=',False)]
        return action

    def action_arg_advanced(self):
        self.ensure_one();self.check_access('read')
        return {'type':'ir.actions.act_window','name':_('Ficha avanzada'),'res_model':'res.partner','res_id':self.id,
                'view_mode':'form','views':[(self.env.ref('base.view_partner_form').id,'form')]}
