from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class WorkReverse(models.TransientModel):
    _name = 'arg.pyme.repair.work.reverse'
    _description = 'Reversión de trabajo registrado ARG'

    worklog_id = fields.Many2one('arg.pyme.repair.intervention', required=True, readonly=True, ondelete='cascade')
    date = fields.Date(required=True, default=fields.Date.context_today, string='Fecha de corrección')
    reason = fields.Text(required=True, string='Motivo')

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            worklog = self.env['arg.pyme.repair.intervention'].browse(values['worklog_id'])
            worklog.check_access('read')
            worklog.case_id._commercial_check(manager=True)
        return super().create(vals_list)

    def write(self, values):
        if 'worklog_id' in values:
            raise AccessError(_('La reversión conserva el parte de trabajo original.'))
        return super().write(values)

    def action_apply(self):
        self.ensure_one()
        self.check_access('write')
        self.worklog_id._reverse_work(self.date, self.reason or '')
        return {'type': 'ir.actions.act_window_close'}
