"""Replenishment configuration and paginated references, without procurement.

    The proposal/execution layer is a separate part of this service. None of
    these entry points calls native replenishment actions or a scheduler.
"""
import math
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Domain

from ..tools.replenishment import json_hash


_CONFIG_FIELDS = frozenset({
    'product_id', 'warehouse_id', 'location_id',
    'product_min_qty', 'product_max_qty', 'route_id', 'replenishment_uom_id',
})
_RELATIONS = {
    'product_id': 'product.product', 'warehouse_id': 'stock.warehouse',
    'location_id': 'stock.location', 'route_id': 'stock.route',
    'replenishment_uom_id': 'uom.uom',
}


class ReplenishmentRule(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    def _arg_lock_configuration(self):
        self.check_access('write')
        for rule in self.sorted('id'):
            rule.check_field_access(rule._fields['company_id'], 'read')
            if rule.company_id != self.env.company:
                raise AccessError(_('La regla debe pertenecer a la compañía actual.'))
            rule.flush_recordset(['write_date', 'write_uid'])
            self.env.cr.execute(
                'UPDATE stock_warehouse_orderpoint '
                'SET write_date=clock_timestamp(),write_uid=%s WHERE id=%s RETURNING id',
                [self.env.uid, rule.id],
            )
            if not self.env.cr.fetchone():
                raise UserError(_('La regla ya no está disponible. Volvé a consultar.'))
            rule.invalidate_recordset()


class Replenishment(models.AbstractModel):
    _name = 'arg.pyme.replenishment'
    _description = 'Reposición ARG'

    def _extension_specs(self):
        """Optional adapters own their native fields and selector semantics."""
        return {}

    def _config_relations(self):
        return {**_RELATIONS, **{spec['field']: spec['model']
                                for spec in self._extension_specs().values()}}

    def _extension_domain(self, kind, product, query):
        raise ValidationError(_('La opción de reposición no está disponible.'))

    def _extension_label(self, kind, record):
        raise ValidationError(_('La opción de reposición no está disponible.'))

    def _validate_extension(self, kind, record, product):
        template = self._get(product, 'product_tmpl_id')
        self._record('product.template', template.id)
        target_template = self._get(record, 'product_tmpl_id')
        target_product = self._get(record, 'product_id')
        if target_template != template or (target_product and target_product != product):
            raise ValidationError(_('La opción de abastecimiento no corresponde al producto.'))
        if record._name == 'mrp.bom' and self._get(record, 'type') != 'normal':
            raise ValidationError(_('Elegí una lista de materiales de fabricación normal.'))
        self._extension_label(kind, record)

    def _extension_relation(self, rule, kind, spec):
        try:
            target = self._get(rule, spec['field'])
            if not target:
                return {'id': False, 'name': _('Sin especificar'), 'status': 'unset'}
            self._record(spec['model'], target.id)
            return {'id': target.id, 'name': self._extension_label(kind, target), 'status': 'known'}
        except AccessError:
            return {'id': False, 'name': _('No determinado por permisos'), 'status': 'unknown'}

    def _scoped(self):
        service = self.with_user(self.env.uid).sudo(False).with_context({
            'allowed_company_ids': [self.env.company.id],
            'lang': self.env.context.get('lang'),
            'tz': self.env.context.get('tz'),
            'active_test': True,
        })
        service.env['arg.pyme.stock.matrix']._authorize()
        return service

    def _manager(self):
        if not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Configurar reposición requiere responsable ARG.'))

    def _identifier(self, value):
        if type(value) is not int or value <= 0:
            raise ValidationError(_('Elegí una referencia válida.'))
        return value

    def _offset(self, value):
        if type(value) is not int or value < 0:
            raise ValidationError(_('Página no válida.'))
        return value

    def _optional_id(self, value):
        return False if value is False or value is None else self._identifier(value)

    def _record(self, model, identifier, active=False):
        self._identifier(identifier)
        record = self.env[model].browse(identifier)
        try:
            record.check_access('read')
            if not record.exists():
                raise AccessError(_('Referencia no disponible.'))
            if 'company_id' in record._fields:
                record.check_field_access(record._fields['company_id'], 'read')
                if record.company_id and record.company_id != self.env.company:
                    raise AccessError(_('Compañía no disponible.'))
            if active and 'active' in record._fields:
                record.check_field_access(record._fields['active'], 'read')
                if not record.active:
                    raise AccessError(_('Referencia archivada.'))
        except AccessError:
            raise AccessError(_('La referencia no está disponible con sus permisos actuales.')) from None
        return record

    def _get(self, record, name):
        record.check_field_access(record._fields[name], 'read')
        return record[name]

    def _label(self, record):
        record.check_access('read')
        names = ['display_name']
        if record._name in ('product.product', 'product.template'):
            names += ['name', 'default_code']
        for name in names:
            record.check_field_access(record._fields[name], 'read')
        return record.display_name

    def _relation(self, record, name):
        try:
            target = self._get(record, name)
            if not target:
                return {'id': False, 'name': _('Sin especificar'), 'status': 'unset'}
            self._record(target._name, target.id)
            return {'id': target.id, 'name': self._label(target), 'status': 'known'}
        except AccessError:
            return {'id': False, 'name': _('No determinado por permisos'), 'status': 'unknown'}

    def _number(self, value):
        if type(value) not in (int, float):
            raise ValidationError(_('Ingresá mínimos y máximos numéricos.'))
        try:
            result = float(value)
        except (OverflowError, ValueError):
            raise ValidationError(_('La cantidad está fuera del rango admitido.')) from None
        if not math.isfinite(result):
            raise ValidationError(_('Las cantidades deben ser finitas.'))
        return result

    def _configuration(self, rule):
        rule.check_access('read')
        unit = self._relation(rule, 'uom_id')
        known = unit['status'] == 'known'
        minimum = self._number(self._get(rule, 'product_min_qty')) if known else None
        maximum = self._number(self._get(rule, 'product_max_qty')) if known else None
        return {
            'id': rule.id, 'name': self._get(rule, 'name'),
            'product': self._relation(rule, 'product_id'),
            'unit': unit,
            'warehouse': self._relation(rule, 'warehouse_id'),
            'location': self._relation(rule, 'location_id'),
            'minimum': minimum, 'maximum': maximum,
            'bounds_status': 'known' if known else 'unknown',
            'trigger': self._get(rule, 'trigger'),
            'active': self._get(rule, 'active'),
            'token': self._configuration_token(rule),
            'route': self._relation(rule, 'route_id'),
            'multiple': self._relation(rule, 'replenishment_uom_id'),
            'extensions': {kind: self._extension_relation(rule, kind, spec)
                           for kind, spec in self._extension_specs().items()},
            'can_edit': self.env.user.has_group('arg_pyme_base.group_manager') and rule.has_access('write'),
        }

    def _configuration_token(self, rule):
        stamp = self._get(rule, 'write_date')
        return json_hash({'id': rule.id, 'stamp': stamp.isoformat() if stamp else False})

    def _visible_domain(self, warehouse_id=False, product_id=False, query=''):
        # Queries stay in SQL and already carry target ACL/record rules. Do not
        # materialize a whole catalog, or rely on many2one display-name sudo.
        products = Domain('company_id', 'in', [False, self.env.company.id])
        if query:
            model = self.env['product.product']
            for name in ['name', 'default_code']:
                model.check_field_access(model._fields[name], 'read')
            products &= Domain('name', 'ilike', query) | Domain('default_code', 'ilike', query)
        if product_id:
            self._record('product.product', product_id)
            products &= Domain('id', '=', product_id)
        domain = Domain('company_id', '=', self.env.company.id)
        domain &= Domain('product_id', 'in', self.env['product.product']._search(products))
        domain &= Domain('warehouse_id', 'in', self.env['stock.warehouse']._search([
            ('company_id', '=', self.env.company.id),
        ]))
        domain &= Domain('location_id', 'in', self.env['stock.location']._search([
            ('company_id', 'in', [False, self.env.company.id]), ('usage', '=', 'internal'),
        ]))
        if warehouse_id:
            self._record('stock.warehouse', warehouse_id)
            domain &= Domain('warehouse_id', '=', warehouse_id)
        return domain

    @api.model
    @api.readonly
    def options(self):
        service = self._scoped()
        rules = service.env['stock.warehouse.orderpoint']
        manager = service.env.user.has_group('arg_pyme_base.group_manager')
        return {
            'company': service._label(service.env.company),
            'as_of': fields.Datetime.to_string(fields.Datetime.now()),
            'can_create': manager and rules.has_access('create'),
            'can_write': manager and rules.has_access('write'),
            'extensions': [{'kind': kind, 'field': spec['field'], 'label': spec['label']}
                           for kind, spec in service._extension_specs().items()],
            'horizon': service._horizon_configuration(),
        }

    def _horizon_configuration(self):
        company = self._record('res.company', self.env.company.id)
        try:
            days = self._get(company, 'horizon_days')
            token = self._get(company, 'write_date')
        except AccessError:
            return {'days': None, 'status': 'unknown', 'can_edit': False, 'token': False}
        return {'days': days, 'status': 'known',
                'token': json_hash({'company': company.id, 'stamp': token.isoformat() if token else False}),
                'can_edit': self.env.user.has_group('arg_pyme_base.group_manager') and company.has_access('write')}

    @api.model
    def save_horizon(self, days, expected_token):
        service = self._scoped()
        service._manager()
        if type(days) is not int or not 0 <= days <= 2147483647:
            raise ValidationError(_('Ingresá una cantidad entera de días mayor o igual a cero.'))
        try:
            fields.Date.today() + timedelta(days=days)
        except OverflowError:
            raise ValidationError(_('El horizonte supera el rango de fechas admitido.')) from None
        previous = service._horizon_configuration()
        if not previous['can_edit']:
            raise AccessError(_('Modificar el horizonte requiere permiso de edición de la compañía.'))
        if not isinstance(expected_token, str) or expected_token != previous['token']:
            raise UserError(_('La compañía cambió desde la consulta. Volvé a consultar el horizonte antes de guardarlo.'))
        company = service.env.company
        company.check_access('write')
        company.check_field_access(company._fields['horizon_days'], 'write')
        company.flush_recordset(['write_date', 'write_uid'])
        service.env.cr.execute('UPDATE res_company SET write_date=clock_timestamp(),write_uid=%s WHERE id=%s RETURNING id',
                               [service.env.uid, company.id])
        if not service.env.cr.fetchone():
            raise UserError(_('La compañía ya no está disponible.'))
        company.invalidate_recordset()
        if days != service._get(company, 'horizon_days'):
            company.write({'horizon_days': days})
        return {'horizon': service._horizon_configuration(),
                'message': _('Horizonte actualizado para todas las reglas de la compañía. No se generó abastecimiento.')}

    @api.model
    @api.readonly
    def extension_choices(self, kind, product_id, query='', offset=0):
        service = self._scoped()
        service._manager()
        service._offset(offset)
        specs = service._extension_specs()
        if not isinstance(kind, str) or kind not in specs:
            raise ValidationError(_('La opción de reposición no está disponible.'))
        if not isinstance(query, str) or len(query) > 120:
            raise ValidationError(_('La búsqueda admite hasta120 caracteres.'))
        product = service._record('product.product', product_id, active=True)
        if not service._get(product, 'is_storable'):
            raise ValidationError(_('Elegí un producto con control de existencias.'))
        spec = specs[kind]
        model = service.env[spec['model']]
        domain = service._extension_domain(kind, product, query.strip())
        rows = model.search(domain, limit=30, offset=offset, order='id')
        return {'offset': offset, 'count': model.search_count(domain),
                'rows': [{'id': row.id, 'name': service._extension_label(kind, row)} for row in rows]}

    @api.model
    @api.readonly
    def extension_reference(self, kind, identifier, product_id):
        service = self._scoped()
        service._manager()
        specs = service._extension_specs()
        if not isinstance(kind, str) or kind not in specs:
            raise ValidationError(_('La opción de reposición no está disponible.'))
        product = service._record('product.product', product_id, active=True)
        record = service._record(specs[kind]['model'], identifier, active=True)
        service._validate_extension(kind, record, product)
        return {'id': record.id, 'name': service._extension_label(kind, record), 'status': 'known'}

    @api.model
    @api.readonly
    def page(self, warehouse_id=False, product_id=False, query='', offset=0):
        service = self._scoped()
        service._offset(offset)
        warehouse_id = service._optional_id(warehouse_id)
        product_id = service._optional_id(product_id)
        if not isinstance(query, str) or len(query) > 120:
            raise ValidationError(_('La búsqueda admite hasta120 caracteres.'))
        domain = service._visible_domain(warehouse_id, product_id, query.strip())
        model = service.env['stock.warehouse.orderpoint']
        records = model.search(domain, limit=30, offset=offset, order='location_id,product_id,id')
        return {
            'company': service._label(service.env.company),
            'as_of': fields.Datetime.to_string(fields.Datetime.now()),
            'offset': offset, 'count': model.search_count(domain),
            'rows': [service._configuration(rule) for rule in records],
        }

    @api.model
    @api.readonly
    def choices(self, kind, query='', offset=0, warehouse_id=False):
        service = self._scoped()
        service._offset(offset)
        warehouse_id = service._optional_id(warehouse_id)
        if not isinstance(query, str) or len(query) > 120:
            raise ValidationError(_('La búsqueda admite hasta120 caracteres.'))
        models_by_kind = {
            'product': 'product.product', 'warehouse': 'stock.warehouse',
            'location': 'stock.location', 'route': 'stock.route',
        }
        if not isinstance(kind, str) or kind not in models_by_kind:
            raise ValidationError(_('Selector no válido.'))
        model = service.env[models_by_kind[kind]]
        domain = Domain('company_id', 'in', [False, service.env.company.id])
        if kind == 'warehouse':
            domain = Domain('company_id', '=', service.env.company.id)
        if kind == 'product':
            domain &= Domain('is_storable', '=', True)
        if kind == 'location':
            domain &= Domain('usage', '=', 'internal')
            if warehouse_id:
                warehouse = service._record('stock.warehouse', warehouse_id)
                view = service._get(warehouse, 'view_location_id')
                service._record('stock.location', view.id)
                domain &= Domain('id', 'child_of', view.id)
        if query.strip():
            model.check_field_access(model._fields['name'], 'read')
            names = Domain('name', 'ilike', query.strip())
            if kind == 'product':
                model.check_field_access(model._fields['default_code'], 'read')
                names |= Domain('default_code', 'ilike', query.strip())
            domain &= names
        rows = model.search(domain, limit=30, offset=offset, order='name,id')
        return {'offset': offset, 'count': model.search_count(domain),
                'rows': [{'id': row.id, 'name': service._label(row)} for row in rows]}

    @api.model
    @api.readonly
    def reference(self, kind, identifier):
        service = self._scoped()
        models_by_kind = {
            'product': 'product.product', 'warehouse': 'stock.warehouse',
            'location': 'stock.location', 'route': 'stock.route', 'unit': 'uom.uom',
        }
        if not isinstance(kind, str) or kind not in models_by_kind:
            raise ValidationError(_('Selector no válido.'))
        record = service._record(models_by_kind[kind], identifier)
        result = {'id': record.id, 'name': service._label(record)}
        if kind == 'product':
            result['unit'] = service._relation(record, 'uom_id')
        if kind == 'warehouse':
            result['default_location'] = service._relation(record, 'lot_stock_id')
        return result

    def _proposed_configuration(self, values, rule):
        proposed_values = {'company_id': self.env.company.id, **values}
        if rule:
            for name in ['route_id', 'supplier_id', 'bom_id']:
                if name in rule._fields and name not in proposed_values:
                    target = self._get(rule, name)
                    if target:
                        self._record(target._name, target.id)
                    proposed_values[name] = target.id
        # purchase_stock/MRP route inverses clear explicit vendor/BOM when an
        # existing route is removed. Simulate the configuration actually saved,
        # not the previous explicit selection, for native multiple choices.
        clears_route = ('route_id' in values and not values['route_id']
                        and (not rule or bool(self._get(rule, 'route_id'))))
        if clears_route:
            for name in ['supplier_id', 'bom_id']:
                if name in self.env['stock.warehouse.orderpoint']._fields:
                    proposed_values[name] = False
        return self.env['stock.warehouse.orderpoint'].new(proposed_values)

    @api.model
    @api.readonly
    def multiple_choices(self, values, rule_id=False, query='', offset=0):
        service = self._scoped()
        service._manager()
        service._offset(offset)
        rule_id = service._optional_id(rule_id)
        if not isinstance(query, str) or len(query) > 120:
            raise ValidationError(_('La búsqueda admite hasta120 caracteres.'))
        if not isinstance(values, dict):
            raise ValidationError(_('La configuración contiene campos no admitidos.'))
        model = service.env['stock.warehouse.orderpoint']
        rule = service._record(model._name, rule_id, active=True) if rule_id else model
        rule.check_access('write' if rule else 'create')
        # Validate the proposed dimensions but do not require the previous
        # multiple to remain valid while choosing its replacement.
        prepared = service._save_values({**values, 'replenishment_uom_id': False}, rule)
        proposed = service._proposed_configuration(prepared, rule)
        allowed = service._get(proposed, 'allowed_replenishment_uom_ids')
        units = service.env['uom.uom']
        domain = Domain('id', 'in', allowed.ids)
        if query.strip():
            units.check_field_access(units._fields['name'], 'read')
            domain &= Domain('name', 'ilike', query.strip())
        rows = units.search(domain, limit=30, offset=offset, order='name,id')
        return {'offset': offset, 'count': units.search_count(domain),
                'rows': [{'id': row.id, 'name': service._label(row)} for row in rows]}

    @api.model
    @api.readonly
    def open_rule(self, rule_id):
        service = self._scoped()
        rule = service._record('stock.warehouse.orderpoint', rule_id)
        return {'type': 'ir.actions.act_window', 'name': _('Ficha de reposición Odoo'),
                'res_model': rule._name, 'res_id': rule.id, 'views': [(False, 'form')],
                'target': 'current', 'context': {'allowed_company_ids': [service.env.company.id]}}

    @api.model
    @api.readonly
    def defaults(self, rule_id=False, product_id=False):
        service = self._scoped()
        service._manager()
        rule_id = service._optional_id(rule_id)
        product_id = service._optional_id(product_id)
        if rule_id:
            rule = service._record('stock.warehouse.orderpoint', rule_id, active=True)
            rule.check_access('write')
            result = service._configuration(rule)
            if result['bounds_status'] != 'known':
                raise AccessError(_('La unidad de la regla no está disponible con sus permisos actuales.'))
            values = {'product_min_qty': result['minimum'], 'product_max_qty': result['maximum']}
            for key, name in [('product_id', 'product'), ('warehouse_id', 'warehouse'),
                              ('location_id', 'location'), ('route_id', 'route'),
                              ('replenishment_uom_id', 'multiple')]:
                if result[name]['status'] != 'unknown':
                    values[key] = result[name]['id']
            for kind, spec in service._extension_specs().items():
                if result['extensions'][kind]['status'] != 'unknown':
                    values[spec['field']] = result['extensions'][kind]['id']
            return {'values': values, 'configuration': result}
        service.env['stock.warehouse.orderpoint'].check_access('create')
        values = {'product_min_qty': 0.0, 'product_max_qty': 0.0,
                  'route_id': False, 'replenishment_uom_id': False}
        values.update({spec['field']: False for spec in service._extension_specs().values()})
        if product_id:
            product = service._record('product.product', product_id, active=True)
            if not service._get(product, 'is_storable'):
                raise ValidationError(_('Elegí un producto con control de existencias.'))
            values['product_id'] = product.id
        warehouses = service.env['stock.warehouse'].search([
            ('company_id', '=', service.env.company.id),
        ], limit=2)
        if len(warehouses) == 1:
            location = service._get(warehouses, 'lot_stock_id')
            service._record('stock.location', location.id, active=True)
            values.update(warehouse_id=warehouses.id, location_id=location.id)
        return {'values': values, 'configuration': False}

    def _save_values(self, values, rule):
        relations = self._config_relations()
        if not isinstance(values, dict) or not values or set(values) - (_CONFIG_FIELDS | set(relations)):
            raise ValidationError(_('La configuración contiene campos no admitidos.'))
        result = dict(values)
        for name in ['product_id', 'warehouse_id', 'location_id', 'product_min_qty', 'product_max_qty']:
            if name not in result:
                if not rule:
                    raise ValidationError(_('Completá producto, depósito, ubicación, mínimo y máximo.'))
                value = self._get(rule, name)
                result[name] = value.id if name in relations else value
        product = self._record('product.product', result['product_id'], active=True)
        if not self._get(product, 'is_storable'):
            raise ValidationError(_('Elegí un producto con control de existencias.'))
        if self._relation(product, 'uom_id')['status'] != 'known':
            raise AccessError(_('La unidad del producto no está disponible con sus permisos actuales.'))
        warehouse = self._record('stock.warehouse', result['warehouse_id'], active=True)
        location = self._record('stock.location', result['location_id'], active=True)
        if warehouse.company_id != self.env.company or self._get(location, 'usage') != 'internal':
            raise ValidationError(_('Elegí un depósito propio y una ubicación interna compatible.'))
        view = self._get(warehouse, 'view_location_id')
        self._record('stock.location', view.id)
        path, root = self._get(location, 'parent_path'), self._get(view, 'parent_path')
        if not path or not root or not path.startswith(root):
            raise ValidationError(_('La ubicación debe pertenecer al depósito elegido.'))
        minimum = self._number(result['product_min_qty'])
        maximum = self._number(result['product_max_qty'])
        if not 0 <= minimum <= maximum:
            raise ValidationError(_('El mínimo debe ser mayor o igual a cero y no superar el máximo.'))
        result.update(product_min_qty=minimum, product_max_qty=maximum)
        product_changed = rule and product != self._get(rule, 'product_id')
        if product_changed:
            # Native supplier/BOM selectors accept explicit records; form
            # domains do not make a retained record compatible with a new SKU.
            template = self._get(product, 'product_tmpl_id')
            self._record('product.template', template.id)
            for name in ['supplier_id', 'bom_id']:
                if name not in rule._fields:
                    continue
                # Explicit clear/replacement must be evaluated instead of the
                # old selection when retargeting an existing rule.
                if name in result:
                    identifier = self._optional_id(result[name])
                    target = self.env[rule._fields[name].comodel_name].browse(identifier)
                else:
                    target = self._get(rule, name)
                if not target:
                    continue
                self._record(target._name, target.id)
                target_template = self._get(target, 'product_tmpl_id')
                target_product = self._get(target, 'product_id')
                if target_template != template or (target_product and target_product != product):
                    raise ValidationError(_('Las opciones de proveedor o fabricación no corresponden al nuevo producto. Revisalas antes de cambiarlo.'))
                if name == 'bom_id' and self._get(target, 'type') != 'normal':
                    raise ValidationError(_('La lista de materiales configurada debe ser de fabricación normal.'))
        for name in set(relations) - {'product_id', 'warehouse_id', 'location_id'}:
            if name in result:
                if result[name] is False or result[name] is None:
                    result[name] = False
                else:
                    self._record(relations[name], result[name], active=True)
        for kind, spec in self._extension_specs().items():
            name = spec['field']
            if name not in result or not result[name]:
                continue
            target = self._record(spec['model'], result[name], active=True)
            self._validate_extension(kind, target, product)
            changed = not rule or result[name] != self._get(rule, name).id
            route = result.get('route_id', self._get(rule, 'route_id').id if rule else False)
            if changed and not route:
                raise ValidationError(_('Elegí una ruta explícita antes de fijar proveedor o fabricación.'))
        dimension_change = not rule or any(
            name in result and result[name] != self._get(rule, name).id
            for name in relations
        )
        multiple = result.get('replenishment_uom_id',
                              self._get(rule, 'replenishment_uom_id').id if rule else False)
        if dimension_change and multiple:
            self._record('uom.uom', multiple, active=True)
            proposed = self._proposed_configuration(result, rule)
            allowed = self._get(proposed, 'allowed_replenishment_uom_ids')
            if multiple not in allowed.ids:
                raise ValidationError(_('El múltiplo debe ser una unidad o presentación admitida por el producto.'))
        return result

    @api.model
    def save_rule(self, values, rule_id=False, expected_token=False):
        service = self._scoped()
        service._manager()
        rule_id = service._optional_id(rule_id)
        model = service.env['stock.warehouse.orderpoint']
        relations = service._config_relations()
        rule = service._record('stock.warehouse.orderpoint', rule_id, active=True) if rule_id else model
        model.check_access('write' if rule else 'create')
        previous_token = False
        if rule:
            if not isinstance(expected_token, str) or len(expected_token) != 64:
                raise ValidationError(_('Volvé a abrir la configuración antes de guardar.'))
            previous_token = service._configuration_token(rule)
            rule._arg_lock_configuration()
        prepared = service._save_values(values, rule)
        # Participates in ARG configuration races. Complete global forecast
        # serialization belongs to the execution layer and its native adapters.
        products = service.env['product.product'].browse(prepared['product_id'])
        if rule:
            products |= service._get(rule, 'product_id')
        products._arg_lock_stock()
        reused = False
        if not rule:
            existing = model.with_context(active_test=False).search([
                ('company_id', '=', service.env.company.id),
                ('product_id', '=', prepared['product_id']),
                ('location_id', '=', prepared['location_id']),
            ], limit=1)
            if existing:
                same = all((service._get(existing, name).id if name in relations
                            else service._get(existing, name)) == value for name, value in prepared.items())
                if not service._get(existing, 'active') or not same:
                    raise UserError(_('Ya existe una regla para este producto y ubicación. Abrila para editarla.'))
                rule = existing
                reused = True
            else:
                prepared = {'route_id': False, 'replenishment_uom_id': False, **prepared,
                            'company_id': service.env.company.id, 'trigger': 'manual',
                            'qty_to_order_manual': 0.0, 'snoozed_until': False, 'active': True}
                for optional in ['supplier_id', 'bom_id']:
                    if optional in model._fields and optional not in prepared:
                        prepared[optional] = False
                rule = model.create(prepared)
        else:
            changed = {name: value for name, value in prepared.items()
                       if (service._get(rule, name).id if name in relations
                           else service._get(rule, name)) != value}
            if changed and expected_token != previous_token:
                raise UserError(_('La configuración cambió desde que la abriste. Volvé a consultarla antes de guardar.'))
            if changed:
                rule.write(changed)
        # Native inverses may adjust secondary configuration. Validate the
        # effective stored rule as well; failure rolls back the entire save.
        multiple = service._get(rule, 'replenishment_uom_id')
        if multiple:
            service._record('uom.uom', multiple.id, active=True)
            for name in ['route_id', 'supplier_id', 'bom_id']:
                if name in rule._fields:
                    target = service._get(rule, name)
                    if target:
                        service._record(target._name, target.id)
            if multiple not in service._get(rule, 'allowed_replenishment_uom_ids'):
                raise ValidationError(_('La presentación no es válida para la configuración resultante. Revisá la ruta y el múltiplo.'))
        message = (_('La misma configuración ya existía. Se conservó su modalidad. No se generó abastecimiento.')
                   if reused else _('Configuración guardada. No se generó abastecimiento.'))
        return {'configuration': service._configuration(rule), 'reused': reused, 'message': message}
