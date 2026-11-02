"""Finance master examples only. Execute via native Odoo shell, never on a business database."""
import json
from odoo import Command

company = env.ref('base.main_company')
if env.cr.dbname != 'arg_demo' or not company.arg_demo_mode:
    raise RuntimeError('Finance fixtures require the identified arg_demo company')
if env['account.move'].search_count([]) or env['account.payment'].search_count([]) or env['arg.pyme.treasury.document'].search_count([]):
    raise RuntimeError('Business records exist; this fixture refuses to change their configuration')
env = env(context={**env.context, 'allowed_company_ids': company.ids, 'tracking_disable': True, 'mail_notrack': True, 'mail_create_nosubscribe': True})
company = env['res.company'].browse(company.id)

def example(model, key, values):
    record = env.ref('arg_demo.' + key, raise_if_not_found=False)
    if record:
        if record._name != model or ('company_id' in record._fields and record.company_id != company):
            raise RuntimeError('Fixture reference mismatch')
        return record
    record = env[model].create(values)
    env['ir.model.data'].create({'module':'arg_demo', 'name':key, 'model':model, 'res_id':record.id, 'noupdate':True})
    return record

journals = {}
for kind, code, title in [('cash','ARGC','Caja de ejemplo ARG'),('bank','ARGB','Banco de ejemplo ARG')]:
    journal = example('account.journal', 'finance_' + kind, {'name':title, 'code':code, 'type':kind, 'company_id':company.id})
    if journal.type != kind or journal.code != code:
        raise RuntimeError('An existing example journal was customized; inspect before rerunning')
    journals[kind] = journal
    for direction in ['inbound','outbound']:
        methods = journal[direction + '_payment_method_line_ids'].filtered(lambda l:l.code == 'manual')
        if len(methods) != 1:
            raise RuntimeError('The example journal requires one manual method per direction')
        if kind == 'cash':
            account = journal.default_account_id
        else:
            template_key = 'account_journal_payment_debit_account_id' if direction == 'inbound' else 'account_journal_payment_credit_account_id'
            account = env['account.chart.template'].with_company(company).ref(template_key, raise_if_not_found=False)
            if not account:
                account = example('account.account', 'outstanding_' + direction, {
                    'name':('Cobros por acreditar' if direction == 'inbound' else 'Pagos por acreditar') + ' · Ejemplo ARG',
                    'code':'ARG1001' if direction == 'inbound' else 'ARG1002', 'account_type':'asset_current',
                    'reconcile':True, 'company_ids':[Command.set(company.ids)]})
        if not account:
            raise RuntimeError('Missing example payment account')
        if not methods.payment_account_id:
            methods.write({'payment_account_id':account.id})
        elif methods.payment_account_id != account:
            raise RuntimeError('An existing fixture method was customized; not overwriting it')
defaults = {'arg_receipt_method_id':journals['cash'].inbound_payment_method_line_ids.filtered(lambda l:l.code == 'manual').id,
            'arg_payment_method_id':journals['cash'].outbound_payment_method_line_ids.filtered(lambda l:l.code == 'manual').id}
for field, value in defaults.items():
    if company[field] and company[field].id != value:
        raise RuntimeError('An existing company default was customized; not overwriting it')
company.write(defaults)
env['ir.cron'].with_context(active_test=False).search([]).write({'active':False})
env['ir.mail_server'].with_context(active_test=False).search([]).write({'active':False})
if env['account.move'].search_count([]) or env['account.payment'].search_count([]) or env['arg.pyme.treasury.document'].search_count([]):
    raise RuntimeError('Unexpected business effect while preparing masters')
env.cr.commit()
print('ARG_FINANCE_MASTERS=' + json.dumps({'journal_ids':{key:journal.id for key,journal in journals.items()},
      'receipt_method_id':company.arg_receipt_method_id.id, 'payment_method_id':company.arg_payment_method_id.id,
      'business_records_created':0, 'bank_credentials_added':False, 'fiscal_ids_added':False}))
