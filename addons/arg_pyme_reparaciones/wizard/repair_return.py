from odoo import fields, models


class RepairReturn(models.TransientModel):
    _name = 'arg.pyme.repair.return.wizard'
    _description = 'Devolver equipo sin reparar ARG'

    case_id = fields.Many2one('arg.pyme.repair.case', required=True, readonly=True, ondelete='cascade')
    date = fields.Date(required=True, default=fields.Date.context_today, string='Fecha de devolución')
    recipient = fields.Char(required=True, string='Retira')
    reason = fields.Text(required=True, string='Motivo / constancia')

    def action_confirm(self):
        self.ensure_one()
        self.case_id._return_unrepaired(self.date, self.recipient or '', self.reason or '')
        return {'type': 'ir.actions.act_window_close'}
