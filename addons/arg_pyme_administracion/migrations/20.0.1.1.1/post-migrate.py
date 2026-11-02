from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    old = env.ref('arg_pyme_administracion.help_current_account', raise_if_not_found=False)
    new = env.ref('arg_pyme_administracion.help_treasury', raise_if_not_found=False)
    if old and new:
        old.write({'state':'review' if old.url else 'replaced', 'replacement_id':new.id})
