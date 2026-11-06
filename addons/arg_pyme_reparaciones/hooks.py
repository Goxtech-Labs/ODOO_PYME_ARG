def sync_help_revision(env):
    for old, new in [('help_repairs_intake', 'help_repairs_work'),
                     ('help_repairs_work', 'help_repairs_corrections')]:
        previous = env.ref('arg_pyme_reparaciones.' + old, raise_if_not_found=False)
        current = env.ref('arg_pyme_reparaciones.' + new, raise_if_not_found=False)
        if previous and current and previous.state == 'current':
            previous.write({'state': 'review', 'replacement_id': current.id})


def post_init_hook(env):
    env['arg.pyme.document.type']._ensure_companies(env['res.company'].search([]))
    sync_help_revision(env)
