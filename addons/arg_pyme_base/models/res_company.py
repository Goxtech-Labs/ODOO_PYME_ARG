from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'
    arg_default_currency_id = fields.Many2one('res.currency', string='Moneda de gestión ARG', default=lambda s: s.env.company.currency_id)

    @api.model_create_multi
    def create(self, values_list):
        companies = super().create(values_list)
        self.env['arg.pyme.document.type']._ensure_companies(companies)
        return companies
