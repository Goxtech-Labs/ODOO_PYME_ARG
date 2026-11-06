from odoo import api, SUPERUSER_ID
from odoo.addons.arg_pyme_reparaciones.hooks import sync_help_revision


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['arg.pyme.document.type']._ensure_companies(env['res.company'].search([]))
    sync_help_revision(env)
