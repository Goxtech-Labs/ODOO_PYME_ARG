import hashlib
import json
import math
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str, separators=(',', ':')).encode()).hexdigest()


def _touch_pricelists(records):
    """Audit invalidation, not a price ledger. Effective UPDATE serializes RR requests."""
    if not records:
        return
    records.check_access('write')
    records.flush_recordset(['write_date', 'write_uid'])
    for record in records.sorted('id'):
        records.env.cr.execute('UPDATE product_pricelist SET write_date=clock_timestamp(), write_uid=%s WHERE id=%s',
                               [records.env.uid, record.id])
    records.invalidate_recordset(['write_date', 'write_uid'])


class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.model_create_multi
    def create(self, vals_list):
        # Mark before native writes, taking parents in stable order.
        self.check_access('create')
        ids = {v.get('pricelist_id') or self.env.context.get('default_pricelist_id') for v in vals_list}
        _touch_pricelists(self.env['product.pricelist'].browse(sorted(i for i in ids if i)))
        return super().create(vals_list)

    def write(self, values):
        self.check_access('write')
        parents = self.pricelist_id
        if values.get('pricelist_id'):
            parents |= self.env['product.pricelist'].browse(values['pricelist_id'])
        _touch_pricelists(parents)
        return super().write(values)

    def unlink(self):
        self.check_access('unlink')
        _touch_pricelists(self.pricelist_id)
        return super().unlink()


class PriceChangeBatch(models.Model):
    _name = 'arg.pyme.price.change.batch'
    _description = 'Registro de cambios de precios ARG'
    _order = 'id desc'
    company_id = fields.Many2one('res.company', required=True, index=True)
    user_id = fields.Many2one('res.users', required=True)
    operation_key = fields.Char(required=True, index=True)
    payload_hash = fields.Char(required=True)
    changes = fields.Json(required=True)
    _operation_unique = models.Constraint('UNIQUE(company_id,user_id,operation_key)', 'La operación de precios ya está registrada.')

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.su:
            raise AccessError(_('Este registro sólo se crea al aplicar precios autorizados.'))
        return super().create(vals_list)

    def write(self, values):
        raise UserError(_('El registro de cambios es inmutable.'))

    def unlink(self):
        raise UserError(_('El registro de cambios se conserva.'))


class PricelistMatrix(models.AbstractModel):
    _name = 'arg.pyme.pricelist.matrix'
    _description = 'Matriz de precios ARG'

    @api.model
    def _authorize(self, edit=False):
        group = 'arg_pyme_base.group_manager' if edit else 'arg_pyme_base.group_operator'
        if not self.env.user.has_group(group) or self.env.user.share:
            raise AccessError(_('No tiene permiso para esta operación de precios.'))

    @api.model
    def _pricelists(self, ids, limit=5):
        if not isinstance(ids, list) or not ids or len(ids) > limit or any(type(i) is not int or i <= 0 for i in ids):
            raise ValidationError(_('Seleccione entre una y cinco listas.'))
        records = self.env['product.pricelist'].browse(ids).exists()
        records.check_access('read')
        if len(records) != len(set(ids)) or any(not r.active or (r.company_id and r.company_id != self.env.company) for r in records):
            raise AccessError(_('Lista no disponible para la compañía actual.'))
        return records

    @api.model
    def options(self):
        self._authorize()
        lists = self.env['product.pricelist'].search([('company_id', 'in', [False, self.env.company.id])], order='name,id', limit=200)
        categories = self.env['product.category'].search([], order='name,id', limit=200)
        return {'lists': [{'id': p.id, 'name': p.name, 'currency': p.currency_id.name} for p in lists],
                'categories': [{'id': c.id, 'name': c.display_name} for c in categories],
                'can_edit': self.env.user.has_group('arg_pyme_base.group_manager'),
                'date': str(fields.Date.context_today(self))}

    @api.model
    def _cell(self, product, pricelist, when, quantity, version=None, product_version=None, template_version=None):
        quantity = float(quantity)
        price, rule_id = pricelist._get_product_price_rule(product, quantity, date=when, uom=product.uom_id)
        rule = self.env['product.pricelist.item'].browse(rule_id)
        try:
            self._require_rule_rates(product,pricelist,rule,when,quantity,set())
        except UserError as error:
            return {'price':None,'token':False,'editable':False,'reason':str(error),'rule_id':rule.id or False}
        editable = not rule or (rule.compute_price == 'fixed' and rule.applied_on == '0_product_variant'
                   and rule.product_id == product and not rule.date_start and not rule.date_end
                   and not rule.uom_id and rule.min_quantity == 0)
        current_date = fields.Date.context_today(self)
        editable = editable and quantity == 1 and when.date() == current_date
        values = [product.id, str(product.write_date) if product_version is None else product_version,
                  str(product.product_tmpl_id.write_date) if template_version is None else template_version,
                  pricelist.id, str(pricelist.write_date) if version is None else version,
                  rule.id, str(rule.write_date) if rule else '', product.uom_id.id,
                  pricelist.currency_id.id, str(when), quantity, price]
        return {'price': price, 'token': _digest(values), 'editable': bool(editable),
                'reason': '' if editable else _('Regla avanzada o consulta fuera de una unidad/hoy. Editar desde Listas y reglas.'),
                'rule_id': rule.id or False}

    @api.model
    def _require_rule_rates(self,product,pricelist,rule,when,quantity,seen):
        if pricelist.id in seen:raise UserError(_('Revise las dependencias entre listas.'))
        seen.add(pricelist.id)
        if rule and rule.compute_price=='fixed':
            extra=(rule.env.context.get('no_variant_attributes_price_extra',0)
                   if rule.applied_on=='0_product_variant' else product._get_attributes_extra_price())
            if extra:
                product.currency_id._arg_require_conversion(pricelist.currency_id,self.env.company,when.date())
            return
        if rule and rule.base=='pricelist':
            base=rule.base_pricelist_id
            base.currency_id._arg_require_conversion(pricelist.currency_id,self.env.company,when.date())
            _,rule_id=base._get_product_price_rule(product,quantity,date=when,uom=product.uom_id)
            return self._require_rule_rates(product,base,self.env['product.pricelist.item'].browse(rule_id),when,quantity,seen)
        currency=product.cost_currency_id if rule and rule.base=='standard_price' else product.currency_id
        currency._arg_require_conversion(pricelist.currency_id,self.env.company,when.date())

    @api.model
    def page(self, list_ids, filters=None, offset=0, quantity=1, date=None):
        self._authorize()
        lists = self._pricelists(list_ids)
        filters = filters or {}
        if not isinstance(filters, dict) or type(offset) is not int or offset < 0:
            raise ValidationError(_('Filtros o página no válidos.'))
        quantity = float(quantity)
        if not math.isfinite(quantity) or quantity <= 0:
            raise ValidationError(_('La cantidad debe ser positiva.'))
        day = fields.Date.to_date(date) if date else fields.Date.context_today(self)
        when = fields.Datetime.to_datetime(day)
        domain = [('company_id', 'in', [False, self.env.company.id])]
        query = str(filters.get('query') or '').strip()[:120]
        if query:
            domain += ['|', ('name', 'ilike', query), ('default_code', 'ilike', query)]
        if filters.get('kind') in ('consu', 'service'):
            domain.append(('type', '=', filters['kind']))
        if filters.get('sale'): domain.append(('sale_ok', '=', True))
        if filters.get('purchase'): domain.append(('purchase_ok', '=', True))
        if filters.get('category'): domain.append(('categ_id', 'child_of', int(filters['category'])))
        products = self.env['product.product'].search(domain, limit=30, offset=offset, order='default_code,id')
        count = self.env['product.product'].search_count(domain)
        rows = []
        for product in products:
            cells = {str(p.id): self._cell(product, p, when, quantity) for p in lists}
            row = {'id': product.id, 'name': product.display_name, 'code': product.default_code or '',
                   'unit': product.uom_id.display_name, 'type': product.type, 'cells': cells}
            if self.env.user.has_group('arg_pyme_base.group_manager'):
                cost = product.standard_price
                cost_currency = product.cost_currency_id
                row.update(cost=cost, cost_currency=cost_currency.name)
                for p in lists:
                    sale = cells[str(p.id)]['price']
                    try:
                        cost_currency._arg_require_conversion(p.currency_id,self.env.company,day)
                        converted = cost_currency._convert(cost,p.currency_id,self.env.company,day,round=False)
                    except UserError:
                        converted=None
                    cells[str(p.id)].update(cost=converted,margin=(sale-converted)/sale*100 if sale and converted is not None else None)
            rows.append(row)
        return {'rows': rows, 'count': count, 'offset': offset, 'limit': 30,
                'columns': [{'id': p.id, 'name': p.name, 'currency': p.currency_id.name} for p in lists],
                'date': str(day), 'quantity': quantity}

    @api.model
    def apply(self, operation_key, changes):
        self._authorize(edit=True)
        if not isinstance(operation_key, str) or not 16 <= len(operation_key) <= 80:
            raise ValidationError(_('Falta una clave de operación válida.'))
        if not isinstance(changes, list) or not changes or len(changes) > 500:
            raise ValidationError(_('Revise entre uno y quinientos cambios por guardado.'))
        normalized = []
        for value in changes:
            if not isinstance(value, dict): raise ValidationError(_('Cambio no válido.'))
            product_id, list_id = value.get('product_id'), value.get('list_id')
            token, date = value.get('token'), value.get('date')
            amount = value.get('price')
            if type(product_id) is not int or type(list_id) is not int or not isinstance(token, str) or len(token) != 64:
                raise ValidationError(_('La referencia del cambio no es válida.'))
            if type(amount) not in (int, float) or not math.isfinite(amount) or amount < 0:
                raise ValidationError(_('El precio debe ser un número no negativo.'))
            normalized.append({'product_id': product_id, 'list_id': list_id, 'token': token, 'date': date, 'price': amount})
        if len({(c['product_id'], c['list_id']) for c in normalized}) != len(normalized):
            raise ValidationError(_('Una celda sólo puede aparecer una vez.'))
        normalized.sort(key=lambda c: (c['list_id'], c['product_id']))
        payload_hash = _digest(normalized)
        # Authorize native records before the narrow technical audit access below.
        lists = self._pricelists(sorted({c['list_id'] for c in normalized}), limit=500)
        lists.check_access('write')
        products = self.env['product.product'].browse(sorted({c['product_id'] for c in normalized})).exists()
        products.check_access('read')
        if len(products) != len({c['product_id'] for c in normalized}) or any(not p.active or (p.company_id and p.company_id != self.env.company) for p in products):
            raise AccessError(_('Producto no disponible para la compañía actual.'))
        items = self.env['product.pricelist.item']
        items.check_access('create')
        versions = {p.id: str(p.write_date) for p in lists}
        product_versions = {p.id: str(p.write_date) for p in products}
        templates = products.product_tmpl_id
        template_versions = {p.id: str(p.write_date) for p in templates}
        _touch_pricelists(lists)
        # Concurrent native catalogue edits also invalidate the snapshot, including new rules on unchanged prices.
        from odoo.tools import SQL
        for records in (templates, products):
            records.check_access('write')
            records.flush_recordset(['write_date', 'write_uid'])
            for record in records.sorted('id'):
                self.env.cr.execute(SQL('UPDATE %s SET write_date=clock_timestamp(), write_uid=%s WHERE id=%s',
                    SQL.identifier(record._table), self.env.uid, record.id))
            records.invalidate_recordset(['write_date', 'write_uid'])
        audit = self.env['arg.pyme.price.change.batch'].sudo()
        prior = audit.search([('company_id', '=', self.env.company.id), ('user_id', '=', self.env.uid), ('operation_key', '=', operation_key)], limit=1)
        if prior:
            if prior.payload_hash != payload_hash: raise ValidationError(_('Esta clave corresponde a otros cambios.'))
            return {'batch_id': prior.id, 'count': len(prior.changes), 'replayed': True}
        pmap = {p.id: p for p in products}; lmap = {p.id: p for p in lists}
        prepared = []
        today = fields.Date.context_today(self)
        for change in normalized:
            if change['date'] != str(today): raise UserError(_('Cambió la fecha de la consulta. Recargue y revise los cambios.'))
            p, pl = pmap[change['product_id']], lmap[change['list_id']]
            cell = self._cell(p, pl, fields.Datetime.to_datetime(today), 1, version=versions[pl.id],
                              product_version=product_versions[p.id], template_version=template_versions[p.product_tmpl_id.id])
            if cell['token'] != change['token'] or not cell['editable']:
                raise UserError(_('Cambió un precio o su regla. No se guardó ningún cambio. Recargue y revise la matriz.'))
            rule = items.browse(cell['rule_id'])
            if rule: rule.check_access('write')
            prepared.append((p, pl, rule, cell['price'], change['price']))
        records = []
        for product, pl, rule, before, after in prepared:
            if rule: rule.write({'fixed_price': after})
            else: items.create({'pricelist_id': pl.id, 'product_id': product.id,
                              'applied_on': '0_product_variant', 'compute_price': 'fixed',
                              'fixed_price': after, 'min_quantity': 0})
            records.append({'product_id': product.id, 'list_id': pl.id, 'currency_id': pl.currency_id.id,
                            'unit_id': product.uom_id.id, 'before': before, 'after': after})
        batch = audit.create({'company_id': self.env.company.id, 'user_id': self.env.uid,
                              'operation_key': operation_key, 'payload_hash': payload_hash, 'changes': records})
        return {'batch_id': batch.id, 'count': len(records), 'replayed': False}
