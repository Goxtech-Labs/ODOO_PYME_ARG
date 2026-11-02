from odoo import Command

def post_init_hook(env):
    # Only stable, explicitly labelled fixtures are assigned roles automatically.
    for key, role in [('customer_retail','customer'),('customer_pyme','customer'),('supplier_general','supplier')]:
        partner=env.ref('arg_demo.'+key,raise_if_not_found=False)
        if partner:
            partner.with_context(tracking_disable=True).write({'arg_role_ids':[Command.link(env.ref('arg_pyme_terceros.role_'+role).id)]})
