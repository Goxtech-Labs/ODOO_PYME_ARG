import math
from odoo import models, _
from odoo.exceptions import AccessError, UserError
from odoo.addons.arg_pyme_base.tools.quantity import quantity_rounding
from odoo.tools.float_utils import float_compare
from .repair_event import repair_engine


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _arg_repair_stock_moves_now(self):
        self.ensure_one()
        self.check_access('read')
        # IDs only: prove visibility of the entire native relation before its ORM classification.
        # A hidden return must not turn a net pending quantity into a completed one.
        self.env['stock.move'].flush_model(['sale_line_id'])
        self.env.cr.execute('SELECT id FROM stock_move WHERE sale_line_id=%s', [self.id])
        all_moves = self.env['stock.move'].browse([row[0] for row in self.env.cr.fetchall()])
        if not all_moves.has_access('read'):
            raise AccessError(_('Faltan permisos para verificar todos los movimientos del repuesto.'))
        if any(move.company_id != self.company_id for move in all_moves):
            raise UserError(_('Hay movimientos cuya compañía no coincide con el pedido de reparación.'))
        current = self.with_context({key: value for key, value in self.env.context.items()
                                    if key != 'accrual_entry_date'})
        return current._get_outgoing_incoming_moves()

    def _arg_repair_stock_quantity(self):
        outgoing, incoming = self._arg_repair_stock_moves_now()
        quantity = sum(move.uom_id._compute_quantity(move.quantity, self.product_uom_id, rounding_method='HALF-UP')
                       for move in outgoing if move.state == 'done')
        for move in incoming.filtered(lambda row: row.state == 'done'):
            if (not move.origin_returned_move_id and not move.location_id._is_outgoing()
                    and self.product_uom_qty > 0 and not move.picking_id.return_id):
                continue
            quantity -= move.uom_id._compute_quantity(move.quantity, self.product_uom_id, rounding_method='HALF-UP')
        return quantity


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _arg_lock_sale_origin(self):
        result = super()._arg_lock_sale_origin()
        cases = self.sale_line_id.order_id.arg_repair_case_id
        cases._lock_commercial_roots()
        for case in cases.sorted('id'):
            case._lock()
        return result

    def _action_done(self, *args, **kwargs):
        repairs = self.filtered(lambda move: move.sale_line_id.order_id.arg_repair_case_id and move.state not in ('done', 'cancel'))
        if repairs:
            self._arg_lock_sale_origin()
        for move in repairs:
            case = move.sale_line_id.order_id.arg_repair_case_id
            if move.location_id.usage in ('inventory', 'production') or move.location_dest_id.usage in ('inventory', 'production'):
                raise UserError(_('Los repuestos del pedido usan su ruta comercial; no una baja o fabricación implícita.'))
            if move.origin_returned_move_id:
                if (move.origin_returned_move_id.sale_line_id != move.sale_line_id
                        or move.origin_returned_move_id.state != 'done' or not move.to_refund):
                    raise UserError(_('La devolución conserva el movimiento validado y actualiza las cantidades del pedido.'))
                if case.state not in ('in_progress', 'ready', 'delivered'):
                    raise UserError(_('La reparación no admite esta corrección de repuestos.'))
            else:
                case._check_order(move.sale_line_id.order_id, confirmed=True)
                if case.state != 'in_progress':
                    raise UserError(_('Iniciá el trabajo autorizado antes de registrar la salida de repuestos.'))
        for line in repairs.sale_line_id:
            outgoing, incoming = line._arg_repair_stock_moves_now()
            actual = line._arg_repair_stock_quantity()
            rounding = quantity_rounding(self.env)
            if line.qty_delivered_method != 'stock_move' or float_compare(line.qty_delivered, actual, precision_rounding=rounding):
                raise UserError(_('El cumplimiento del repuesto debe provenir de sus movimientos nativos actuales.'))
            delta = sum(move.uom_id._compute_quantity(move.quantity, line.product_uom_id, round=False)
                        for move in repairs & outgoing)
            delta -= sum(move.uom_id._compute_quantity(move.quantity, line.product_uom_id, round=False)
                         for move in repairs & incoming)
            total = actual + delta
            if not math.isfinite(total) or float_compare(total, 0, precision_rounding=rounding) < 0 or float_compare(total, line.product_uom_qty, precision_rounding=rounding) > 0:
                raise UserError(_('La cantidad neta de repuestos supera el pedido autorizado o su devolución disponible.'))
        return super(StockMove, repair_engine(self))._action_done(*args, **kwargs)
