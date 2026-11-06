from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import SQL
from .repair_event import repair_engine


class RepairCase(models.Model):
    _name = 'arg.pyme.repair.case'
    _inherit = ['arg.pyme.document.mixin']
    _description = 'Parte de reparación ARG'
    _rec_name = 'arg_number'
    _order = 'id desc'
    _check_company_auto = True

    date = fields.Date(required=True, default=fields.Date.context_today, string='Fecha de recepción')
    partner_id = fields.Many2one('res.partner', required=True, check_company=True,
                                 ondelete='restrict', string='Cliente')
    equipment = fields.Char(required=True, string='Equipo recibido',
                            help='Descripción suficiente para reconocer el equipo del cliente. No crea un producto ni existencias.')
    symptom = fields.Text(required=True, string='Problema informado')
    brand = fields.Char(string='Marca')
    model = fields.Char(string='Modelo')
    serial = fields.Char(string='Número de serie')
    accessories = fields.Text(string='Accesorios recibidos')
    condition_note = fields.Text(string='Estado al recibir')
    diagnosis = fields.Text(string='Diagnóstico')
    notes = fields.Text(string='Observaciones')
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company, index=True)
    state = fields.Selection([('draft', 'Borrador'), ('received', 'Recibido'),
                              ('diagnosed', 'Diagnosticado'), ('returned', 'Devuelto sin reparar'),
                              ('canceled', 'Cancelado')], required=True, default='draft',
                             readonly=True, copy=False, index=True, string='Estado')
    event_ids = fields.One2many('arg.pyme.repair.event', 'case_id', readonly=True, copy=False,
                                string='Historial')

    def _arg_document_code(self):
        return 'REP'

    @api.model
    def _check_repair_role(self):
        if not self.env.user.has_group('arg_pyme_reparaciones.group_repair'):
            raise AccessError(_('Se requiere acceso a Reparaciones ARG.'))

    def _lock(self):
        self.ensure_one()
        self._check_repair_role()
        self._arg_check_document_access()
        self.check_access('write')
        self.flush_recordset()
        self.env.cr.execute(SQL('UPDATE %s SET write_date=clock_timestamp(), write_uid=%s WHERE id=%s',
                                SQL.identifier(self._table), self.env.uid, self.id))
        self.invalidate_recordset()

    @api.model_create_multi
    def create(self, vals_list):
        self._check_repair_role()
        for values in vals_list:
            company = self.env['res.company'].browse(values.get('company_id') or
                       self.env.context.get('default_company_id') or self.env.company.id)
            if company not in self.env.companies:
                raise AccessError(_('Compañía no habilitada.'))
            effective = self.default_get(['state', 'event_ids'])
            effective.update(values)
            if effective.get('state') != 'draft' or effective.get('event_ids') or 'event_ids' in values or 'default_event_ids' in self.env.context:
                raise AccessError(_('El parte comienza en borrador; sus hechos se registran mediante acciones.'))
        return super().create(vals_list)

    def write(self, values):
        if {'state', 'event_ids'} & values.keys():
            raise AccessError(_('Use las acciones del parte para registrar sus hechos.'))
        for record in self.sorted('id'):
            record._lock()
            if record.state in ('returned', 'canceled'):
                raise UserError(_('El parte cerrado conserva sus datos e historial.'))
            if record.state != 'draft' and {'date', 'partner_id', 'equipment', 'symptom',
                    'brand', 'model', 'serial', 'accessories', 'condition_note', 'company_id'} & values.keys():
                raise UserError(_('La recepción conserva cliente, equipo, fecha y condiciones recibidas.'))
            if record.state != 'received' and 'diagnosis' in values:
                raise UserError(_('El diagnóstico se completa después de recibir y antes de registrarlo.'))
        return super().write(values)

    @api.constrains('equipment', 'symptom')
    def _check_essential_text(self):
        for record in self:
            if not (record.equipment or '').strip() or not (record.symptom or '').strip():
                raise ValidationError(_('Indicá el equipo recibido y el problema informado.'))

    def _record(self, kind, target, effective_date, evidence):
        self.ensure_one()
        repair_engine(self.env['arg.pyme.repair.event']).create({
            'case_id': self.id, 'kind': kind, 'effective_date': effective_date,
            'recorded_at': fields.Datetime.now(), 'actor_id': self.env.uid, 'evidence': evidence,
        })
        # Private server path; normal writes cannot set state or evidence, even via RPC context.
        super(RepairCase, self).write({'state': target})
        return True

    def action_receive(self):
        self._lock()
        if self.state in ('received', 'diagnosed', 'returned'):
            return True
        if self.state != 'draft':
            raise UserError(_('Sólo se recibe un parte en borrador.'))
        if self.date > fields.Date.context_today(self):
            raise UserError(_('Una recepción efectiva no puede tener una fecha futura. Conservá el borrador hasta recibir el equipo.'))
        return self._record('receive', 'received', self.date, {
            'partner_id': self.partner_id.id, 'equipment': self.equipment, 'symptom': self.symptom,
            'brand': self.brand, 'model': self.model, 'serial': self.serial,
            'accessories': self.accessories, 'condition': self.condition_note,
        })

    def action_record_diagnosis(self):
        self._lock()
        if self.event_ids.filtered(lambda event: event.kind == 'diagnose'):
            return True
        if self.state != 'received':
            raise UserError(_('Recibí el equipo antes de registrar su diagnóstico.'))
        if not (self.diagnosis or '').strip():
            raise UserError(_('Completá el diagnóstico.'))
        return self._record('diagnose', 'diagnosed', fields.Date.context_today(self),
                            {'diagnosis': self.diagnosis})

    def action_cancel_draft(self):
        self._lock()
        if self.state == 'canceled':
            return True
        if self.state != 'draft':
            raise UserError(_('Un equipo recibido se devuelve con constancia; no se cancela su recepción.'))
        return self._record('cancel', 'canceled', fields.Date.context_today(self), {})

    def action_return_unrepaired(self):
        self._lock()
        if self.state not in ('received', 'diagnosed'):
            raise UserError(_('Sólo se devuelve un equipo recibido que continúa en custodia.'))
        return {'type': 'ir.actions.act_window', 'res_model': 'arg.pyme.repair.return.wizard',
                'view_mode': 'form', 'target': 'new', 'name': _('Devolución sin reparación'),
                'context': {'default_case_id': self.id}}

    def _return_unrepaired(self, date, recipient, reason):
        self._lock()
        evidence = {'recipient': recipient.strip(), 'reason': reason.strip()}
        date = fields.Date.to_date(date)
        previous = self.event_ids.filtered(lambda event: event.kind == 'return')
        if previous:
            if previous.effective_date == date and previous.evidence == evidence:
                return True
            raise UserError(_('La devolución ya está registrada con otra constancia.'))
        if self.state not in ('received', 'diagnosed'):
            raise UserError(_('El equipo no está pendiente de devolución.'))
        latest_date = max([self.date] + self.event_ids.mapped('effective_date'))
        if not date or date < latest_date or date > fields.Date.context_today(self) or not evidence['recipient'] or not evidence['reason']:
            raise UserError(_('Indicá una fecha efectiva no anterior al último hecho, quién retira y motivo.'))
        return self._record('return', 'returned', date, evidence)

    @api.depends('state', 'event_ids.kind')
    def _compute_arg_completion_axes(self):
        super()._compute_arg_completion_axes()

    def _arg_get_completion_axes(self):
        self.ensure_one()
        received = bool(self.event_ids.filtered(lambda event: event.kind == 'receive'))
        diagnosed = bool(self.event_ids.filtered(lambda event: event.kind == 'diagnose'))
        returned = bool(self.event_ids.filtered(lambda event: event.kind == 'return'))
        row = lambda target, done, closed=0: [{'target': target, 'done': done, 'closed': closed, 'rounding': 1}]
        return [self._arg_axis(_('Recepción'), row(int(self.state != 'canceled'), int(received))),
                self._arg_axis(_('Diagnóstico'), row(int(received), int(diagnosed), int(returned and not diagnosed))),
                self._arg_axis(_('Devolución del equipo'), row(int(received), int(returned)))]

    def action_arg_print(self):
        self._arg_check_document_access()
        self._check_repair_role()
        if not self.arg_identity_id:
            raise UserError(_('Guardá primero el parte para asignar su número.'))
        return self.env.ref('arg_pyme_reparaciones.action_report_repair').report_action(self)
