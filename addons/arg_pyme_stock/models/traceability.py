"""Native lot movements and current quantities; no inventory ledger of our own."""
from ast import literal_eval
import math
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class StockTrace(models.AbstractModel):
    _name = 'arg.pyme.stock.trace'
    _description = 'Series y lotes ARG'

    def _scoped(self):
        service = self.with_context({'allowed_company_ids': [self.env.company.id],
            'lang': self.env.context.get('lang'), 'tz': self.env.context.get('tz'), 'active_test': True})
        service.env['arg.pyme.stock.matrix']._authorize()
        return service

    def _record(self, model, identifier, active=False):
        if type(identifier) is not int or identifier <= 0:
            raise ValidationError(_('Referencia no válida.'))
        record = self.env[model].browse(identifier).exists()
        record.check_access('read')
        if not record or ('company_id' in record._fields and record.company_id and record.company_id != self.env.company):
            raise AccessError(_('Registro no disponible en la compañía actual.'))
        if active and 'active' in record._fields and not record.active:
            raise AccessError(_('El registro está archivado.'))
        return record

    def _relation(self, record, field):
        """Check target access before display_name; many2one.read may sudo that name."""
        try:
            record.check_field_access(record._fields[field], 'read')
            target = record[field]
            if not target:
                return {'id': False, 'name': '—', 'status': 'unset'}
            self._record(target._name, target.id)
            label = target.display_name
            if 'arg_number' in target._fields:
                target.check_field_access(target._fields['arg_number'], 'read')
                label = target.arg_number or label
            return {'id': target.id, 'name': label, 'status': 'known'}
        except AccessError:
            return {'id': False, 'name': _('No determinado por permisos'), 'status': 'unknown'}

    def _product(self, product):
        product.check_access('read')
        return {'id': product.id, 'name': product.display_name, 'code': product.default_code or '',
                'unit': self._relation(product, 'uom_id'), 'tracking': product.tracking, 'active': product.active}

    def _lot(self, lot):
        try:
            lot.check_field_access(lot._fields['product_id'], 'read')
            product = self._record('product.product', lot.product_id.id)
            summary = self._product(product)
        except AccessError:
            summary = {'id': False, 'name': _('No determinado por permisos'), 'code': '',
                       'unit': {'id': False, 'name': _('No determinado'), 'status': 'unknown'},
                       'tracking': False, 'active': False}
        return {'id': lot.id, 'name': lot.name, 'ref': lot.ref or '', 'product': summary}

    def _offset(self, offset):
        if type(offset) is not int or offset < 0:
            raise ValidationError(_('Página no válida.'))
        return offset

    def _moment(self, value):
        if value is None or value is False or value == '':
            return None
        try:
            if not isinstance(value, str):
                raise ValueError()
            instant = fields.Datetime.to_datetime(value)
            if instant.tzinfo is not None or fields.Datetime.to_string(instant) != value:
                raise ValueError()
            return instant
        except (TypeError, ValueError, OverflowError):
            raise ValidationError(_('Elegí una fecha y hora válidas.'))

    @api.model
    @api.readonly
    def reference(self, kind, identifier):
        service = self._scoped()
        if kind == 'lot':
            return service._lot(service._record('stock.lot', identifier))
        if kind == 'product':
            return service._product(service._record('product.product', identifier))
        raise ValidationError(_('Selector no válido.'))

    @api.model
    @api.readonly
    def options(self):
        service = self._scoped()
        return {'company': service.env.company.display_name,
                'can_create': service.env['stock.lot'].has_access('create')}

    @api.model
    @api.readonly
    def choices(self, kind, query='', offset=0, product_id=False):
        service = self._scoped(); service._offset(offset)
        if kind not in ('lot', 'product'):
            raise ValidationError(_('Selector no válido.'))
        model = service.env['stock.lot' if kind == 'lot' else 'product.product']
        domain = [('company_id', 'in', [False, service.env.company.id])]
        if kind == 'product':
            domain += [('is_storable', '=', True), ('tracking', 'in', ['serial', 'lot'])]
        elif product_id is not False and product_id is not None:
            domain.append(('product_id', '=', service._record('product.product', product_id).id))
        query = str(query or '').strip()[:120]
        if query:
            domain += ['|', ('name', 'ilike', query), ('ref' if kind == 'lot' else 'default_code', 'ilike', query)]
        records = model.search(domain, offset=offset, limit=30, order='name,id')
        return {'rows': [service._lot(r) if kind == 'lot' else service._product(r) for r in records],
                'offset': offset, 'limit': 30, 'count': model.search_count(domain)}

    def _movement(self, line):
        product = self._record('product.product', line.product_id.id)
        unit = self._relation(product, 'uom_id')
        line.check_field_access(line._fields['quantity_product_uom'], 'read')
        quantity = line.quantity_product_uom
        if not math.isfinite(quantity):
            raise UserError(_('La línea contiene una cantidad no finita.'))
        picking = self._relation(line, 'picking_id'); move = self._relation(line, 'move_id')
        parent = {'id': False, 'name': '—', 'status': 'unset'}
        if move['status'] == 'known':
            parent = self._relation(line.move_id, 'origin_returned_move_id')
        source = self._relation(line, 'location_id'); destination = self._relation(line, 'location_dest_id')
        return {'id': line.id, 'when': fields.Datetime.to_string(line.date),
                'product': self._product(product), 'quantity': quantity if unit['status'] == 'known' else None,
                'unit': unit, 'source': source, 'destination': destination,
                'source_usage': line.location_id.usage if source['status'] == 'known' else None,
                'destination_usage': line.location_dest_id.usage if destination['status'] == 'known' else None,
                'document': picking if picking['status'] == 'known' else move,
                'has_picking': picking['status'] == 'known', 'return_of': parent,
                'inventory': bool(line.is_inventory), 'scrap': bool(line.is_scrap)}

    def _quantities(self, lot, offset=0):
        self._offset(offset)
        result = {'status': 'unknown', 'total': None, 'count': None, 'rows': [], 'offset': offset, 'limit': 30,
                  'unit': {'id': False, 'name': _('No determinado'), 'status': 'unknown'},
                  'as_of': fields.Datetime.to_string(fields.Datetime.now()),
                  'scope': _('Existencias visibles actuales en las ubicaciones del dominio nativo de la compañía.'),
                  'reason': _('No determinado según los permisos actuales.')}
        try:
            model = self.env['stock.quant']; model.check_access('read')
            lot.check_field_access(lot._fields['product_qty'], 'read')
            product = self._record('product.product', lot.product_id.id)
            unit = self._relation(product, 'uom_id')
            if unit['status'] != 'known':
                raise AccessError(_('Unidad no disponible.'))
            domain = list(product._get_domain_locations()[0]) + [('lot_id', '=', lot.id)]
            total = lot.product_qty
            if not math.isfinite(total):
                raise UserError(_('La existencia nativa no es finita.'))
            records = model.search(domain, offset=offset, limit=30, order='location_id,id')
            rows = []
            for quant in records:
                if quant.product_id != product:
                    raise UserError(_('El lote contiene existencias de otro producto. Revisá el origen nativo.'))
                for field in ('quantity', 'reserved_quantity'):
                    quant.check_field_access(quant._fields[field], 'read')
                if not all(math.isfinite(v) for v in (quant.quantity, quant.reserved_quantity)):
                    raise UserError(_('Una cantidad nativa no es finita.'))
                rows.append({'id': quant.id, 'location': self._relation(quant, 'location_id'),
                             'owner': self._relation(quant, 'owner_id'), 'package': self._relation(quant, 'package_id'),
                             'quantity': quant.quantity, 'reserved': quant.reserved_quantity})
            result.update(status='known', total=total, unit=unit, rows=rows, count=model.search_count(domain), reason='')
        except AccessError:
            pass
        except UserError as error:
            result['reason'] = str(error)
        return result

    @api.model
    @api.readonly
    def quantities(self, lot_id, offset=0):
        service = self._scoped(); lot = service._record('stock.lot', lot_id)
        service._record('product.product', lot.product_id.id)
        return service._quantities(lot, offset)

    @api.model
    @api.readonly
    def page(self, lot_id, offset=0, start=None, end=None):
        service = self._scoped(); service._offset(offset); lot = service._record('stock.lot', lot_id)
        start_at, end_at = service._moment(start), service._moment(end)
        if start_at and end_at and start_at > end_at:
            raise ValidationError(_('El inicio debe ser anterior al fin del rango.'))
        history = {'status': 'unknown', 'rows': [], 'count': None, 'offset': offset, 'limit': 30,
                   'reason': _('No determinado según los permisos actuales.')}
        try:
            model = service.env['stock.move.line']
            domain = [('lot_id', '=', lot.id), ('company_id', '=', service.env.company.id), ('state', '=', 'done')]
            if start_at: domain.append(('date', '>=', start_at))
            if end_at: domain.append(('date', '<=', end_at))
            records = model.search(domain, offset=offset, limit=30, order='date,id')
            history.update(status='known', rows=[service._movement(line) for line in records],
                           count=model.search_count(domain), reason='')
        except AccessError:
            pass
        return {'lot': service._lot(lot), 'company': service.env.company.display_name,
                'as_of': fields.Datetime.to_string(fields.Datetime.now()),
                'start': fields.Datetime.to_string(start_at) if start_at else None,
                'end': fields.Datetime.to_string(end_at) if end_at else None,
                'history': history, 'quantities': service._quantities(lot)}

    @api.model
    @api.readonly
    def open_document(self, lot_id, line_id):
        service = self._scoped(); lot = service._record('stock.lot', lot_id)
        line = service._record('stock.move.line', line_id)
        if line.lot_id != lot or line.state != 'done':
            raise AccessError(_('La línea no pertenece a la historia elegida.'))
        picking = service._relation(line, 'picking_id')
        if picking['status'] == 'known':
            target = service._record('stock.picking', picking['id'])
            views = [(service.env.ref('arg_pyme_stock.picking_form').id, 'form')]
        else:
            target = service._record('stock.move', line.move_id.id); views = [(False, 'form')]
        return {'type': 'ir.actions.act_window', 'res_model': target._name, 'res_id': target.id,
                'views': views, 'context': dict(service.env.context)}

    @api.model
    @api.readonly
    def open_lot(self, lot_id):
        service = self._scoped(); lot = service._record('stock.lot', lot_id)
        return {'type': 'ir.actions.act_window', 'res_model': 'stock.lot', 'res_id': lot.id,
                'views': [(service.env.ref('stock.view_production_lot_form').id, 'form')],
                'context': dict(service.env.context)}

    @api.model
    @api.readonly
    def advanced(self, lot_id):
        service = self._scoped(); lot = service._record('stock.lot', lot_id)
        action = service.env['ir.actions.actions']._for_xml_id('stock.action_stock_report')
        native_context = literal_eval(action.get('context') or '{}')
        action['context'] = {**native_context, **service.env.context, 'active_id': lot.id,
                             'active_ids': [lot.id], 'active_model': 'stock.lot'}
        return action

    @api.model
    @api.readonly
    def from_lot(self, lot_id):
        service = self._scoped(); lot = service._record('stock.lot', lot_id)
        return {'type': 'ir.actions.client', 'tag': 'arg_pyme.stock_trace', 'name': _('Series y lotes ARG'),
                'params': {'lot_id': lot.id}, 'context': dict(service.env.context)}

    @api.model
    @api.readonly
    def create_lot(self, product_id=False):
        service = self._scoped(); service.env['stock.lot'].check_access('create')
        context = dict(service.env.context)
        if product_id is not False and product_id is not None:
            context['default_product_id'] = service._record('product.product', product_id, active=True).id
        return {'type': 'ir.actions.act_window', 'name': _('Nueva serie/lote ARG'),
                'res_model': 'arg.pyme.lot.create', 'views': [(service.env.ref('arg_pyme_stock.lot_create_form').id, 'form')],
                'target': 'new', 'context': context}


class StockLotTraceAction(models.Model):
    _inherit = 'stock.lot'

    def action_arg_trace(self):
        self.ensure_one()
        return self.env['arg.pyme.stock.trace'].from_lot(self.id)
