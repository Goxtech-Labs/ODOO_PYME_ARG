"""Optional fictitious customer and one REP draft; never receive, move stock or invoice."""
import json
import os

if env.cr.dbname != 'arg_demo' or os.environ.get('ARG_REPAIRS_ACK_EXAMPLES') != '1':
    raise RuntimeError('Requires arg_demo and ARG_REPAIRS_ACK_EXAMPLES=1')
company = env['res.company'].browse(int(os.environ['ARG_REPAIRS_COMPANY_ID'])).exists()
if not company or company not in env.companies or not company.arg_demo_mode:
    raise RuntimeError('Select an enabled company explicitly marked as example')
if not env.user.has_group('arg_pyme_base.group_admin'):
    raise RuntimeError('Example setup requires an ARG administrator')
if not env['ir.module.module'].search_count([('name', '=', 'arg_pyme_reparaciones'), ('state', '=', 'installed')]):
    raise RuntimeError('Install Reparaciones ARG before loading examples')
context = {key: value for key, value in env.context.items() if not key.startswith('default_')}
context.update(allowed_company_ids=company.ids, tracking_disable=True, mail_notrack=True,
               mail_create_nosubscribe=True)
env = env(context=context)
company = env['res.company'].browse(company.id)
models = ['stock.move', 'account.move', 'account.payment', 'arg.pyme.quotation',
          'sale.order', 'arg.pyme.repair.event']
counts = {model: env[model].search_count([('company_id', '=', company.id)]) for model in models}
created = []


def example(model, key, values):
    identity = env['ir.model.data'].search([('module', '=', 'arg_demo'), ('name', '=', key)])
    if identity:
        if len(identity) != 1 or identity.model != model:
            raise RuntimeError('Fixture identity belongs to another model')
        record = env[model].browse(identity.res_id).exists()
        if not record or record.company_id != company:
            raise RuntimeError('Fixture target is absent or belongs to another company')
        record.check_access('read')
        return record
    record = env[model].create(values)
    env['ir.model.data'].create({'module': 'arg_demo', 'name': key, 'model': model,
                               'res_id': record.id, 'noupdate': True})
    created.append(key)
    return record


customer = example('res.partner', 'repairs_customer', {
    'name': 'EJEMPLO · Cliente de reparaciones ARG', 'company_id': company.id,
})
case = example('arg.pyme.repair.case', 'repairs_intake', {
    'company_id': company.id, 'partner_id': customer.id,
    'equipment': 'EJEMPLO · Taladro del cliente',
    'symptom': 'EJEMPLO FICTICIO · No enciende al accionar el interruptor.',
    'accessories': 'EJEMPLO · Equipo y cable, sin maletín.',
    'notes': 'DATOS FICTICIOS. Borrador para aprender, sin recepción ni intervención registrada.',
})
for model, before in counts.items():
    if env[model].search_count([('company_id', '=', company.id)]) != before:
        raise RuntimeError('Unexpected operational effect while loading a draft')
env.cr.commit()
print('ARG_REPAIRS_EXAMPLES=' + json.dumps({
    'created_keys': created, 'case_id': case.id, 'number': case.arg_number, 'state': case.state,
    'draft_created': 'repairs_intake' in created, 'events_created': 0,
    'stock_moves_created': 0, 'invoices_created': 0, 'payments_created': 0,
    'external_calls': 0,
}))
