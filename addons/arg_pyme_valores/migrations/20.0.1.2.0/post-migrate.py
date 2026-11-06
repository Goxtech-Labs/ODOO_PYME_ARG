from odoo import api, SUPERUSER_ID
from odoo.addons.arg_pyme_valores.hooks import sync_help_revision
from odoo.addons.arg_pyme_valores.models.value_event import _VALUE_ENGINE


def migrate(cr, version):
    # Metadata only: preserve original manual/video; flag review and link the newer guide.
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Metadata only; historical anonymous payments retain correction/reconciliation callbacks.
    # New creation/posting or changed monetary terms still enforce the current policy.
    previous = env['account.payment'].search([('arg_value_instrument_id','=',False),
                                            ('arg_value_pre12_payment','=',False)])
    previous.with_context(_arg_value_engine=_VALUE_ENGINE).write({'arg_value_pre12_payment': True})
    sync_help_revision(env)
