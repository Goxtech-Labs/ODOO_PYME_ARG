"""Bounded native variant consultation. No variant factories or business writes."""
from odoo import api, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


def _identifier(value):
    if type(value) is not int or value <= 0:
        raise ValidationError(_('Referencia no válida.'))
    return value


def _offset(value):
    if type(value) is not int or value < 0:
        raise ValidationError(_('Página no válida.'))
    return value


class VariantMatrix(models.AbstractModel):
    _name = 'arg.pyme.variant.matrix'
    _description = 'Matriz de variantes ARG'

    def _scoped(self):
        # Never inherit a caller's historic/warehouse/owner/default filters.
        return self.with_context({
            'allowed_company_ids': [self.env.company.id],
            'lang': self.env.context.get('lang'), 'tz': self.env.context.get('tz'),
            'active_test': True,
        })

    def _authorize(self):
        if self.env.user.share or not self.env.user.has_group('arg_pyme_base.group_operator'):
            raise AccessError(_('Se requiere acceso al catálogo ARG.'))

    def _template(self, template_id):
        self._authorize()
        template = self.env['product.template'].browse(_identifier(template_id)).exists()
        template.check_access('read')
        if not template or not template.active or (template.company_id and template.company_id != self.env.company):
            raise AccessError(_('Producto no disponible para la compañía actual.'))
        return template

    def _lines(self, template):
        return self.env['product.template.attribute.line'].search([
            ('product_tmpl_id', '=', template.id), ('active', '=', True),
            ('value_count', '>', 0), ('attribute_id.create_variant', '!=', 'no_variant'),
        ], order='sequence,attribute_id,id')

    def _values(self, line, query='', offset=0, limit=30):
        domain = [('attribute_line_id', '=', line.id), ('ptav_active', '=', True)]
        query = str(query or '').strip()[:120]
        if query:
            domain.append(('name', 'ilike', query))
        model = self.env['product.template.attribute.value']
        return model.search(domain, offset=_offset(offset), limit=limit, order='sequence,id'), model.search_count(domain)

    @api.model
    def templates(self, query='', offset=0):
        service = self._scoped(); service._authorize()
        domain = [('company_id', 'in', [False, service.env.company.id])]
        query = str(query or '').strip()[:120]
        if query:
            domain += ['|', ('name', 'ilike', query), ('default_code', 'ilike', query)]
        model = service.env['product.template']
        rows = model.search(domain, offset=_offset(offset), limit=30, order='name,id')
        return {'rows': [{'id': p.id, 'name': p.display_name} for p in rows],
                'count': model.search_count(domain), 'offset': offset, 'limit': 30}

    @api.model
    def configure(self, template_id):
        service = self._scoped(); template = service._template(template_id)
        lines = service._lines(template)
        options = []
        for line in lines:
            values, count = service._values(line, limit=1)
            options.append({'id': line.id, 'name': line.attribute_id.display_name,
                            'first': {'id': values.id, 'name': values.name} if values else False,
                            'count': count})
        return {'template': {'id': template.id, 'name': template.display_name},
                'lines': options, 'x': lines[:1].id or False, 'y': lines[1:2].id or False,
                'company': service.env.company.display_name}

    @api.model
    def values(self, template_id, line_id, query='', offset=0):
        service = self._scoped(); template = service._template(template_id)
        line = service._lines(template).filtered(lambda row: row.id == _identifier(line_id))
        if not line:
            raise ValidationError(_('El atributo no pertenece al producto.'))
        values, count = service._values(line, query, offset)
        return {'rows': [{'id': value.id, 'name': value.name} for value in values],
                'count': count, 'offset': offset, 'limit': 30}

    def _layout(self, template, x, y, fixed):
        if not isinstance(fixed, dict):
            raise ValidationError(_('Filtros de atributos no válidos.'))
        lines = self._lines(template); by_id = {line.id: line for line in lines}
        for axis in (x, y):
            if axis is not False and (_identifier(axis) not in by_id):
                raise ValidationError(_('El eje no pertenece al producto.'))
        if x and x == y:
            raise ValidationError(_('Elija atributos diferentes para filas y columnas.'))
        chosen = self.env['product.template.attribute.value']; normalized = {}
        if any(str(key) not in {str(line.id) for line in lines if line.id not in (x, y)} for key in fixed):
            raise ValidationError(_('Hay filtros que no corresponden a los atributos fijos.'))
        for line in lines:
            if line.id in (x, y):
                continue
            supplied = fixed.get(str(line.id), fixed.get(line.id))
            if supplied is None:
                value = self._values(line, limit=1)[0]
            else:
                value = self.env['product.template.attribute.value'].search([
                    ('id', '=', _identifier(supplied)), ('attribute_line_id', '=', line.id), ('ptav_active', '=', True),
                ], limit=1)
            if not value:
                raise UserError(_('El atributo %s necesita un valor activo y visible.', line.attribute_id.display_name))
            chosen |= value
            normalized[str(line.id)] = {'id': value.id, 'name': value.name, 'line_name': line.attribute_id.display_name}
        return by_id.get(x), by_id.get(y), chosen, normalized

    def _arg_quantities(self, products):
        return {p.id: {'status': 'not_applicable' if p.type == 'service' else 'unavailable',
                       'physical': None, 'free': None} for p in products}

    @api.model
    def page(self, template_id, x=False, y=False, fixed=None, x_offset=0, y_offset=0, x_query='', y_query=''):
        service = self._scoped(); template = service._template(template_id)
        xline, yline, chosen, fixed = service._layout(template, x, y, {} if fixed is None else fixed)
        xvalues, xcount = service._values(xline, x_query, x_offset, 8) if xline else ([False], 1)
        yvalues, ycount = service._values(yline, y_query, y_offset, 15) if yline else ([False], 1)
        combinations = []
        for row in yvalues:
            for column in xvalues:
                combination = chosen
                if row: combination |= row
                if column: combination |= column
                combinations.append(combination.sorted(key=lambda v: (
                    v.attribute_line_id.sequence, v.attribute_id.id, v.attribute_line_id.id)))
        possible = {combination._ids2str() for combination in template._filter_combinations_impossible_by_config(
            combinations, ignore_no_variant=True)}
        # The native cached lookup uses sudo; search only this visible page instead.
        products = service.env['product.product'].search([
            ('product_tmpl_id', '=', template.id), ('active', '=', True),
            ('combination_indices', 'in', list(possible) + ([False] if '' in possible else [])),
        ], limit=120) if possible else service.env['product.product']
        by_key = {p.combination_indices or '': p for p in products}
        quantities = service._arg_quantities(products)
        rows = []; index = 0
        for row in yvalues:
            cells = []
            for column in xvalues:
                key = combinations[index]._ids2str(); index += 1
                product = by_key.get(key)
                cell = {'key': key, 'status': 'excluded' if key not in possible else 'unknown'}
                if product and key in possible:
                    cell.update(status='visible', id=product.id, name=product.display_name,
                                code=product.default_code or '', barcode=product.barcode or '',
                                unit=product.uom_id.display_name, quantities=quantities[product.id])
                cells.append(cell)
            rows.append({'id': row.id if row else 0, 'name': row.name if row else _('Producto'), 'cells': cells})
        return {'rows': rows, 'columns': [{'id': c.id if c else 0, 'name': c.name if c else _('Variante')} for c in xvalues],
                'fixed': fixed, 'x_count': xcount, 'y_count': ycount, 'x_offset': _offset(x_offset),
                'y_offset': _offset(y_offset), 'company': service.env.company.display_name}

    def _selected(self, template_id, ids):
        template = self._template(template_id)
        if not isinstance(ids, list) or not ids or len(ids) > 200 or any(type(i) is not int or i <= 0 for i in ids) or len(set(ids)) != len(ids):
            raise ValidationError(_('Seleccione entre una y doscientas variantes diferentes.'))
        products = self.env['product.product'].browse(ids).exists(); products.check_access('read')
        if len(products) != len(ids) or any(not p.active or p.product_tmpl_id != template or (p.company_id and p.company_id != self.env.company) for p in products):
            raise AccessError(_('La selección contiene variantes no disponibles.'))
        for product in products:
            if not template._is_combination_possible_by_config(product.product_template_attribute_value_ids, ignore_no_variant=True):
                raise UserError(_('Cambió la configuración del producto. Revise la selección.'))
        return products

    @api.model
    def open_variant(self, template_id, product_id):
        service = self._scoped(); product = service._selected(template_id, [_identifier(product_id)])
        return {'type': 'ir.actions.act_window', 'name': _('Variante ARG'), 'res_model': 'product.product',
                'res_id': product.id, 'views': [(False, 'form')], 'context': dict(service.env.context)}

    @api.model
    def labels(self, template_id, product_ids):
        service = self._scoped(); products = service._selected(template_id, product_ids)
        return products.action_open_label_layout()

    @api.model
    def prices(self, template_id):
        service = self._scoped(); template = service._template(template_id)
        return {'type': 'ir.actions.client', 'tag': 'arg_pyme.price_matrix', 'name': _('Precios ARG'),
                'params': {'template_id': template.id, 'template_name': template.display_name},
                'context': dict(service.env.context)}
