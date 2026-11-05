"""Optional masters and ONE cheque draft. No posting, stock, external calls or cron changes."""
import os
import json
from odoo import Command, fields

if os.environ.get('ARG_VALUES_ACK_EXAMPLES') != '1' or env.cr.dbname != 'arg_demo':
    raise RuntimeError('Requires arg_demo and ARG_VALUES_ACK_EXAMPLES=1')
company = env['res.company'].browse(int(os.environ['ARG_VALUES_COMPANY_ID'])).exists()
if not company or company not in env.companies or not company.arg_demo_mode:
    raise RuntimeError('Choose an enabled company explicitly marked as example')
context = {k: v for k, v in env.context.items() if not k.startswith('default_')}
context.update(allowed_company_ids=company.ids, tracking_disable=True, mail_notrack=True, mail_create_nosubscribe=True)
env = env(context=context)
company = env['res.company'].browse(company.id)
company.check_access('write')
if company.arg_value_receipt_method_id:
    previous = env.ref('arg_demo.values_journal', raise_if_not_found=False)
    if not previous or company.arg_value_receipt_method_id.journal_id != previous:
        raise RuntimeError('A value profile is already configured; not replacing it')

business_models = ['account.move', 'account.payment', 'arg.pyme.treasury.document']
if 'stock.move' in env:
    business_models.append('stock.move')
counts = {model: env[model].search_count([('company_id', '=', company.id)]) for model in business_models}
created = []

def example(model, key, values):
    record = env.ref('arg_demo.' + key, raise_if_not_found=False)
    if record:
        if record._name != model or ('company_id' in record._fields and record.company_id != company):
            raise RuntimeError('Fixture reference or company mismatch')
        return record
    record = env[model].create(values)
    env['ir.model.data'].create({'module': 'arg_demo', 'name': key, 'model': model, 'res_id': record.id, 'noupdate': True})
    created.append(key)
    return record

account = example('account.account', 'values_account', {
    'name': 'Valores a depositar · EJEMPLO ARG', 'code': 'ARGVAL001', 'account_type': 'asset_current',
    'reconcile': True, 'company_ids': [Command.set(company.ids)]})
if account.account_type != 'asset_current' or not account.reconcile or company not in account.company_ids:
    raise RuntimeError('Example account was customized; not overwriting it')
journal = example('account.journal', 'values_journal', {
    'name': 'Cartera de cheques · EJEMPLO ARG', 'code': 'ARGV', 'type': 'bank', 'company_id': company.id})
if journal.type != 'bank' or journal.code != 'ARGV':
    raise RuntimeError('Example journal was customized; not overwriting it')
method = journal.inbound_payment_method_line_ids.filtered(lambda m: m.code == 'manual')
if len(method) != 1:
    raise RuntimeError('The example journal requires one manual inbound method')
if method.payment_account_id and method.payment_account_id != account and 'values_journal' not in created:
    raise RuntimeError('Example payment method was customized; not overwriting it')
if method.payment_account_id != account:
    method.write({'payment_account_id': account.id})
company.write({'arg_value_receipt_method_id': method.id})
customer = example('res.partner', 'values_customer', {'name': 'EJEMPLO · Cliente cartera ARG', 'company_id': company.id})
issuer = example('res.partner', 'values_issuer', {'name': 'EJEMPLO · Librador de cheque ARG', 'company_id': company.id})
today = fields.Date.context_today(env['arg.pyme.value.instrument'])
value = example('arg.pyme.value.instrument', 'values_paper_cheque', {
    'company_id': company.id, 'date': today, 'partner_id': customer.id,
    'instrument_kind': 'cheque', 'ownership': 'third_party', 'support': 'paper', 'cheque_type': 'deferred',
    'currency_id': (company.arg_default_currency_id or company.currency_id).id, 'amount': 100000,
    'bank_name': 'BANCO FICTICIO · EJEMPLO', 'bank_identifier': 'DEMO-ARG',
    'issuer_account': 'CUENTA-FICTICIA-ARG', 'instrument_number': 'EJEMPLO-0001', 'issuer_id': issuer.id,
    'issued_on': today, 'payable_on': today,
    'note': 'DATOS FICTICIOS. Borrador de aprendizaje, sin recepción ni validez bancaria. No es un cheque real.'})
for model, count in counts.items():
    if env[model].search_count([('company_id', '=', company.id)]) != count:
        raise RuntimeError('Unexpected accounting, treasury or stock effect')
env.cr.commit()
print('ARG_VALUES_EXAMPLES=' + json.dumps({'created_keys': created, 'cheque_id': value.id,
    'cheque_number': value.arg_number, 'state': value.state, 'draft_created': 'values_paper_cheque' in created,
    'payments_created': 0, 'account_moves_created': 0, 'external_calls': 0}))
