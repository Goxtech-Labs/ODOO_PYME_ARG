from odoo import models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_arg_variants(self):
        self.ensure_one()
        self.env['arg.pyme.variant.matrix']._scoped()._template(self.id)
        return {
            'type': 'ir.actions.client', 'name': 'Variantes ARG',
            'tag': 'arg_pyme.variant_matrix', 'params': {'template_id': self.id}}

    def action_arg_advanced(self):
        self.ensure_one()
        self.check_access('read')
        view = self.env.ref('product.product_template_only_form_view')
        return {'type': 'ir.actions.act_window', 'res_model': self._name,
                'res_id': self.id, 'views': [(view.id, 'form')]}
