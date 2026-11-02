from odoo import models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_arg_advanced(self):
        self.ensure_one()
        self.check_access('read')
        view = self.env.ref('product.product_template_only_form_view')
        return {'type': 'ir.actions.act_window', 'res_model': self._name,
                'res_id': self.id, 'views': [(view.id, 'form')]}
