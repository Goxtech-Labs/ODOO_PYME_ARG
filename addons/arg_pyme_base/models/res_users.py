from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'
    arg_density = fields.Selection([('comfortable', 'Cómoda'), ('compact', 'Compacta')], default='comfortable', string='Densidad ARG', user_writeable=True)
    arg_theme = fields.Selection([('light', 'Claro'), ('dark', 'Oscuro'), ('system', 'Según dispositivo')], default='system', string='Tema ARG', user_writeable=True)

