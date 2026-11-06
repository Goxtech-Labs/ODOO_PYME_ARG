from odoo import api, models, _
from odoo.exceptions import AccessError
from odoo.addons.arg_pyme_base.tools.quantity import quantity_rounding


class RepairFacts(models.Model):
    _inherit = 'arg.pyme.repair.case'

    @api.depends('state', 'event_ids.kind', 'event_ids.order_id.state',
                 'quotation_root_id.current_revision_id', 'quotation_root_id.current_revision_id.state',
                 'quotation_root_id.current_revision_id.line_ids.accepted_target_total',
                 'quotation_root_id.current_revision_id.line_ids.target_quantity_total',
                 'event_ids.order_id.arg_commitment_released', 'event_ids.order_id.order_line.qty_delivered',
                 'event_ids.order_id.order_line.qty_invoiced_posted', 'event_ids.order_id.invoice_ids.state',
                 'event_ids.order_id.invoice_ids.amount_residual', 'worklog_ids.state')
    def _compute_arg_completion_axes(self):
        super()._compute_arg_completion_axes()

    def _arg_get_completion_axes(self):
        axes = super()._arg_get_completion_axes()
        orders = self.event_ids.filtered(lambda event: event.kind == 'order').mapped('order_id')
        commercial_access = self.env.user.has_group('arg_pyme_base.group_ventas') and orders.has_access('read')
        if self.quotation_root_id:
            if commercial_access and self.quotation_root_id.has_access('read'):
                quote = self.quotation_root_id.current_revision_id
                if quote.has_access('read'):
                    for axis in quote._arg_get_completion_axes():
                        axes.append(dict(axis, label='%s · %s' % (quote.arg_number, axis['label'])))
                else:
                    axes.append(self._arg_unknown_axis(_('Presupuesto vigente'), _('Falta acceso a la revisión vigente.')))
            else:
                axes.append(self._arg_unknown_axis(_('Presupuesto y compromisos'), _('Falta acceso comercial completo.')))
        if not orders:
            return axes
        if not commercial_access:
            return axes + [self._arg_unknown_axis(_('Trabajo y documentos comerciales'),
                _('La consulta comercial requiere sus permisos. La custodia se muestra por separado.'))]
        rows = []
        for order in orders:
            for line in order.order_line.filtered(lambda row: not row.display_type and not row.is_downpayment):
                try:
                    actual = line._arg_repair_stock_quantity() if line.product_id.type == 'consu' else sum(
                        self.worklog_ids.filtered(lambda log: log.order_line_id == line and log.state == 'confirmed').mapped('quantity'))
                except AccessError:
                    return axes + [self._arg_unknown_axis(_('Trabajo y repuestos'),
                        _('Faltan permisos para verificar sus fuentes nativas completas.'))]
                rows.append({'label': '%s · %s' % (order.arg_number, line.name),
                             'unit': line.product_uom_id.display_name, 'rounding': quantity_rounding(self.env),
                             'target': line.product_uom_qty, 'done': actual,
                             'closed': max(0, line.product_uom_qty - actual)
                             if order.state == 'cancel' and order.arg_commitment_released else 0})
        axes.append(self._arg_axis(_('Trabajo y repuestos'), rows))
        # Keep order/currency scope. No sum or implicit allocation of cash across orders.
        for order in orders:
            for axis in order._arg_get_completion_axes():
                if axis['label'] != 'Entrega':
                    axes.append(dict(axis, label='%s · %s' % (order.arg_number, axis['label'])))
        return axes

    def action_repair_stock(self):
        self._arg_check_document_access()
        self._check_repair_role()
        if not self.env.user.has_group('arg_pyme_base.group_stock'):
            raise AccessError(_('La consulta requiere Stock ARG.'))
        pickings = self._orders().order_line.move_ids.picking_id
        pickings.check_access('read')
        return {'type': 'ir.actions.act_window', 'res_model': 'stock.picking',
                'name': _('Repuestos: entregas y devoluciones'), 'view_mode': 'list,form',
                'domain': [('id', 'in', pickings.ids)], 'context': {'create': False},
                'views': [(self.env.ref('arg_pyme_stock.picking_list').id, 'list'),
                          (self.env.ref('arg_pyme_stock.picking_form').id, 'form')]}

    def action_repair_invoices(self):
        self._commercial_check()
        invoices = self._orders().invoice_ids
        invoices.check_access('read')
        return {'type': 'ir.actions.act_window', 'res_model': 'account.move', 'view_mode': 'list,form',
                'name': _('Facturas y notas vinculadas'), 'domain': [('id', 'in', invoices.ids)],
                'context': {'create': False}}

    def action_new_worklog(self):
        self._commercial_check()
        self._lock()
        return {'type': 'ir.actions.act_window', 'res_model': 'arg.pyme.repair.intervention',
                'view_mode': 'form', 'context': {'default_case_id': self.id},
                'name': _('Nuevo parte de trabajo')}
