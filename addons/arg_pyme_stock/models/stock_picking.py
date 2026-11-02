from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError

_MOVE_ENGINE = object()


def _manager(env):
    if not env.user.has_group('arg_pyme_base.group_manager'):
        raise AccessError(_('Validar o cancelar movimientos requiere responsable ARG.'))


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'arg.pyme.document.mixin']
    arg_demand_snapshot = fields.Json(readonly=True, copy=False, groups='base.group_user')

    def _arg_document_code(self):
        if self.return_id:
            return {'outgoing': 'DCL', 'incoming': 'DCP'}.get(self.return_id.picking_type_id.code, 'TRA')
        return {'outgoing': 'REM', 'incoming': 'ENT', 'internal': 'TRA'}.get(self.picking_type_id.code)

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get('arg_demand_snapshot') or self.env.context.get('default_arg_demand_snapshot'):
                raise AccessError(_('La evidencia del movimiento se genera al validar.'))
            if values.get('state', self.env.context.get('default_state')) in ('done', 'cancel'):
                raise AccessError(_('Prepare el movimiento y valídelo mediante su acción.'))
        return super().create(vals_list)

    def write(self, values):
        if 'arg_demand_snapshot' in values:
            raise AccessError(_('La demanda histórica no se modifica manualmente.'))
        if 'state' in values and self.env.context.get('_arg_move_engine') is not _MOVE_ENGINE and (values['state'] in ('done', 'cancel') or self.filtered(lambda p: p.state in ('done', 'cancel') and p.state != values['state'])):
            raise AccessError(_('Use Validar o Cancelar, no un cambio directo de estado.'))
        if {'return_id', 'backorder_id'} & values.keys() and self.filtered('arg_identity_id'):
            raise AccessError(_('Las relaciones de origen se reciben al crear el documento vinculado.'))
        if {'location_id', 'location_dest_id', 'partner_id', 'scheduled_date'} & values.keys() and self.filtered(lambda p: p.state in ('done', 'cancel')):
            raise UserError(_('El documento terminado conserva sus condiciones. Prepare una corrección vinculada.'))
        if 'picking_type_id' in values and any(p.arg_identity_id and p.picking_type_id.id != values['picking_type_id'] for p in self):
            raise UserError(_('El documento conserva su tipo y código. Prepare otro movimiento.'))
        return super().write(values)

    def _arg_demand_payload(self):
        self.ensure_one()
        products = {}
        for move in self.move_ids.filtered(lambda m: m.state != 'cancel' and m.product_id and m.uom_id):
            key = str(move.product_id.id)
            row = products.setdefault(key, {'label': move.product_id.display_name, 'unit': move.product_id.uom_id.display_name,
                                            'rounding': move.product_id.uom_id.rounding, 'target': 0})
            row['target'] += move.uom_id._compute_quantity(move.product_uom_qty, move.product_id.uom_id, round=False)
        return {'products': products, 'company': self.company_id.name,
                'partner': self.partner_id.name or '', 'address': self.partner_id.contact_address or ''}

    def _arg_capture_demand(self):
        for picking in self.filtered(lambda p: not p.arg_demand_snapshot):
            picking.check_access('write')
            super(StockPicking, picking).write({'arg_demand_snapshot': picking._arg_demand_payload()})

    def button_validate(self):
        _manager(self.env)
        for picking in self:
            picking._arg_check_document_access()
        # Prepare first, so native draft validation cannot silently replace a zero actual quantity by its full demand.
        draft = self.filtered(lambda p: p.state == 'draft')
        if draft:
            result = draft.action_confirm()
            if result is not True:
                return result
        return super().button_validate()

    def action_cancel(self):
        _manager(self.env)
        self._arg_capture_demand()
        return super(StockPicking, self.with_context(_arg_move_engine=_MOVE_ENGINE)).action_cancel()

    def action_return(self):
        self.ensure_one()
        self._arg_check_document_access()
        self.check_access('write')
        if self.state != 'done':
            raise UserError(_('La devolución se prepara desde un movimiento validado.'))
        action = super().action_return()
        action['views'] = [(self.env.ref('arg_pyme_stock.picking_form').id, 'form')]
        return action

    def _arg_family(self):
        family = self
        frontier = self
        while frontier:
            frontier = frontier.backorder_ids - family
            family |= frontier
        return family

    @api.depends('write_date', 'state', 'move_ids.quantity', 'move_ids.product_uom_qty', 'move_ids.uom_id', 'move_ids.product_id', 'move_ids.state', 'backorder_ids.state')
    def _compute_arg_completion_axes(self):
        super()._compute_arg_completion_axes()

    def _arg_get_completion_axes(self):
        # A prepared document already has known demand. Read it without freezing history;
        # the immutable snapshot is still captured only before a physical effect/cancellation.
        snap = self.arg_demand_snapshot or self._arg_demand_payload()
        family = self._arg_family()
        rows = []
        for product_id, raw in snap['products'].items():
            moves = family.move_ids.filtered(lambda m: m.product_id.id == int(product_id))
            done = sum(m.uom_id._compute_quantity(m.quantity, m.product_id.uom_id, round=False) for m in moves if m.state == 'done')
            frontier, visited, sign = moves.returned_move_ids, moves, -1
            while frontier:
                frontier -= visited
                visited |= frontier
                done += sign * sum(m.uom_id._compute_quantity(m.quantity, m.product_id.uom_id, round=False)
                                   for m in frontier if m.state == 'done' and m.product_id.id == int(product_id))
                frontier = frontier.returned_move_ids - visited
                sign *= -1
            row = dict(raw, done=done)
            row['closed'] = sum(moves.mapped('arg_closed_quantity_base'))
            rows.append(row)
        axes = [self._arg_axis('Cantidades y pendientes del documento', rows)]
        if self._arg_document_code() in ('REM', 'ENT'):
            axes.append(self._arg_unknown_axis('Facturación vinculada',
                _('La relación nativa de factura es con el pedido, no con esta entrega/recepción específica. Consulte los documentos relacionados; no se atribuyen cantidades facturadas a este movimiento sin evidencia directa.')))
        return axes

    def _arg_document_relations(self):
        result = super()._arg_document_relations()
        for label, records in [('Pendiente de', self.backorder_id), ('Pendientes derivados', self.backorder_ids),
                               ('Devolución de', self.return_id), ('Devoluciones', self.return_ids)]:
            if records:
                result.append({'label': label, 'records': records})
        return result

    def _arg_report_payload(self):
        snap = self.arg_demand_snapshot or {}
        return {'title': self.arg_document_type_id.name or 'Movimiento ARG', 'company': snap.get('company') or self.company_id.name,
                'date': str(self.date_done or self.scheduled_date), 'state_label': dict(self._fields['state']._description_selection(self.env)).get(self.state),
                'partner_name': snap.get('partner') or self.partner_id.name or '', 'partner_address': snap.get('address') or '',
                'external_reference': self.origin or self.arg_reference, 'currency': '',
                'lines': [{'description': move.product_id.display_name,
                           'quantity': move.quantity if move.state == 'done' else move.product_uom_qty,
                           'unit': move.uom_id.display_name, 'unit_price': '', 'total': ''} for move in self.move_ids if move.state != 'cancel'],
                'totals': [], 'notes': 'Las cantidades de diferentes productos y unidades no se suman. Sin efecto fiscal.'}


class StockMove(models.Model):
    _inherit = 'stock.move'
    arg_inventory_adjustment_id = fields.Many2one('arg.pyme.inventory.adjustment', readonly=True, copy=False, check_company=True)
    arg_closed_quantity_base = fields.Float(readonly=True, copy=False, string='Faltante cerrado en unidad base')

    @api.model_create_multi
    def create(self, vals_list):
        from .stock_quant import _INVENTORY_ENGINE
        context = self.env.context.get('_arg_inventory_engine')
        inventory = isinstance(context, tuple) and len(context) == 2 and context[0] is _INVENTORY_ENGINE
        for values in vals_list:
            picking = self.env['stock.picking'].browse(values.get('picking_id') or self.env.context.get('default_picking_id'))
            if picking.state in ('done', 'cancel') and self.env.context.get('_arg_move_engine') is not _MOVE_ENGINE:
                raise UserError(_('No agregue movimientos a un documento terminado.'))
            if values.get('arg_closed_quantity_base') or self.env.context.get('default_arg_closed_quantity_base'):
                raise AccessError(_('El faltante se registra mediante el cierre nativo.'))
            if (values.get('arg_inventory_adjustment_id') or self.env.context.get('default_arg_inventory_adjustment_id')) and not inventory:
                raise AccessError(_('El ajuste se recibe desde un inventario validado.'))
            if values.get('state', self.env.context.get('default_state')) in ('done', 'cancel'):
                raise AccessError(_('El movimiento se finaliza mediante el motor nativo.'))
        return super().create(vals_list)

    def write(self, values):
        if 'arg_inventory_adjustment_id' in values:
            raise AccessError(_('El ajuste de origen no se cambia.'))
        if self.env.context.get('_arg_move_engine') is not _MOVE_ENGINE:
            if 'arg_closed_quantity_base' in values:
                raise AccessError(_('El faltante cerrado se conserva.'))
            if values.get('state') in ('done', 'cancel') or ('state' in values and self.filtered(lambda m: m.state in ('done', 'cancel') and m.state != values['state'])):
                raise AccessError(_('Use validación o cancelación del circuito.'))
            if {'quantity', 'product_uom_qty', 'product_id', 'uom_id', 'location_id', 'location_dest_id', 'picking_id', 'origin_returned_move_id', 'to_refund'} & values.keys() and self.filtered(lambda m: m.state in ('done', 'cancel')):
                raise UserError(_('Conserve el movimiento validado y prepare una devolución o ajuste vinculado.'))
            if values.get('picking_id') and self.env['stock.picking'].browse(values['picking_id']).state in ('done', 'cancel'):
                raise UserError(_('El destino del movimiento no puede ser un documento terminado.'))
        return super().write(values)

    def _action_done(self, *args, **kwargs):
        _manager(self.env)
        self.picking_id._arg_capture_demand()
        cancel_backorder = args[0] if args else kwargs.get('cancel_backorder', False)
        closed = {m.id: m.uom_id._compute_quantity(max(0, m.product_uom_qty - m.quantity), m.product_id.uom_id, round=False)
                  for m in self if cancel_backorder and m.state not in ('done', 'cancel')}
        originals = self.origin_returned_move_id.sorted('id')
        for original in originals:
            original.check_access('read')
            original.flush_recordset(['write_date'])
            self.env.cr.execute('UPDATE stock_move SET write_date=clock_timestamp() WHERE id=%s', [original.id])
            original.invalidate_recordset(['write_date'])
            returns = self.filtered(lambda m: m.origin_returned_move_id == original and m.state not in ('done', 'cancel'))
            used = original.returned_move_ids.filtered(lambda m: m.state == 'done' and m not in self)
            if original.state != 'done' or any(m.product_id != original.product_id or m.company_id != original.company_id for m in returns):
                raise UserError(_('Revise producto, compañía y movimiento original validado de la devolución.'))
            qty = sum(m.uom_id._compute_quantity(m.quantity, original.uom_id, round=False) for m in used | returns)
            if original.uom_id.compare(qty, original.quantity) > 0:
                raise UserError(_('La devolución supera la cantidad efectivamente movida todavía disponible.'))
        moves = super(StockMove, self.with_context(_arg_move_engine=_MOVE_ENGINE))._action_done(*args, **kwargs)
        for move in self.exists():
            if closed.get(move.id):
                super(StockMove, move).write({'arg_closed_quantity_base': max(move.arg_closed_quantity_base, closed[move.id])})
        return moves.with_context(_arg_move_engine=None)

    def _action_cancel(self, *args, **kwargs):
        _manager(self.env)
        self.picking_id._arg_capture_demand()
        for move in self.filtered(lambda m: m.state not in ('done', 'cancel')):
            super(StockMove, move).write({'arg_closed_quantity_base': move.uom_id._compute_quantity(move.product_uom_qty, move.product_id.uom_id, round=False)})
        return super(StockMove, self.with_context(_arg_move_engine=_MOVE_ENGINE))._action_cancel(*args, **kwargs)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('_arg_move_engine') is not _MOVE_ENGINE:
            moves = self.env['stock.move'].browse(list({v.get('move_id') or self.env.context.get('default_move_id') for v in vals_list} - {None, False}))
            pickings = self.env['stock.picking'].browse(list({v.get('picking_id') or self.env.context.get('default_picking_id') for v in vals_list} - {None, False}))
            if moves.filtered(lambda move: move.state in ('done', 'cancel')) or pickings.filtered(lambda picking: picking.state in ('done', 'cancel')) or any(v.get('state', self.env.context.get('default_state')) in ('done', 'cancel') for v in vals_list):
                raise UserError(_('No agregue detalles a un movimiento validado. Prepare una corrección vinculada.'))
        return super().create(vals_list)

    def write(self, values):
        if 'state' in values and self.env.context.get('_arg_move_engine') is not _MOVE_ENGINE:
            raise AccessError(_('El estado del detalle proviene de su movimiento.'))
        if self.env.context.get('_arg_move_engine') is not _MOVE_ENGINE and self.filtered(lambda line: line.move_id.state in ('done', 'cancel') or line.picking_id.state in ('done', 'cancel')) and {'quantity', 'product_id', 'uom_id', 'location_id', 'location_dest_id', 'lot_id', 'owner_id', 'package_id', 'result_package_id', 'move_id', 'picking_id', 'company_id', 'quant_id'} & values.keys():
            raise UserError(_('Conserve el detalle validado y prepare una corrección vinculada.'))
        if self.env.context.get('_arg_move_engine') is not _MOVE_ENGINE:
            if values.get('move_id') and self.env['stock.move'].browse(values['move_id']).state in ('done', 'cancel'):
                raise UserError(_('El detalle no se reasigna a un movimiento terminado.'))
            if values.get('picking_id') and self.env['stock.picking'].browse(values['picking_id']).state in ('done', 'cancel'):
                raise UserError(_('El detalle no se reasigna a un documento terminado.'))
        return super().write(values)

    def unlink(self):
        if self.filtered(lambda line: line.state == 'done'):
            raise UserError(_('El detalle validado se conserva.'))
        return super().unlink()
