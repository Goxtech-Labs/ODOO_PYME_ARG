# Generic attributes remain native; no forced sizes, colours or variant generation.
from odoo import models

class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    def action_arg_products(self):
        self.ensure_one()
        self.check_access('read')
        return {'type': 'ir.actions.act_window', 'name': 'Productos ARG',
                'res_model': 'product.template', 'view_mode': 'list,form',
                'domain': [('attribute_line_ids.attribute_id', '=', self.id)]}
