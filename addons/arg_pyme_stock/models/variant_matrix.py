from odoo import models
from odoo.exceptions import AccessError


class VariantMatrix(models.AbstractModel):
    _inherit = 'arg.pyme.variant.matrix'

    def _arg_quantities(self, products):
        result = super()._arg_quantities(products)
        goods = products.filtered(lambda product: product.is_storable)
        for product in products - goods:
            result[product.id]['status'] = 'not_applicable'
        if not goods:
            return result
        for product in goods:
            result[product.id]['status'] = 'unknown'
        if not (self.env.user.has_group('arg_pyme_base.group_stock') or self.env.user.has_group('arg_pyme_base.group_admin')):
            return result
        try:
            # ACL and rules remain native. This is the current visible company scope,
            # not a historic or complete-warehouse integrity assertion.
            self.env['stock.quant'].check_access('read')
            rows = goods.read(['qty_available', 'free_qty'])
            for row in rows:
                result[row['id']] = {'status': 'known', 'physical': row['qty_available'], 'free': row['free_qty']}
        except AccessError:
            pass
        return result
