"""Opt-in example catalog only. Native variants, no stock or financial operations.

Run inside Odoo shell with ARG_VARIANTS_ACK_EXAMPLES=1 and an explicit
ARG_VARIANTS_COMPANY_ID. Existing identities are reused, never reset or reactivated.
"""
import json
import os

if env.cr.dbname != 'arg_demo' or os.environ.get('ARG_VARIANTS_ACK_EXAMPLES') != '1':
    raise RuntimeError('Requires arg_demo and ARG_VARIANTS_ACK_EXAMPLES=1')
company = env['res.company'].browse(int(os.environ['ARG_VARIANTS_COMPANY_ID'])).exists()
if not company or company not in env.companies or not company.arg_demo_mode:
    raise RuntimeError('Select an enabled company explicitly marked as example')
if not env.user.has_group('arg_pyme_base.group_admin'):
    raise RuntimeError('Example catalog setup requires an ARG administrator')
module = env['ir.module.module'].search([('name', '=', 'arg_pyme_catalogo'), ('state', '=', 'installed')])
if module.latest_version != '20.0.1.1.0':
    raise RuntimeError('This example loader targets Catalogo ARG20.0.1.1.0')
env = env(context={'allowed_company_ids': company.ids, 'lang': env.context.get('lang'),
                   'tz': env.context.get('tz'), 'tracking_disable': True, 'mail_notrack': True,
                   'mail_create_nosubscribe': True})
company = env['res.company'].browse(company.id)
env.cr.execute('SELECT pg_advisory_xact_lock(%s, %s)', [440791, company.id])
observed_models = [name for name in ['stock.move', 'stock.quant', 'account.move', 'account.payment',
    'sale.order', 'purchase.order', 'arg.pyme.quotation', 'arg.pyme.treasury.document',
    'arg.pyme.repair.case', 'arg.pyme.repair.event', 'arg.pyme.repair.intervention',
    'arg.pyme.value.instrument'] if name in env]
counts = {name: env[name].with_context(active_test=False).search_count([('company_id', '=', company.id)])
          for name in observed_models}
created = []
prefix = 'variants_c%s_' % company.id


def identity(key, model):
    xid = env['ir.model.data'].search([('module', '=', 'arg_demo'), ('name', '=', prefix + key)])
    if not xid:
        return env[model]
    if len(xid) != 1 or xid.model != model:
        raise RuntimeError('Example identity belongs to another model')
    record = env[model].with_context(active_test=False).browse(xid.res_id).exists()
    record.check_access('read')
    if not record:
        raise RuntimeError('Example target is absent; do not silently recreate deleted data')
    return record


def tag(key, record):
    env['ir.model.data'].create({'module': 'arg_demo', 'name': prefix + key,
                               'model': record._name, 'res_id': record.id, 'noupdate': True})
    created.append(prefix + key)
    return record


def fixture(key, model, values):
    return identity(key, model) or tag(key, env[model].create(values))


specs = [('size', 'EJEMPLO · Talle ARG', [('s', 'S'), ('m', 'M')]),
         ('color', 'EJEMPLO · Color ARG', [('sky', 'Celeste'), ('white', 'Blanco')]),
         ('finish', 'EJEMPLO · Terminación ARG', [('matte', 'Mate'), ('bright', 'Brillante')])]
lines = []
for key, name, choices in specs:
    attribute = fixture('attribute_' + key, 'product.attribute', {'name': name, 'create_variant': 'always'})
    if attribute.create_variant != 'always':
        raise RuntimeError('Example attribute was customized; not replacing its generation policy')
    values = []
    for code, label in choices:
        value = fixture('value_' + key + '_' + code, 'product.attribute.value',
                        {'name': label, 'attribute_id': attribute.id})
        if value.attribute_id != attribute:
            raise RuntimeError('Example value belongs to another attribute')
        values.append(value.id)
    lines.append((attribute.id, values))

template = identity('template', 'product.template')
new_template = not template
if new_template:
    data = {'name': 'EJEMPLO · Artículo con variantes ARG', 'company_id': company.id,
            'type': 'consu', 'uom_id': env.ref('uom.product_uom_unit').id, 'list_price': 10000,
            'attribute_line_ids': [(0, 0, {'attribute_id': attribute, 'value_ids': [(6, 0, values)]})
                                   for attribute, values in lines]}
    if 'is_storable' in env['product.template']._fields:
        data['is_storable'] = True
    template = tag('template', env['product.template'].with_company(company).create(data))
    variants = template.product_variant_ids.sorted('id')
    if len(variants) != 8:
        raise RuntimeError('Native generation did not produce the eight expected example variants')
    for index, variant in enumerate(variants, 1):
        variant.write({'default_code': 'ARG-EJ-VAR-%03d' % index})
        tag('product_%03d' % index, variant)
elif template.company_id != company:
    raise RuntimeError('Example template belongs to another company')
else:
    # Respect subsequent edits, archive state, prices, codes and chosen combinations.
    for index in range(1, 9):
        variant = identity('product_%03d' % index, 'product.product')
        if not variant or variant.product_tmpl_id != template:
            raise RuntimeError('Example variant identity was removed or replaced; inspect it manually')

for name, before in counts.items():
    if env[name].with_context(active_test=False).search_count([('company_id', '=', company.id)]) != before:
        raise RuntimeError('Unexpected operational effect while creating example catalog')
result = {'created_keys': created, 'template_id': template.id,
          'template_active': template.active, 'active_variants': len(template.product_variant_ids.filtered('active')),
          'new_template': new_template, 'observed_operational_models_unchanged': observed_models,
          'company_currency': company.currency_id.name, 'loader_external_calls_requested': 0,
          'business_walkthrough_executed': False}
env.cr.commit()
print('ARG_VARIANTS_EXAMPLES=' + json.dumps(result))
