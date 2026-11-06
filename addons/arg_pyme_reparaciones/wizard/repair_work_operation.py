import uuid
from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class WorkOperation(models.TransientModel):
    _name = 'arg.pyme.repair.work.operation'
    _description = 'Autorización / entrega de reparación ARG'

    case_id = fields.Many2one('arg.pyme.repair.case', required=True, readonly=True, ondelete='cascade')
    mode = fields.Selection([('authorize', 'Autorizar pedido'), ('ready', 'Trabajo listo'),
                             ('resume', 'Retomar trabajo'), ('deliver', 'Entregar equipo reparado')],
                            required=True, readonly=True)
    request_key = fields.Char(required=True, readonly=True, copy=False)
    date = fields.Date(required=True, default=fields.Date.context_today, string='Fecha efectiva')
    order_id = fields.Many2one('sale.order', string='Pedido de trabajo')
    authorized_by = fields.Char(string='Autoriza el cliente')
    coverage = fields.Selection([('paid', 'A cargo del cliente'), ('warranty', 'Garantía declarada'),
                                 ('mixed', 'Cobertura mixta')], required=True, default='paid', string='Cobertura')
    reference = fields.Text(string='Constancia / motivo')
    recipient = fields.Char(string='Retira')

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        for raw in vals_list:
            values = dict(raw)
            case = self.env['arg.pyme.repair.case'].browse(values['case_id'])
            case._commercial_check(manager=True)
            values['request_key'] = uuid.uuid4().hex
            if values.get('mode') == 'authorize':
                pending = case._orders().filtered(lambda order: order.state in ('draft', 'sent', 'sale')
                    and not order.arg_commitment_released and order not in case.authorization_ids.order_id)
                if len(pending) == 1:
                    values.setdefault('order_id', pending.id)
            prepared.append(values)
        return super().create(prepared)

    def write(self, values):
        if {'case_id', 'mode', 'request_key'} & values.keys():
            raise AccessError(_('La operación conserva parte, tipo y clave de reintento.'))
        return super().write(values)

    def action_apply(self):
        self.ensure_one()
        self.check_access('write')
        if self.mode == 'authorize':
            self.case_id._authorize_order(self.order_id, self.date, self.authorized_by or '',
                                          self.reference or '', self.coverage)
        else:
            self.case_id._work_transition(self.mode, self.request_key, self.date,
                                          self.reference or '', self.recipient or '')
        return {'type': 'ir.actions.act_window_close'}
