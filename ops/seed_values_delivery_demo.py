"""Optional OPA masters and own-cheque draft. No payments, posting, stock or external operations."""
import os
import json
from odoo import Command, fields

if env.cr.dbname != 'arg_demo' or os.environ.get('ARG_VALUES_DELIVERY_ACK_EXAMPLES') != '1':
    raise RuntimeError('Requires arg_demo and ARG_VALUES_DELIVERY_ACK_EXAMPLES=1')
company = env['res.company'].browse(int(os.environ['ARG_VALUES_COMPANY_ID'])).exists()
if not company or company not in env.companies or not company.arg_demo_mode:
    raise RuntimeError('Choose an allowed company explicitly marked as example')
context = {k: v for k, v in env.context.items() if not k.startswith('default_')}
context.update(allowed_company_ids=company.ids, tracking_disable=True, mail_notrack=True, mail_create_nosubscribe=True)
env = env(context=context)
company = env['res.company'].browse(company.id)
company.check_access('write')
portfolio = env.ref('arg_demo.values_account', raise_if_not_found=False)
receipt_journal = env.ref('arg_demo.values_journal', raise_if_not_found=False)
if not portfolio or not receipt_journal or company not in portfolio.company_ids or receipt_journal.company_id != company:
    raise RuntimeError('Load and preserve the basic values example first')
if company.arg_value_receipt_method_id.journal_id != receipt_journal:
    raise RuntimeError('Owner receipt profile differs; not changing it')
for field, key in [('arg_value_third_out_method_id','values_third_out_journal'), ('arg_value_own_out_method_id','values_own_journal')]:
    if company[field]:
        previous = env.ref('arg_demo.'+key, raise_if_not_found=False)
        if not previous or company[field].journal_id != previous:
            raise RuntimeError('An owner delivery profile is already configured; not replacing it')
models_to_preserve = ['account.move','account.payment','arg.pyme.treasury.document']
if 'stock.move' in env:
    models_to_preserve.append('stock.move')
counts = {name: env[name].search_count([('company_id','=',company.id)]) for name in models_to_preserve}
created = []


def example(model, key, values):
    record = env.ref('arg_demo.'+key, raise_if_not_found=False)
    if record:
        if record._name != model or ('company_id' in record._fields and record.company_id != company):
            raise RuntimeError('Fixture identity or company mismatch')
        return record
    record = env[model].create(values)
    env['ir.model.data'].create({'module':'arg_demo','name':key,'model':model,'res_id':record.id,'noupdate':True})
    created.append(key)
    return record


supplier = example('res.partner','values_supplier', {'name':'EJEMPLO · Proveedor cartera ARG','company_id':company.id})
bank = example('res.partner.bank','values_own_bank', {'account_number':'EJEMPLO-ARG-PROPIA-01',
    'bank_name':'BANCO PROPIO FICTICIO · EJEMPLO','partner_id':company.partner_id.id,'company_id':company.id})
if bank.partner_id != company.partner_id or bank.account_number != 'EJEMPLO-ARG-PROPIA-01':
    raise RuntimeError('Example bank record was customized; not overwriting it')
liability = example('account.account','values_own_liability', {'name':'Cheques propios pendientes · EJEMPLO ARG',
    'code':'ARGVAL002','account_type':'liability_current','reconcile':True,'company_ids':[Command.set(company.ids)]})
if company not in liability.company_ids or liability.account_type != 'liability_current' or not liability.reconcile:
    raise RuntimeError('Example liability was customized; not overwriting it')
profiles = {}
for key, code, title, account, bank_id in [
        ('values_third_out_journal','ARGT','Entrega de terceros · EJEMPLO ARG',portfolio,False),
        ('values_own_journal','ARGO','Banco propio · EJEMPLO ARG',liability,bank.id)]:
    vals = {'name':title,'code':code,'type':'bank','company_id':company.id}
    if bank_id:
        vals['bank_account_id'] = bank_id
    journal = example('account.journal',key,vals)
    if journal.type != 'bank' or journal.code != code or (bank_id and journal.bank_account_id.id != bank_id):
        raise RuntimeError('Example journal was customized; not overwriting it')
    method = journal.outbound_payment_method_line_ids.filtered(lambda m: m.code == 'manual')
    if len(method) != 1:
        raise RuntimeError('Example journal needs one manual outbound method')
    if method.payment_account_id and method.payment_account_id != account and key not in created:
        raise RuntimeError('Example method was customized; not overwriting it')
    if method.payment_account_id != account:
        method.write({'payment_account_id':account.id})
    profiles['arg_value_third_out_method_id' if not bank_id else 'arg_value_own_out_method_id'] = method.id
company.write(profiles)
today = fields.Date.context_today(env['arg.pyme.value.instrument'])
cheque = example('arg.pyme.value.instrument','values_own_cheque', {'company_id':company.id,'date':today,
    'partner_id':supplier.id,'beneficiary_id':supplier.id,'instrument_kind':'cheque','ownership':'own','support':'paper',
    'amount':100000,'currency_id':(company.arg_default_currency_id or company.currency_id).id,
    'bank_account_id':bank.id,'bank_name':bank.bank_name,'bank_identifier':'DEMO-OWN','issuer_account':bank.account_number,
    'instrument_number':'EJEMPLO-PROPIO-0001','issuer_id':company.partner_id.id,'issuer_identifier':False,
    'issued_on':today,'payable_on':today,'note':'DATOS FICTICIOS. Cheque propio de aprendizaje, sin entrega ni validez bancaria.'})
for model, count in counts.items():
    if env[model].search_count([('company_id','=',company.id)]) != count:
        raise RuntimeError('Unexpected ledger, treasury or stock effect')
env.cr.commit()
print('ARG_VALUES_DELIVERY_EXAMPLES='+json.dumps({'created_keys':created,'own_cheque_id':cheque.id,
    'number':cheque.arg_number,'state':cheque.state,'draft_created':'values_own_cheque' in created,
    'payments_created':0,'account_moves_created':0,'external_calls':0}))
