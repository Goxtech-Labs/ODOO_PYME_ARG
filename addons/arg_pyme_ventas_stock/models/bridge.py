from odoo import api, models, _
from odoo.exceptions import AccessError, UserError

class CommercialOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('write_date', 'order_line.qty_delivered', 'order_line.move_ids.state', 'order_line.move_ids.arg_closed_quantity_base')
    def _compute_arg_completion_axes(self):
        super()._compute_arg_completion_axes()

    def _arg_get_completion_axes(self):
        rows = []
        for line in self.order_line.filtered(lambda row: not row.display_type and row.product_id.type == 'consu'):
            moves = line.move_ids.filtered(lambda move: not move.origin_returned_move_id and move.product_id == line.product_id)
            forward = moves.filtered(lambda move: move.location_dest_id._is_outgoing() and move.location_dest_id.usage != 'inventory') if 'sale' == 'sale' else moves.filtered(lambda move: move.location_id.usage == 'supplier' and move.location_dest_id.usage != 'supplier')
            remaining_open = sum(move.uom_id._compute_quantity(move.product_uom_qty, line.product_uom_id, round=False) for move in forward if move.state not in ('done','cancel'))
            closed_base = sum(moves.mapped('arg_closed_quantity_base'))
            closed = line.product_id.uom_id._compute_quantity(closed_base, line.product_uom_id, round=False)
            closed = min(closed, max(0, line.product_uom_qty - line.qty_delivered - remaining_open))
            rows.append({'label': line.name, 'unit': line.product_uom_id.display_name, 'rounding': line.product_uom_id.rounding,
                         'target': line.product_uom_qty, 'done': line.qty_delivered, 'closed': closed})
        return [self._arg_axis('Entrega', rows)] + super()._arg_get_completion_axes()

    def action_arg_physical_documents(self):
        self._arg_check_document_access()
        return {'type':'ir.actions.act_window','name':'Movimientos ARG','res_model':'stock.picking',
                'view_mode':'list,form','domain':[('id','in',self.order_line.move_ids.picking_id.ids)],
                'views':[(self.env.ref('arg_pyme_stock.picking_list').id,'list'),(self.env.ref('arg_pyme_stock.picking_form').id,'form')]}

    def _arg_document_relations(self):
        return super()._arg_document_relations() + [{'label':'Movimientos físicos','records':self.order_line.move_ids.picking_id}]

    def _arg_document_line_relations(self):
        result = super()._arg_document_line_relations()
        for line in self.order_line:
            for move in line.move_ids.filtered('picking_id'):
                result.append({'source_document':self,'source_line':line,'target_document':move.picking_id,'target_line':move,
                               'quantity':move.quantity if move.state == 'done' else move.product_uom_qty,'unit':move.uom_id.display_name})
        return result

class PhysicalDocument(models.Model):
    _inherit = 'stock.picking'

    def _arg_document_relations(self):
        orders = self.move_ids.sale_line_id.order_id
        return super()._arg_document_relations() + [{'label':'Pedidos origen','records':orders},
                                                   {'label':'Facturas de pedidos relacionados (sin atribución al movimiento)','records':orders.invoice_ids}]

class AccountingDocument(models.Model):
    _inherit = 'account.move'

    def _arg_document_relations(self):
        result = super()._arg_document_relations()
        if self.move_type in ('out_invoice','out_refund'):
            result.append({'label':'Movimientos de pedidos origen','records':self.invoice_line_ids.sale_line_ids.move_ids.picking_id})
        return result

class PhysicalMove(models.Model):
    _inherit = 'stock.move'

    def write(self, values):
        if 'sale_line_id' in values and any(move.sale_line_id.id != values['sale_line_id'] for move in self):
            raise UserError(_('El movimiento conserva su línea comercial de origen. Prepare otro movimiento si corresponde.'))
        return super().write(values)

    def _arg_validate_sale_origin(self):
        for move in self.filtered('sale_line_id'):
            line = move.sale_line_id
            line.check_access('read')
            order = line.order_id
            if move.company_id != order.company_id or move.product_id != line.product_id:
                raise UserError(_('El movimiento conserva producto y compañía del documento de origen.'))
            if order.state != 'sale' and not move.origin_returned_move_id:
                raise UserError(_('El movimiento requiere un pedido confirmado o una devolución vinculada.'))
            if order.arg_commitment_released:
                raise UserError(_('El compromiso anterior fue liberado. No se reactivan sus movimientos.'))

    def _arg_lock_sale_origin(self):
        self.check_access('write')
        if any(move.company_id not in self.env.companies for move in self):
            raise AccessError(_('Compañía no habilitada.'))
        if not self:
            return
        self.flush_recordset(['sale_line_id', 'company_id'])
        # Metadata-only serialization, authorized by the native movement. No sudo/read of hidden business values.
        self.env.cr.execute("SELECT DISTINCT q.commercial_root_id FROM stock_move m JOIN sale_order_line l ON l.id=m.sale_line_id JOIN sale_order o ON o.id=l.order_id JOIN arg_pyme_quotation q ON q.id=o.arg_quotation_id WHERE m.id IN %s AND o.company_id=m.company_id ORDER BY q.commercial_root_id", [tuple(self.ids)])
        for root_id, in self.env.cr.fetchall():
            self.env.cr.execute('UPDATE arg_pyme_quotation SET write_date=clock_timestamp() WHERE id=%s', [root_id])
            self.env['arg.pyme.quotation'].browse(root_id).invalidate_recordset(['write_date'])

    def _action_done(self, *args, **kwargs):
        self._arg_validate_sale_origin()
        self._arg_lock_sale_origin()
        return super()._action_done(*args, **kwargs)

    def _action_cancel(self, *args, **kwargs):
        self._arg_lock_sale_origin()
        return super()._action_cancel(*args, **kwargs)
