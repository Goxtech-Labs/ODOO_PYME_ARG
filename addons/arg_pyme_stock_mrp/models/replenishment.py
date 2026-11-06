"""Manufacturing-specific configuration on native orderpoints and BOMs."""
from odoo import models, _
from odoo.fields import Domain


class Replenishment(models.AbstractModel):
    _inherit = 'arg.pyme.replenishment'

    def _extension_specs(self):
        return {**super()._extension_specs(), 'bom': {
            'field': 'bom_id', 'model': 'mrp.bom', 'label': _('Fabricación / lista de materiales'),
        }}

    def _extension_domain(self, kind, product, query):
        if kind != 'bom':
            return super()._extension_domain(kind, product, query)
        template = self._get(product, 'product_tmpl_id')
        self._record('product.template', template.id)
        domain = (Domain('company_id', 'in', [False, self.env.company.id])
                  & Domain('type', '=', 'normal')
                  & Domain('product_tmpl_id', '=', template.id)
                  & Domain('product_id', 'in', [False, product.id]))
        if query:
            model = self.env['mrp.bom']
            model.check_field_access(model._fields['code'], 'read')
            domain &= Domain('code', 'ilike', query)
        return domain

    def _extension_label(self, kind, record):
        if kind != 'bom':
            return super()._extension_label(kind, record)
        template = self._get(record, 'product_tmpl_id')
        self._record('product.template', template.id)
        variant = self._get(record, 'product_id')
        if variant:
            self._record('product.product', variant.id)
        unit = self._get(record, 'uom_id')
        self._record('uom.uom', unit.id, active=True)
        quantity = self._number(self._get(record, 'product_qty'))
        code = self._get(record, 'code') or _('Sin referencia')
        return _('%(product)s · %(code)s · %(quantity)s %(unit)s',
                 product=self._label(variant or template), code=code,
                 quantity=quantity, unit=self._label(unit))
