"""Purchase-specific replenishment configuration; no order generation here."""
from odoo import fields, models, _
from odoo.fields import Domain


class Replenishment(models.AbstractModel):
    _inherit = 'arg.pyme.replenishment'

    def _extension_specs(self):
        return {**super()._extension_specs(), 'supplier': {
            'field': 'supplier_id', 'model': 'product.supplierinfo', 'label': _('Proveedor / condición'),
        }}

    def _extension_domain(self, kind, product, query):
        if kind != 'supplier':
            return super()._extension_domain(kind, product, query)
        template = self._get(product, 'product_tmpl_id')
        self._record('product.template', template.id)
        partners = Domain('company_id', 'in', [False, self.env.company.id]) & Domain('active', '=', True)
        if query:
            model = self.env['res.partner']
            model.check_field_access(model._fields['name'], 'read')
            partners &= Domain('name', 'ilike', query)
        return (Domain('company_id', 'in', [False, self.env.company.id])
                & Domain('product_tmpl_id', '=', template.id)
                & Domain('product_id', 'in', [False, product.id])
                & Domain('partner_id', 'in', self.env['res.partner']._search(partners)))

    def _extension_label(self, kind, record):
        if kind != 'supplier':
            return super()._extension_label(kind, record)
        partner = self._get(record, 'partner_id')
        self._record('res.partner', partner.id, active=True)
        unit = self._get(record, 'uom_id')
        self._record('uom.uom', unit.id, active=True)
        minimum = self._number(self._get(record, 'min_qty'))
        start = self._get(record, 'date_start')
        end = self._get(record, 'date_end')
        return _('%(partner)s · mín. %(minimum)s %(unit)s · %(start)s / %(end)s',
                 partner=self._label(partner), minimum=minimum, unit=self._label(unit),
                 start=fields.Date.to_string(start) if start else _('Sin inicio'),
                 end=fields.Date.to_string(end) if end else _('Sin vencimiento'))
