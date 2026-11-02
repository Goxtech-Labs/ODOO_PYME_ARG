import uuid
from odoo import api, fields, models, Command, _
from odoo.exceptions import AccessError, UserError


class PurchaseBillWizard(models.TransientModel):
    _name = 'arg.pyme.purchase.bill.wizard'
    _description = 'Preparar factura recibida parcial ARG'
    order_id = fields.Many2one('purchase.order', required=True, readonly=True)
    operation_key = fields.Char(required=True, readonly=True)
    line_ids = fields.One2many('arg.pyme.purchase.bill.wizard.line', 'wizard_id')

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        for raw in vals_list:
            values = dict(raw)
            order = self.env['purchase.order'].browse(values['order_id'])
            order._arg_check_document_access()
            order.check_access('write')
            if order.state != 'purchase':
                raise UserError(_('Confirme o apruebe primero el pedido.'))
            values['operation_key'] = uuid.uuid4().hex
            values['line_ids'] = [Command.create({'order_line_id': line.id, 'available': line.qty_to_invoice,
                                                  'quantity': max(0, line.qty_to_invoice)})
                                  for line in order.order_line if not line.display_type and line.qty_to_invoice > 0]
            prepared.append(values)
        return super().create(prepared)

    def write(self, values):
        if {'order_id', 'operation_key'} & values.keys():
            raise AccessError(_('La operación conserva su pedido y clave de reintento.'))
        return super().write(values)

    def action_apply(self):
        self.ensure_one()
        self.check_access('write')
        move = self.order_id._arg_prepare_bill(self.operation_key, [{'line_id': line.order_line_id.id, 'quantity': line.quantity} for line in self.line_ids])
        return {'type': 'ir.actions.act_window', 'res_model': 'account.move', 'res_id': move.id,
                'view_mode': 'form', 'views': [(self.env.ref('account.view_move_form').id, 'form')]}


class PurchaseBillWizardLine(models.TransientModel):
    _name = 'arg.pyme.purchase.bill.wizard.line'
    _description = 'Cantidad facturable parcial ARG'
    wizard_id = fields.Many2one('arg.pyme.purchase.bill.wizard', required=True, ondelete='cascade')
    order_line_id = fields.Many2one('purchase.order.line', required=True, readonly=True)
    product_id = fields.Many2one(related='order_line_id.product_id')
    uom_id = fields.Many2one(related='order_line_id.uom_id')
    available = fields.Float(string='Pendiente al abrir', readonly=True, digits='Product Unit')
    quantity = fields.Float(string='Facturar ahora', digits='Product Unit')

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            wizard = self.env['arg.pyme.purchase.bill.wizard'].browse(values['wizard_id'])
            wizard.check_access('write')
            line = self.env['purchase.order.line'].browse(values['order_line_id'])
            line.check_access('read')
            if line.order_id != wizard.order_id:
                raise AccessError(_('La línea debe pertenecer al pedido de esta operación.'))
        return super().create(vals_list)

    def write(self, values):
        if {'wizard_id', 'order_line_id', 'available'} & values.keys():
            raise AccessError(_('No cambie el origen de la cantidad.'))
        return super().write(values)
