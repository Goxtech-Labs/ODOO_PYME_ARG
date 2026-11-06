"""Optional repair catalog only: one spare and one hourly service, no operational documents."""
import json
import os

if env.cr.dbname != 'arg_demo' or os.environ.get('ARG_REPAIR_WORK_ACK_EXAMPLES') != '1':
    raise RuntimeError('Requires arg_demo and ARG_REPAIR_WORK_ACK_EXAMPLES=1')
company = env['res.company'].browse(int(os.environ['ARG_REPAIR_WORK_COMPANY_ID'])).exists()
if not company or company not in env.companies or not company.arg_demo_mode:
    raise RuntimeError('Select an enabled company explicitly marked as example')
if not env.user.has_group('arg_pyme_base.group_admin'):
    raise RuntimeError('Example catalog setup requires an ARG administrator')
module = env['ir.module.module'].search([('name', '=', 'arg_pyme_reparaciones'), ('state', '=', 'installed')])
if module.latest_version not in ('20.0.1.1.0', '20.0.1.2.0'):
    raise RuntimeError('This catalog loader targets Reparaciones ARG20.0.1.1.0/20.0.1.2.0')
context = {key: value for key, value in env.context.items() if not key.startswith('default_')}
context.update(allowed_company_ids=company.ids, tracking_disable=True, mail_notrack=True,
               mail_create_nosubscribe=True)
env = env(context=context)
company = env['res.company'].browse(company.id)
units = env.ref('uom.product_uom_unit')
hours = env.ref('uom.product_uom_hour')
models = ['stock.move', 'account.move', 'account.payment', 'arg.pyme.quotation', 'sale.order',
          'arg.pyme.repair.case', 'arg.pyme.repair.event', 'arg.pyme.repair.intervention']
counts = {model: env[model].search_count([('company_id', '=', company.id)]) for model in models}
created = []


def product(key, values):
    identity = env['ir.model.data'].search([('module', '=', 'arg_demo'), ('name', '=', key)])
    if identity:
        if len(identity) != 1 or identity.model != 'product.template':
            raise RuntimeError('Fixture identity belongs to another model')
        record = env['product.template'].browse(identity.res_id).exists()
        if not record or record.company_id != company:
            raise RuntimeError('Fixture target is absent or belongs to another company')
        record.check_access('read')
        return record
    record = env['product.template'].with_company(company).create({'company_id': company.id, **values})
    env['ir.model.data'].create({'module': 'arg_demo', 'name': key, 'model': record._name,
                               'res_id': record.id, 'noupdate': True})
    created.append(key)
    return record


spare = product('repairs_spare', {'name': 'EJEMPLO · Interruptor de repuesto ARG',
    'type': 'consu', 'is_storable': True, 'uom_id': units.id, 'list_price': 15000,
    'standard_price': 9000, 'invoice_policy': 'delivery'})
service = product('repairs_hourly_service', {'name': 'EJEMPLO · Hora de servicio técnico ARG',
    'type': 'service', 'service_type': 'manual', 'uom_id': hours.id, 'list_price': 12000,
    'invoice_policy': 'delivery', 'purchase_ok': False})
if spare.type != 'consu' or not spare.is_storable or spare.uom_id != units:
    raise RuntimeError('Spare fixture was customized incompatibly; not replacing it')
if service.type != 'service' or service.service_type != 'manual' or service.uom_id != hours or service.invoice_policy != 'delivery':
    raise RuntimeError('Service fixture was customized incompatibly; not replacing it')
for model, before in counts.items():
    if env[model].search_count([('company_id', '=', company.id)]) != before:
        raise RuntimeError('Unexpected operational effect during catalog setup')
env.cr.commit()
print('ARG_REPAIR_WORK_EXAMPLES=' + json.dumps({'created_keys': created,
    'spare_template_id': spare.id, 'service_template_id': service.id,
    'stock_moves_created': 0, 'worklogs_created': 0, 'orders_created': 0,
    'invoices_created': 0, 'payments_created': 0, 'external_calls': 0}))
