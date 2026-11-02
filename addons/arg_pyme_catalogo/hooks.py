def post_init_hook(env):
    # A standalone editable demonstration list; never rewrite an existing native list.
    if env.ref('arg_demo.customer_pyme', raise_if_not_found=False) and not env.ref('arg_pyme_catalogo.demo_pricelist', raise_if_not_found=False):
        record = env['product.pricelist'].create({'name': 'Ejemplo — Lista general ARG',
            'currency_id': env.company.currency_id.id, 'company_id': env.company.id})
        env['ir.model.data'].create({'module': 'arg_pyme_catalogo', 'name': 'demo_pricelist',
            'model': record._name, 'res_id': record.id, 'noupdate': True})
