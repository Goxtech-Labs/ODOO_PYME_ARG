"""Read-only sales price consultation; native rules remain the only price engine."""
import math
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class PriceConsultation(models.AbstractModel):
    _name = 'arg.pyme.price.consultation'
    _description = 'Consulta de precio y condiciones ARG'

    def _scoped(self):
        service = self.with_context({'allowed_company_ids': [self.env.company.id],
            'lang': self.env.context.get('lang'), 'tz': self.env.context.get('tz'), 'active_test': True})
        service.env['arg.pyme.pricelist.matrix']._authorize()
        return service

    def _record(self, model, identifier, active=True):
        if type(identifier) is not int or identifier <= 0:
            raise ValidationError(_('Referencia no válida.'))
        record = self.env[model].browse(identifier).exists()
        record.check_access('read')
        if not record or (record.company_id and record.company_id != self.env.company):
            raise AccessError(_('Registro no disponible en la compañía actual.'))
        if active and not record.active:
            raise AccessError(_('El registro está archivado.'))
        return record

    def _choice(self, record, kind):
        row = {'id': record.id, 'name': record.display_name}
        if kind == 'product':
            row.update(code=record.default_code or '', unit=record.uom_id.display_name)
        elif kind == 'pricelist':
            row['currency'] = record.currency_id.name
        return row

    @api.model
    @api.readonly
    def reference(self, kind, identifier):
        service = self._scoped()
        models_by_kind = {'partner': 'res.partner', 'product': 'product.product', 'pricelist': 'product.pricelist'}
        if not isinstance(kind, str) or kind not in models_by_kind:
            raise ValidationError(_('Referencia no válida.'))
        return service._choice(service._record(models_by_kind[kind], identifier), kind)

    @api.model
    @api.readonly
    def options(self):
        service = self._scoped()
        return {'when': fields.Datetime.to_string(fields.Datetime.now()),
                'company': service.env.company.display_name,
                'can_configure': service.env.user.has_group('arg_pyme_base.group_manager')}

    @api.model
    @api.readonly
    def choices(self, kind, query='', offset=0, template_id=False):
        service = self._scoped()
        models_by_kind = {'partner': 'res.partner', 'product': 'product.product', 'pricelist': 'product.pricelist'}
        if not isinstance(kind, str) or kind not in models_by_kind or type(offset) is not int or offset < 0:
            raise ValidationError(_('Selector o página no válidos.'))
        model = service.env[models_by_kind[kind]]
        domain = [('company_id', 'in', [False, service.env.company.id])]
        if template_id is not False and template_id is not None:
            if kind != 'product':
                raise ValidationError(_('El filtro de plantilla sólo corresponde a productos.'))
            template = service._record('product.template', template_id)
            domain.append(('product_tmpl_id', '=', template.id))
        query = str(query or '').strip()[:120]
        if query:
            code = 'default_code' if kind == 'product' else ('ref' if kind == 'partner' else 'name')
            domain += ['|', ('name', 'ilike', query), (code, 'ilike', query)]
        records = model.search(domain, offset=offset, limit=30, order='name,id')
        rows = [service._choice(record, kind) for record in records]
        return {'rows': rows, 'count': model.search_count(domain), 'offset': offset, 'limit': 30}

    @api.model
    @api.readonly
    def defaults(self, partner_id):
        service = self._scoped(); partner = service._record('res.partner', partner_id)
        result = {'partner': {'id': partner.id, 'name': partner.display_name},
                  'pricelist': None, 'pricelist_status': 'unknown',
                  'payment_term': None, 'payment_term_status': 'unavailable',
                  'note': None, 'note_status': 'unavailable'}
        try:
            pricelist = partner.property_product_pricelist
            if pricelist:
                service._record('product.pricelist', pricelist.id)
                result.update(pricelist={'id': pricelist.id, 'name': pricelist.display_name,
                                         'currency': pricelist.currency_id.name}, pricelist_status='known')
            else:
                result['pricelist_status'] = 'unset'
        except AccessError:
            pass
        for field, value_key, status_key in [('property_payment_term_id', 'payment_term', 'payment_term_status'),
                                            ('arg_conditions_note', 'note', 'note_status')]:
            if field not in partner._fields:
                continue
            try:
                partner.check_field_access(partner._fields[field], 'read')
                value = partner[field]
                if partner._fields[field].type == 'many2one' and value:
                    value.check_access('read')
                    if 'company_id' in value._fields and value.company_id and value.company_id != service.env.company:
                        raise AccessError(_('Condición no disponible en la compañía actual.'))
                    value = value.display_name
                result[value_key] = value or None
                result[status_key] = 'known'
            except AccessError:
                result[status_key] = 'unknown'
        return result

    def _when(self, date, at):
        try:
            if at is not None:
                if not isinstance(at, str) or not at:
                    raise ValueError()
                when = fields.Datetime.to_datetime(at)
                if fields.Datetime.to_string(when) != at or when.tzinfo is not None:
                    raise ValueError()
                return when, 'instant'
            if date is not None:
                if not isinstance(date, str) or not date:
                    raise ValueError()
                day = fields.Date.to_date(date)
                if fields.Date.to_string(day) != date:
                    raise ValueError()
                return fields.Datetime.to_datetime(day), 'matrix_day'
            return fields.Datetime.now(), 'instant'
        except (TypeError, ValueError, OverflowError):
            raise ValidationError(_('Elegí una fecha y hora válidas.'))

    def _trace(self, product, pricelist, quantity, when):
        """Inspect the same native winning rules; never reproduce their arithmetic."""
        steps = []; seen = set(); current = pricelist; cost_basis = False
        for depth in range(100):
            self._record('product.pricelist', current.id, active=False)
            if current.id in seen:
                raise UserError(_('Las listas tienen una dependencia circular.'))
            seen.add(current.id)
            rule_id = current._get_product_rule(product, quantity, date=when, uom=product.uom_id)
            rule = self.env['product.pricelist.item'].browse(rule_id).exists()
            rule.check_access('read')
            if rule and rule.pricelist_id != current:
                raise UserError(_('Una extensión devolvió una regla de otra lista.'))
            step = {'list': current.display_name, 'currency': current.currency_id.name,
                    'list_active': current.active, 'rule_id': rule.id or False}
            if not rule:
                step.update(kind='catalog', basis='list_price')
                steps.append(step)
                return steps, cost_basis, False
            kind = rule.compute_price
            basis = 'fixed' if kind == 'fixed' else rule.base
            cost_basis |= basis == 'standard_price'
            step.update(kind=kind, basis=basis, scope=rule.applied_on,
                        minimum=rule.min_quantity, unit=(rule.uom_id or product.uom_id).display_name,
                        start=fields.Datetime.to_string(rule.date_start) if rule.date_start else None,
                        end=fields.Datetime.to_string(rule.date_end) if rule.date_end else None)
            if kind == 'fixed':
                step['fixed_price'] = rule.fixed_price
            elif kind in ('discount', 'markup'):
                step.update(discount=rule.price_discount, markup=rule.price_markup,
                            rounding=rule.price_round, surcharge=rule.price_surcharge,
                            minimum_margin=rule.price_min_margin, maximum_margin=rule.price_max_margin)
            steps.append(step)
            if kind == 'fixed' or basis != 'pricelist':
                return steps, cost_basis, kind not in ('fixed', 'discount', 'markup') or basis not in ('fixed', 'list_price', 'standard_price')
            if not rule.base_pricelist_id:
                raise UserError(_('La regla necesita una lista base válida.'))
            current = rule.base_pricelist_id
        return steps, cost_basis, True

    @api.model
    @api.readonly
    def explain(self, product_id, pricelist_id=False, quantity=1, date=None, partner_id=False, at=None, expected_token=None):
        service = self._scoped(); product = service._record('product.product', product_id)
        if type(quantity) not in (int, float) or not math.isfinite(quantity) or quantity <= 0:
            raise ValidationError(_('La cantidad debe ser positiva y finita.'))
        if expected_token is not None and expected_token is not False and (
                not isinstance(expected_token, str) or len(expected_token) != 64
                or any(c not in '0123456789abcdef' for c in expected_token)):
            raise ValidationError(_('La referencia de la matriz no es válida.'))
        when, basis = service._when(date, at)
        conditions = service.defaults(partner_id) if partner_id is not False and partner_id is not None else None
        if pricelist_id is not False and pricelist_id is not None:
            service._record('product.pricelist', pricelist_id)
        if (pricelist_id is False or pricelist_id is None) and conditions and conditions['pricelist']:
            pricelist_id = conditions['pricelist']['id']
        result = {'product': {'id': product.id, 'name': product.display_name, 'code': product.default_code or ''},
                  'quantity': quantity, 'unit': product.uom_id.display_name, 'company': service.env.company.display_name,
                  'when': fields.Datetime.to_string(when), 'date_basis': basis, 'conditions': conditions,
                  'price': None, 'status': 'unknown', 'steps': [], 'explanation_status': 'unknown',
                  'reason': '', 'tax_scope': 'not_computed', 'changed_since_matrix': False}
        if not pricelist_id:
            result['reason'] = _('Elegí una lista disponible; no se asignó una lista ficticia al cliente.')
            return result
        pricelist = service._record('product.pricelist', pricelist_id)
        result['pricelist'] = {'id': pricelist.id, 'name': pricelist.display_name, 'currency': pricelist.currency_id.name}
        can_cost = service.env.user.has_group('arg_pyme_base.group_manager')
        cost_basis = False
        try:
            steps, cost_basis, partial = service._trace(product, pricelist, float(quantity), when)
            cell = service.env['arg.pyme.pricelist.matrix']._cell(product, pricelist, when, quantity)
            result['changed_since_matrix'] = bool(expected_token and expected_token != cell['token'])
            if cell['price'] is None:
                result['reason'] = cell['reason']
                return result
            if not math.isfinite(cell['price']):
                raise UserError(_('El cálculo nativo no produjo un importe finito.'))
            result.update(price=cell['price'], status='known')
            if cost_basis and not can_cost:
                result.update(explanation_status='restricted', reason=_('El detalle de esta base de cálculo está restringido por permisos.'))
                return result
            if not can_cost:
                if partial:
                    result.update(explanation_status='restricted', reason=_('La extensión de cálculo necesita un adaptador de explicación autorizado.'))
                    return result
                for step in steps:
                    restricted = bool(step.pop('minimum_margin', 0) or step.get('maximum_margin', 0))
                    step.pop('maximum_margin', None)
                    if restricted:
                        step['adjustments_restricted'] = True
                        partial = True
            result.update(steps=steps, explanation_status='partial' if partial else 'known')
            if partial:
                result['reason'] = _('El detalle mostrado es parcial por permisos o por el alcance de la traza.')
            # Fixed template/global/category rules can add variant extras natively.
            if steps and steps[0]['kind'] == 'fixed':
                extra = 0 if steps[0]['scope'] == '0_product_variant' else product._get_attributes_extra_price()
                result['variant_extra'] = {'amount': extra, 'currency': product.currency_id.name,
                                           'unit': product.uom_id.display_name}
        except AccessError:
            result.update(price=None, status='unknown', steps=[], explanation_status='unknown',
                          reason=_('No determinado según los permisos y la compañía actual.'))
        except (UserError, RecursionError, OverflowError) as error:
            result.update(price=None, status='unknown', steps=[], explanation_status='unknown',
                          reason=(str(error) if isinstance(error, UserError) and (can_cost or not cost_basis)
                                  else _('No se pudo completar el cálculo nativo con el detalle permitido.')))
        return result

    @api.model
    @api.readonly
    def open_rules(self, pricelist_id):
        service = self._scoped()
        if not service.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Configurar reglas requiere Responsable ARG.'))
        pricelist = service._record('product.pricelist', pricelist_id)
        pricelist.check_access('write')
        return {'type': 'ir.actions.act_window', 'name': _('Lista y condiciones ARG'),
                'res_model': 'product.pricelist', 'res_id': pricelist.id, 'views': [(False, 'form')],
                'context': {**service.env.context, 'default_date_start': fields.Datetime.to_string(fields.Datetime.now())}}

    @api.model
    @api.readonly
    def open_partner(self, partner_id):
        service = self._scoped(); partner = service._record('res.partner', partner_id)
        view = service.env.ref('base.view_partner_form')
        return {'type': 'ir.actions.act_window', 'name': _('Condiciones del cliente'), 'res_model': 'res.partner',
                'res_id': partner.id, 'views': [(view.id, 'form')], 'context': dict(service.env.context)}

    @api.model
    @api.readonly
    def from_template(self, template_id):
        service = self._scoped(); template = service._record('product.template', template_id)
        products = service.env['product.product'].search([
            ('product_tmpl_id', '=', template.id), ('company_id', 'in', [False, service.env.company.id]),
        ], limit=2)
        params = {'template_id': template.id}
        if len(products) == 1:
            params['product_id'] = products.id
        return {'type': 'ir.actions.client', 'tag': 'arg_pyme.price_consultation',
                'name': _('Consulta de precio ARG'), 'params': params, 'context': dict(service.env.context)}
