from odoo import api, SUPERUSER_ID
from odoo.addons.arg_pyme_reparaciones.hooks import sync_help_revision


def migrate(cr, version):
    sync_help_revision(api.Environment(cr, SUPERUSER_ID, {}))
