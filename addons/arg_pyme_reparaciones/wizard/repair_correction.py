import uuid
from odoo import api, fields, models, _
from odoo.exceptions import AccessError
from ..models.repair_correction import CORRECTION_FIELDS


class CorrectionWizard(models.TransientModel):
    _name = 'arg.pyme.repair.correction.wizard'
    _description = 'Corrección de recepción / diagnóstico ARG'

    case_id = fields.Many2one('arg.pyme.repair.case', required=True, readonly=True, ondelete='cascade')
    request_key = fields.Char(required=True, readonly=True, copy=False)
    snapshot = fields.Json(required=True, readonly=True)
    partner_label = fields.Char(readonly=True)
    date = fields.Date(required=True, default=fields.Date.context_today, string='Fecha de corrección')
    field_name = fields.Selection(CORRECTION_FIELDS, required=True, default='equipment', string='Dato a corregir')
    current_value = fields.Text(compute='_compute_current_value', string='Valor al abrir')
    new_text = fields.Text(string='Nuevo valor')
    new_partner_id = fields.Many2one('res.partner', string='Nuevo cliente')
    new_date = fields.Date(string='Nueva fecha de recepción')
    clear_value = fields.Boolean(string='Dejar este dato opcional vacío')
    reason = fields.Text(required=True, string='Motivo')

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        for raw in vals_list:
            values = dict(raw)
            case = self.env['arg.pyme.repair.case'].browse(values['case_id'])
            case._correction_check()
            case._lock()
            values.update(request_key=uuid.uuid4().hex, snapshot=case._correction_snapshot(),
                          partner_label=case.partner_id.display_name)
            values.setdefault('new_partner_id', case.partner_id.id)
            values.setdefault('new_date', case.date)
            prepared.append(values)
        return super().create(prepared)

    def write(self, values):
        if {'case_id', 'request_key', 'snapshot', 'partner_label'} & values.keys():
            raise AccessError(_('La corrección conserva origen, solicitud y valores observados.'))
        return super().write(values)

    @api.depends('field_name', 'snapshot', 'partner_label')
    def _compute_current_value(self):
        for wizard in self:
            value = (wizard.snapshot or {}).get(wizard.field_name, '')
            wizard.current_value = wizard.partner_label if wizard.field_name == 'partner_id' else str(value or '')

    @api.onchange('field_name')
    def _onchange_field(self):
        self.new_text = False
        self.clear_value = False

    def action_apply(self):
        self.ensure_one()
        self.check_access('write')
        self.case_id._apply_correction(self.request_key, self.date, self.field_name,
            self.new_text or '', self.new_partner_id.id, self.new_date, self.clear_value,
            self.reason or '', self.snapshot)
        return {'type': 'ir.actions.act_window_close'}


class FollowupWizard(models.TransientModel):
    _name = 'arg.pyme.repair.followup.wizard'
    _description = 'Nueva visita de reparación ARG'

    case_id = fields.Many2one('arg.pyme.repair.case', required=True, readonly=True, ondelete='cascade')
    request_key = fields.Char(required=True, readonly=True, copy=False)
    snapshot = fields.Json(required=True, readonly=True)
    date = fields.Date(required=True, default=fields.Date.context_today, string='Fecha propuesta de recepción')
    problem = fields.Text(required=True, string='Problema de la nueva visita')

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        for raw in vals_list:
            values = dict(raw)
            case = self.env['arg.pyme.repair.case'].browse(values['case_id'])
            case._correction_check()
            case._lock()
            values.update(request_key=uuid.uuid4().hex, snapshot=case._correction_snapshot())
            prepared.append(values)
        return super().create(prepared)

    def write(self, values):
        if {'case_id', 'request_key', 'snapshot'} & values.keys():
            raise AccessError(_('El seguimiento conserva origen, solicitud y valores conocidos.'))
        return super().write(values)

    def action_prepare(self):
        self.ensure_one()
        self.check_access('write')
        case = self.case_id._prepare_followup(self.request_key, self.date, self.problem or '', self.snapshot)
        return {'type': 'ir.actions.act_window', 'res_model': case._name, 'res_id': case.id,
                'view_mode': 'form', 'views': [(self.env.ref('arg_pyme_reparaciones.repair_form').id, 'form')]}
