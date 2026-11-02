def post_init_hook(env):
    fixture=env.ref('arg_demo.customer_pyme',raise_if_not_found=False)
    if fixture: env.company.arg_demo_mode=True
