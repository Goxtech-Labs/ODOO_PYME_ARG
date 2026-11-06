def post_init_hook(env):
    env['arg.pyme.document.type']._ensure_companies(env['res.company'].search([]))
