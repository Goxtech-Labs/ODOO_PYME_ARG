def sync_help_revision(env):
    previous = env.ref('arg_pyme_reparaciones.help_repairs_intake', raise_if_not_found=False)
    current = env.ref('arg_pyme_reparaciones.help_repairs_work', raise_if_not_found=False)
    if previous and current and previous.state == 'current':
        previous.write({'state': 'review', 'replacement_id': current.id})


def post_init_hook(env):
    env['arg.pyme.document.type']._ensure_companies(env['res.company'].search([]))
    sync_help_revision(env)
