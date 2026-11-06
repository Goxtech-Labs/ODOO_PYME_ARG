from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from .repair_event import _REPAIR_ENGINE, repair_engine


CORRECTION_FIELDS = [
    ('date', 'Fecha de recepción'), ('partner_id', 'Cliente'), ('equipment', 'Equipo'),
    ('symptom', 'Problema informado'), ('brand', 'Marca'), ('model', 'Modelo'),
    ('serial', 'Serie'), ('accessories', 'Accesorios'), ('condition_note', 'Estado al recibir'),
    ('diagnosis', 'Diagnóstico registrado'),
]
OPTIONAL_TEXT_FIELDS = {'brand', 'model', 'serial', 'accessories', 'condition_note'}


class RepairCorrection(models.Model):
    _inherit = 'arg.pyme.repair.case'

    previous_case_id = fields.Many2one('arg.pyme.repair.case', readonly=True, copy=False,
                                       check_company=True, ondelete='restrict', index=True,
                                       string='Reparación anterior')
    followup_key = fields.Char(readonly=True, copy=False, index=True)
    _followup_unique = models.Constraint('UNIQUE(previous_case_id, followup_key)', 'El seguimiento de esta solicitud ya existe.')

    @api.model_create_multi
    def create(self, vals_list):
        names = ['previous_case_id', 'followup_key']
        inherited = self.default_get(names)
        prepared = []
        for raw in vals_list:
            values = dict(raw)
            effective = dict(inherited, **values)
            requested = any(name in values or 'default_' + name in self.env.context for name in names) or any(inherited.values())
            if requested:
                if self.env.context.get('_arg_repair_engine') is not _REPAIR_ENGINE:
                    raise AccessError(_('El seguimiento se prepara desde la reparación anterior.'))
                previous = self.browse(effective.get('previous_case_id')).exists()
                if not previous or not effective.get('followup_key'):
                    raise UserError(_('El seguimiento necesita origen y clave de solicitud.'))
                previous._correction_check()
                previous._lock()
                if previous.state not in ('returned', 'delivered') or values.get('company_id') != previous.company_id.id:
                    raise UserError(_('El seguimiento conserva compañía y una reparación cuya custodia terminó.'))
            prepared.append(values)
        return super().create(prepared)

    def write(self, values):
        if {'previous_case_id', 'followup_key'} & values.keys():
            raise AccessError(_('El seguimiento conserva su origen.'))
        return super().write(values)

    def _correction_check(self):
        self.ensure_one()
        self._arg_check_document_access()
        self._check_repair_role()
        self.check_access('write')
        if not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Corregir o preparar un seguimiento requiere responsable ARG.'))

    def _correction_snapshot(self):
        self.ensure_one()
        return {name: (self[name].id if name == 'partner_id' else str(self.date) if name == 'date'
                       else self[name] or '') for name, label in CORRECTION_FIELDS}

    def action_repair_correction(self):
        self._correction_check()
        self._lock()
        if self.state in ('draft', 'canceled'):
            raise UserError(_('El borrador se edita normalmente; un borrador cancelado conserva sus datos.'))
        wizard = repair_engine(self.env['arg.pyme.repair.correction.wizard']).create({'case_id': self.id})
        return {'type': 'ir.actions.act_window', 'res_model': wizard._name, 'res_id': wizard.id,
                'view_mode': 'form', 'target': 'new', 'name': _('Corregir datos registrados')}

    def _apply_correction(self, key, date, field_name, new_text, new_partner_id, new_date, clear, reason, snapshot):
        self._correction_check()
        self._lock()
        labels = dict(CORRECTION_FIELDS)
        if field_name not in labels:
            raise UserError(_('Elegí un dato de recepción o diagnóstico.'))
        date = fields.Date.to_date(date)
        reason = reason.strip()
        if field_name == 'date':
            after = str(fields.Date.to_date(new_date)) if new_date else ''
        elif field_name == 'partner_id':
            after = new_partner_id or False
        else:
            after = '' if clear else new_text.strip()
        before = (snapshot or {}).get(field_name)
        prior = self.event_ids.filtered(lambda event: event.request_key == key)
        if prior:
            evidence = prior.evidence
            if (prior.kind == ('diagnosis_correction' if field_name == 'diagnosis' else 'receipt_correction')
                    and prior.effective_date == date and evidence.get('field') == field_name
                    and evidence.get('before') == before and evidence.get('after') == after
                    and evidence.get('reason') == reason):
                return True
            raise UserError(_('La solicitud ya corresponde a otra corrección.'))
        if self.state in ('draft', 'canceled'):
            raise UserError(_('El estado actual no permite esta corrección.'))
        if snapshot != self._correction_snapshot():
            raise UserError(_('Los datos cambiaron desde que abriste la corrección. Volvé a abrirla para revisar el valor actual.'))
        if not reason or not date or date > fields.Date.context_today(self) or date < max(self.event_ids.mapped('effective_date')):
            raise UserError(_('Indicá motivo y fecha efectiva no futura ni anterior al último hecho.'))
        if field_name in ('partner_id', 'date') and (self.quotation_root_id or self.state in ('returned', 'delivered')):
            raise UserError(_('Cliente y fecha sólo se corrigen antes del presupuesto y mientras el equipo está en custodia.'))
        if field_name == 'diagnosis' and not self.event_ids.filtered(lambda event: event.kind == 'diagnose'):
            raise UserError(_('Completá el diagnóstico en su ficha antes de registrarlo.'))
        if clear and field_name not in OPTIONAL_TEXT_FIELDS:
            raise UserError(_('Este dato no puede quedar vacío.'))
        if not after and field_name not in OPTIONAL_TEXT_FIELDS:
            raise UserError(_('Completá el nuevo valor del dato.'))
        if after == before:
            raise UserError(_('El nuevo valor es igual al actual.'))
        if field_name == 'partner_id':
            partner = self.env['res.partner'].browse(after).exists()
            partner.check_access('read')
            if not partner or (partner.company_id and partner.company_id != self.company_id):
                raise UserError(_('El cliente no está disponible en esta compañía.'))
            before_label, after_label = self.partner_id.display_name, partner.display_name
        else:
            before_label, after_label = before, after
        if field_name == 'date':
            dates = self.event_ids.filtered(lambda event: event.kind not in ('receive', 'receipt_correction', 'diagnosis_correction')).mapped('effective_date')
            if fields.Date.to_date(after) > min(dates + [date]):
                raise UserError(_('La recepción corregida no puede ser posterior a los hechos ya registrados.'))
        self._repair_update({field_name: after or False})
        return self._record('diagnosis_correction' if field_name == 'diagnosis' else 'receipt_correction',
                            self.state, date, {'field': field_name, 'field_label': labels[field_name],
                            'before': before, 'after': after, 'before_label': before_label,
                            'after_label': after_label, 'reason': reason}, request_key=key)

    def action_prepare_followup(self):
        self._correction_check()
        self._lock()
        if self.state not in ('returned', 'delivered'):
            raise UserError(_('Prepará un seguimiento después de terminar la custodia anterior.'))
        wizard = repair_engine(self.env['arg.pyme.repair.followup.wizard']).create({'case_id': self.id})
        return {'type': 'ir.actions.act_window', 'res_model': wizard._name, 'res_id': wizard.id,
                'view_mode': 'form', 'target': 'new', 'name': _('Nueva visita / seguimiento')}

    def _prepare_followup(self, key, date, problem, snapshot):
        self._correction_check()
        self._lock()
        date = fields.Date.to_date(date)
        problem = problem.strip()
        prior = self.event_ids.filtered(lambda event: event.request_key == key)
        if prior:
            if prior.kind != 'followup' or prior.evidence.get('date') != str(date) or prior.evidence.get('problem') != problem:
                raise UserError(_('La solicitud ya corresponde a otro seguimiento.'))
            case = prior.related_case_id.exists()
            if not case:
                raise UserError(_('El seguimiento registrado no está disponible.'))
            case.check_access('read')
            return case
        if self.state not in ('returned', 'delivered') or snapshot != self._correction_snapshot():
            raise UserError(_('El origen cambió o su custodia no terminó. Volvé a preparar el seguimiento.'))
        ended = self.event_ids.filtered(lambda event: event.kind in ('return', 'deliver')).mapped('effective_date')
        if not date or not ended or date < max(ended) or not problem:
            raise UserError(_('Indicá el nuevo problema y una fecha no anterior a la entrega anterior.'))
        values = {name: self[name] or False for name in ('equipment', 'brand', 'model', 'serial')}
        values.update(company_id=self.company_id.id, partner_id=self.partner_id.id, date=date,
                      symptom=problem, diagnosis=False, accessories=False, condition_note=False,
                      previous_case_id=self.id, followup_key=key, state='draft',
                      arg_identity_id=False, arg_document_type_id=False, arg_number=False,
                      notes=_('Seguimiento de %s', self.arg_number))
        case = repair_engine(self.env[self._name]).create(values)
        self._record('followup', self.state, fields.Date.context_today(self),
                     {'date': str(date), 'problem': problem, 'source_snapshot': snapshot},
                     request_key=key, related_case_id=case.id)
        return case

    def _arg_document_relations(self):
        return super()._arg_document_relations() + [
            {'label': _('Reparación anterior'), 'records': self.previous_case_id},
            {'label': _('Nuevas visitas / seguimientos'),
             'records': self.event_ids.filtered(lambda event: event.kind == 'followup').mapped('related_case_id')},
        ]
