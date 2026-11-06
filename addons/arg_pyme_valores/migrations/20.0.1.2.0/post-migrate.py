from odoo import api, SUPERUSER_ID
from odoo.addons.arg_pyme_valores.hooks import sync_help_revision


def migrate(cr, version):
    # Metadata only: preserve original manual/video; flag review and link the newer guide.
    sync_help_revision(api.Environment(cr, SUPERUSER_ID, {}))
