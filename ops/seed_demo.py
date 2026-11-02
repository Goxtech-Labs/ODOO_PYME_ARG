"""Load identifiable, idempotent master examples through an Odoo shell.

Requires the isolated arg_demo database and ARG_DEMO_PASSWORD for initial access.
Creates no fiscal authorization, posted transaction, stock movement or external message.
Explicit private LOGIN, BASE_URL and ACK_EXAMPLES=1 are also required; no owner-specific URL/login.
"""
import json
import os
from urllib.parse import urlsplit
from odoo import Command

if env.cr.dbname != "arg_demo":
    raise RuntimeError("This fixture loader only accepts arg_demo")

password = os.environ.pop('ARG_DEMO_PASSWORD', None)
login = os.environ.pop('ARG_DEMO_LOGIN', None)
base_url = os.environ.pop('ARG_DEMO_BASE_URL', None)
if os.environ.pop('ARG_DEMO_ACK_EXAMPLES', None) != '1':
    raise RuntimeError('Explicit example-only initialization is required')
if not password or len(password) < 16 or not login or not base_url:
    raise RuntimeError('Provide private ARG_DEMO_PASSWORD (16+ characters), LOGIN and BASE_URL')
url = urlsplit(base_url)
if url.scheme not in ('http','https') or not url.hostname or url.username or url.password or url.query or url.fragment or url.path not in ('','/'):
    raise RuntimeError('BASE_URL must be the chosen instance origin without credentials or query')
for model in ['account.chart.template','stock.warehouse','product.pricelist']:
    if model not in env:
        raise RuntimeError('Full demo requires accounting, stock and price lists; use the services profile separately')
if env['res.company'].with_context(active_test=False).search_count([]) != 1:
    raise RuntimeError('Example initialization requires a fresh single-company database')
if not env['ir.module.module'].search_count([('name','=','l10n_ar'),('state','=','installed')]):
    raise RuntimeError('Install l10n_ar before initializing examples')
company = env.ref('base.main_company')
if company.chart_template and company.chart_template != 'ar_ri':
    raise RuntimeError('Existing chart differs from the example profile; refusing to overwrite configuration')
env = env(context=dict(env.context, allowed_company_ids=company.ids, default_company_id=company.id))
for model in ['account.move','account.payment','sale.order','purchase.order','stock.move','stock.picking','stock.quant','arg.pyme.treasury.document','arg.pyme.quotation','arg.pyme.inventory.count','arg.pyme.inventory.adjustment']:
    if model in env and env[model].with_context(active_test=False).search_count([]):
        raise RuntimeError('Business records exist; refusing to initialize example masters')

env = env(context=dict(env.context, tracking_disable=True, mail_notrack=True,
                       mail_create_nosubscribe=True, no_reset_password=True))
company = env.ref("base.main_company")
company.write({
    "name": "Ejemplo — Odoo Pymes ARG",
    "country_id": env.ref("base.ar").id,
    "currency_id": env.ref("base.ARS").id,
    "vat": False,
    **({"arg_demo_mode": True} if "arg_demo_mode" in company._fields else {}),
    **({"arg_default_currency_id": env.ref("base.ARS").id} if "arg_default_currency_id" in company._fields else {}),
})
if not company.chart_template:
    env["account.chart.template"].try_loading("ar_ri", company, install_demo=False)

def example(model, key, values, module="arg_demo"):
    external_id = module + "." + key
    record = env.ref(external_id, raise_if_not_found=False)
    if record:
        if record._name != model:
            raise RuntimeError("Fixture key/model mismatch")
        return record
    record = env[model].create(values)
    env["ir.model.data"].create({"module": module, "name": key,
                                 "model": model, "res_id": record.id,
                                 "noupdate": True})
    return record

pricelist_module = 'arg_pyme_catalogo' if 'arg.pyme.price.change.batch' in env else 'arg_demo'
pricelist = example('product.pricelist', 'demo_pricelist', {'name':'Ejemplo — Lista general ARG',
    'currency_id':env.ref('base.ARS').id, 'company_id':company.id}, module=pricelist_module)
if pricelist.currency_id != company.currency_id or pricelist.company_id != company:
    raise RuntimeError('Existing example price list was customized; not overwriting it')

partners = []
for key, name, role in [
    ("customer_retail", "Ejemplo — Cliente Mostrador", "customer"),
    ("customer_pyme", "Ejemplo — Cliente Pyme", "customer"),
    ("supplier_general", "Ejemplo — Proveedor General", "supplier"),
]:
    values = {"name": name, "country_id": env.ref("base.ar").id,
              "email": key + "@example.invalid", "vat": False,
              "comment": "Dato de ejemplo ARG. Sin identidad fiscal real."}
    rank = "customer_rank" if role == "customer" else "supplier_rank"
    if rank in env["res.partner"]._fields:
        values[rank] = 1
    if 'arg_role_ids' in env['res.partner']._fields:
        role_record = env.ref('arg_pyme_terceros.role_' + role)
        values['arg_role_ids'] = [Command.link(role_record.id)]
    if 'arg_currency_id' in env['res.partner']._fields:
        values['arg_currency_id'] = company.currency_id.id
    if role == 'customer' and 'property_product_pricelist' in env['res.partner']._fields:
        values['property_product_pricelist'] = pricelist.id
    if role == 'supplier' and 'property_purchase_currency_id' in env['res.partner']._fields:
        values['property_purchase_currency_id'] = company.currency_id.id
    partners.append(example("res.partner", key, values))

products = []
for key, name, price, cost, service in [
    ("product_a", "Ejemplo — Producto A", 10000.0, 6000.0, False),
    ("product_b", "Ejemplo — Producto B", 20000.0, 12000.0, False),
    ("service_a", "Ejemplo — Servicio A", 15000.0, 0.0, True),
]:
    values = {"name": name, "default_code": "EJ-" + key.upper(),
              "type": "service" if service else "consu",
              "list_price": price, "standard_price": cost,
              "sale_ok": True, "purchase_ok": True,
              "description": "Ejemplo ARG. Importes ficticios en ARS."}
    if not service and "is_storable" in env["product.template"]._fields:
        values["is_storable"] = True
    products.append(example("product.template", key, values))

warehouse = env["stock.warehouse"].search([("company_id", "=", company.id)], limit=1)
if warehouse:
    warehouse.write({"name": "Ejemplo — Depósito Principal", "code": "DEMO"})

env["res.lang"]._activate_lang("es_AR")
admin = env.ref("base.user_admin")
admin.write({"login": login, "password": password,
             "name": "Administrador — Entorno de ejemplo", "email": "admin@example.invalid",
             "lang": "es_AR", "tz": "America/Argentina/Cordoba"})
for key, value in {
    "web.base.url": base_url.rstrip("/"),
    "web.base.url.freeze": True,
    "auth_signup.invitation_scope": "b2b",
    "auth_signup.reset_password": False,
}.items():
    params = env["ir.config_parameter"].sudo()
    if isinstance(value, bool):
        params.set_bool(key, value)
    else:
        params.set_str(key, value)
env["ir.cron"].with_context(active_test=False).search([]).write({"active": False})
env["ir.mail_server"].with_context(active_test=False).search([]).write({"active": False})
env.cr.commit()
print(json.dumps({"database": env.cr.dbname, "company": company.name,
                  "partners": len(partners), "products": len(products),
                  "posted_documents_created": 0, "stock_moves_created": 0,
                  "external_messages_sent": 0}, ensure_ascii=False))
