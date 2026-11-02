"""Sales review fixture, executed only in an explicitly isolated example database.

Run inside odoo shell with ARG_QA_SALES_ISOLATED=1 and ARG_QA_SALES_PHASE.
The network guard rejects a container with any interface besides loopback.
Creates fictitious documents only; never sends mail or requests fiscal authorization.
"""
import json
import os
import socket
from odoo import Command, fields
from odoo.exceptions import AccessError, UserError

assert os.environ.get('ARG_QA_SALES_ISOLATED') == '1'
assert {name for _, name in socket.if_nameindex()} == {'lo'}, 'This review requires an isolated container'
assert env.cr.dbname == 'arg_demo' and env.company.arg_demo_mode
assert not env['ir.cron'].search_count([('active', '=', True)])
assert not env['ir.mail_server'].search_count([('active', '=', True)])
PHASE = os.environ['ARG_QA_SALES_PHASE']
CASE = 'QA-VENTAS-20261102'
manager = env['res.users'].search([('login', '=', 'gonzalo')], limit=1)
assert manager and manager.has_group('arg_pyme_base.group_manager')
E = env['res.partner'].with_user(manager).with_company(env.company).env
customer = E.ref('arg_demo.customer_pyme')
quotes = E['arg.pyme.quotation']
quote = quotes.search([('arg_reference', '=', CASE)], limit=1)
result = {'phase': PHASE, 'case': CASE, 'isolated': True, 'business_user': manager.login}


def counts():
    return {model: E[model].search_count([]) for model in ('stock.move', 'stock.picking', 'account.move', 'account.payment')}


def expect_denied(label, operation):
    try:
        with E.cr.savepoint():
            operation()
    except (AccessError, UserError):
        result[label] = True
    else:
        raise AssertionError(label + ' was unexpectedly permitted')


def describe(record):
    return {'model': record._name, 'id': record.id, 'number': record.arg_number, 'state': record.state,
            'axes': record._arg_get_completion_axes()}


if PHASE == 'metadata':
    product = E.ref('arg_demo.product_a').product_variant_id
    result.update(company=E.company.name, currency=E.company.currency_id.name, counts=counts(),
                  product={'name': product.name, 'stockable': product.is_storable, 'unit': product.uom_id.name,
                           'invoice_policy': product.invoice_policy},
                  native_journals=E['account.journal'].search([('type', '=', 'sale')]).read(['name', 'code']))
elif PHASE == 'quote':
    if not quote:
        assert not quotes.search_count([]), 'Inspect existing review documents before creating another case'
        template = E.ref('arg_demo.product_a').copy({'name': 'Ejemplo QA — Producto de Ventas',
                                                   'default_code': CASE, 'invoice_policy': 'delivery'})
        quote = quotes.create({'partner_id': customer.id, 'arg_reference': CASE,
                               'line_ids': [Command.create({'product_id': template.product_variant_id.id,
                                                            'target_quantity_total': 2, 'price_unit': 10000})]})
        assert quote.arg_number.startswith('PRE-')
    if quote.state == 'draft':
        before = counts()
        quote.action_issue()
        operation = E['arg.pyme.quotation.operation'].browse(quote.action_accept_quantities()['res_id'])
        operation.action_apply()
        assert counts() == before, 'Accepting a quotation must not move stock or money'
    assert quote.state == 'confirmed' and quote.line_ids.accepted_target_total == 2
    expect_denied('accepted_line_locked', lambda: quote.line_ids.write({'price_unit': 999}))
    result.update(document=describe(quote), net=quote.amount_untaxed, tax=quote.amount_tax, total=quote.amount_total,
                  physical_and_financial_effects_unchanged=True)
elif PHASE == 'order':
    assert quote and quote.state == 'confirmed'
    order = quote.order_ids
    if not order:
        before = counts()
        operation = E['arg.pyme.quotation.operation'].browse(quote.action_generate_order()['res_id'])
        action = operation.action_apply();order = E['sale.order'].browse(action['res_id'])
        retry = operation.action_apply()
        assert retry['res_id'] == order.id and len(quote.order_ids) == 1
        assert counts() == before, 'Generating a draft order must not create stock/accounting effects'
        assert order.state == 'draft' and order.arg_number.startswith('PED-')
        assert order.arg_number != quote.arg_number
        assert order.arg_quotation_id == quote and order.order_line.arg_quotation_line_id == quote.line_ids
        result['retry_returns_same_order'] = True
    if order.state == 'draft':
        order.action_confirm()
    assert order.state == 'sale' and order.order_line.product_uom_qty == 2
    assert order.order_line.move_ids.picking_id and not order.invoice_ids
    expect_denied('derived_line_locked', lambda: order.order_line.write({'price_unit': 999}))
    result.update(quotation=describe(quote), document=describe(order),
                  physical_documents=[describe(p) for p in order.order_line.move_ids.picking_id])
elif PHASE == 'delivery':
    order = quote.order_ids
    assert len(order) == 1 and order.state == 'sale'
    line = order.order_line
    product = line.product_id
    picking = line.move_ids.picking_id.filtered(lambda p: not p.backorder_id)
    assert len(picking) == 1
    count = E['arg.pyme.inventory.count'].search([('arg_reference', '=', CASE)], limit=1)
    if not count:
        count = E['arg.pyme.inventory.count'].create({'location_id': picking.location_id.id,
            'reason': 'Apertura ficticia para revisión aislada de Ventas', 'arg_reference': CASE,
            'line_ids': [Command.create({'product_id':product.id})]})
        count.action_start()
        count.line_ids.write({'counted_quantity':10, 'counted':True})
        count.action_mark_counted(); count.action_apply()
    assert count.state == 'applied'
    if picking.state != 'done':
        picking.action_assign()
        picking.move_ids.write({'quantity':1, 'picked':True})
        action = picking.button_validate()
        if isinstance(action, dict) and action.get('res_model') == 'stock.backorder.confirmation':
            wizard = E[action['res_model']].with_context(action['context']).create({})
            wizard.process()
        else:
            assert action is True, str(action)
    assert picking.state == 'done' and line.qty_delivered == 1
    assert len(picking.backorder_ids) == 1 and picking.backorder_ids.state not in ('done','cancel')
    assert picking.backorder_ids.move_ids.product_uom_qty == 1
    assert not order.invoice_ids
    axes = order._arg_get_completion_axes()
    assert next(a for a in axes if a['label'] == 'Entrega')['state'] == 'partial'
    result.update(document=describe(picking), order=describe(order),
        backorder=describe(picking.backorder_ids), opening_inventory=describe(count),
        quantity_on_hand=product.qty_available, delivered=line.qty_delivered,
        invoices_created=0)
elif PHASE == 'invoice':
    order = quote.order_ids
    assert order.order_line.qty_delivered == 1
    before_stock = E['stock.move'].search_count([])
    journal = E['account.journal'].search([('code','=','QARG'),('company_id','=',E.company.id)],limit=1)
    if not journal:
        original = E['account.journal'].search([('type','=','sale'),('company_id','=',E.company.id)],limit=1)
        values = {'name':'Ejemplo QA — Ventas internas sin emisión fiscal','code':'QARG',
                  'type':'sale','company_id':E.company.id,'default_account_id':original.default_account_id.id}
        if 'l10n_latam_use_documents' in E['account.journal']._fields:
            values['l10n_latam_use_documents'] = False
        journal = E['account.journal'].create(values)
    order.write({'journal_id':journal.id})
    invoice = order.invoice_ids
    if not invoice:
        action = order.action_arg_invoice()
        wizard = E['sale.advance.payment.inv'].with_context(action['context']).create({})
        wizard.create_invoices()
        invoice = order.invoice_ids
    assert len(invoice) == 1 and invoice.journal_id == journal
    assert invoice.invoice_line_ids.filtered(lambda l:l.display_type=='product').quantity == 1
    assert invoice.arg_number.startswith('FAC-') and invoice.amount_total == 10000
    if invoice.state == 'draft':
        invoice.write({'invoice_date': fields.Date.context_today(invoice)})
        invoice.action_post()
    assert invoice.state == 'posted' and invoice.amount_residual == 10000
    assert E['stock.move'].search_count([]) == before_stock
    assert order.order_line.qty_delivered == 1 and order.order_line.qty_invoiced_posted == 1
    axes = order._arg_get_completion_axes()
    assert next(a for a in axes if a['label']=='Facturación del pedido')['state']=='partial'
    assert next(a for a in axes if a['label']=='Entrega')['state']=='partial'
    result.update(document=describe(invoice), order=describe(order), total=invoice.amount_total,
        residual=invoice.amount_residual, journal=journal.name, native_number=invoice.name,
        fiscal_emission=False, stock_moves_unchanged=True)
elif PHASE == 'checks':
    order = quote.order_ids;invoice = order.invoice_ids
    assert len(order)==1 and len(invoice)==1 and invoice.state=='posted'
    assert quote.line_ids.target_quantity_total==2 and quote.line_ids.accepted_target_total==2
    assert order.order_line.qty_delivered==1 and order.order_line.qty_invoiced_posted==1
    assert invoice.amount_residual==10000
    expect_denied('direct_quote_state_denied',lambda:quote.write({'state':'draft'}))
    expect_denied('direct_invoice_state_denied',lambda:invoice.write({'state':'draft'}))
    expect_denied('derived_quantity_locked',lambda:order.order_line.write({'product_uom_qty':9}))
    expect_denied('accepted_terms_locked',lambda:quote.line_ids.write({'price_unit':9}))
    expect_denied('invoice_evidence_locked',lambda:invoice.write({'arg_header_snapshot':{}}))
    assert not quotes.search_count([('arg_reference','=','Ejemplo visual ARG — sin guardar')])
    result.update(counts=counts(), figures={'ordered':2,'delivered':1,'invoiced':1,'pending_delivery':1,
        'pending_invoice':1,'receivable_ars':invoice.amount_residual}, visual_draft_not_persisted=True)
elif PHASE == 'reports':
    from datetime import timedelta
    order=quote.order_ids;invoice=order.invoice_ids
    rendered=[]
    for document in [quote,order,order.order_line.move_ids.picking_id.filtered(lambda p:not p.backorder_id),invoice]:
        report=E.ref('arg_pyme_documentos.action_report_document')
        data={'arg_model':document._name,'arg_ids':document.ids}
        payload=E['report.arg_pyme_documentos.document_report']._get_report_values(document.ids,data=data)
        assert payload['pages'][0]['demo'] and payload['pages'][0]['number']==document.arg_number
        html,_=report._render_qweb_html(report.report_name,document.ids,data=data)
        assert document.arg_number.encode() in html and b'No acredita' in html
        from lxml import html as lxml_html
        text = lxml_html.fromstring(html).text_content()
        page = payload['pages'][0]
        assert page['title'] in text and page['partner_name'] in text
        assert all(str(line['description']) in text and str(line['quantity']) in text for line in page['lines'])
        assert all(str(total['amount']) in text for total in page['totals'])
        assert 'DATOS DE EJEMPLO' in text
        rendered.append({'number':document.arg_number,'html_bytes':len(html),'demo_mark':True,
                         'header_lines_amounts':True})
    queries=[]
    for source,expected in [('sale_orders',2),('sales',1),('stock_now',9)]:
        query=E['arg.pyme.report.query'].create({'source':source,'product_query':CASE,
            'date_from':fields.Date.today()-timedelta(days=7),'date_to':fields.Date.today()+timedelta(days=1)})
        query.action_refresh()
        snapshot=E['arg.pyme.report.engine']._snapshot(query)
        assert snapshot['rows'] and sum(row['quantity'] for row in snapshot['rows'])==expected
        assert all(row['unit_rounding']==0.01 for row in snapshot['rows'])
        assert query.result_html and query.action_csv()['target']=='download'
        queries.append({'source':source,'source_count':snapshot['source_count'],'quantity':expected,'unit_rounding':0.01})
    result.update(document_html=rendered,fact_queries=queries,fiscal_emission=False)
else:
    raise RuntimeError('This review phase has not been prepared yet')

E.cr.commit()
print('ARG_QA_RESULT=' + json.dumps(result, ensure_ascii=False, default=str))
