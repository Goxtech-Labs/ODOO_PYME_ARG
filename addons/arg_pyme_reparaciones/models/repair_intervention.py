import math
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.float_utils import float_compare
from odoo.addons.arg_pyme_base.tools.quantity import quantity_rounding
from .repair_event import repair_engine


class RepairIntervention(models.Model):
    _name = 'arg.pyme.repair.intervention'
    _inherit = ['arg.pyme.document.mixin']
    _description = 'Parte de trabajo ARG'
    _rec_name = 'arg_number'
    _order = 'id desc'
    _check_company_auto = True

    date = fields.Date(required=True, default=fields.Date.context_today, string='Fecha de trabajo')
    case_id = fields.Many2one('arg.pyme.repair.case', required=True, ondelete='restrict', check_company=True,
                              string='Reparación')
    company_id = fields.Many2one(related='case_id.company_id', store=True, index=True)
    partner_id = fields.Many2one(related='case_id.partner_id', string='Cliente')
    order_line_id = fields.Many2one('sale.order.line', required=True, check_company=True, ondelete='restrict',
                                    string='Trabajo / servicio del pedido')
    unit_id = fields.Many2one(related='order_line_id.product_uom_id', string='Unidad')
    quantity = fields.Float(required=True, default=1, digits='Product Unit', string='Cantidad trabajada')
    technician_id = fields.Many2one('res.users', default=lambda self: self.env.user, check_company=True,
                                    string='Realizado por')
    notes = fields.Text(string='Detalle del trabajo')
    state = fields.Selection([('draft', 'Borrador'), ('confirmed', 'Registrado'),
                              ('reversed', 'Revertido'), ('canceled', 'Cancelado')], required=True,
                             default='draft', readonly=True, copy=False, index=True, string='Estado')
    confirmed_by = fields.Many2one('res.users', readonly=True, copy=False, ondelete='restrict')
    confirmed_at = fields.Datetime(readonly=True, copy=False)
    reversed_by = fields.Many2one('res.users', readonly=True, copy=False, ondelete='restrict')
    reversed_on = fields.Date(readonly=True, copy=False)
    reversal_reason = fields.Text(readonly=True, copy=False)

    def _arg_document_code(self):
        return 'PTM'

    @api.model
    def _effect_fields(self):
        return {'state', 'confirmed_by', 'confirmed_at', 'reversed_by', 'reversed_on', 'reversal_reason'}

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        for raw in vals_list:
            values = dict(raw)
            effective = self.default_get(list(self._effect_fields()) + ['case_id'])
            effective.update(values)
            if effective.get('state') != 'draft' or any(effective.get(name) for name in self._effect_fields() - {'state'}):
                raise AccessError(_('El parte de trabajo empieza en borrador.'))
            case = self.env['arg.pyme.repair.case'].browse(effective.get('case_id'))
            case._commercial_check()
            case._lock()
            if case.state != 'in_progress':
                raise UserError(_('Iniciá el trabajo antes de cargar su parte.'))
            values['company_id'] = case.company_id.id
            prepared.append(values)
        return super().create(prepared)

    def _lock(self):
        self.ensure_one()
        self.check_access('write')
        self._arg_check_document_access()
        self.case_id._commercial_check()
        self.case_id._lock()
        self.invalidate_recordset()

    def write(self, values):
        if self._effect_fields() & values.keys() or {'case_id', 'company_id'} & values.keys():
            raise AccessError(_('El origen y los hechos del trabajo se conservan.'))
        for log in self.sorted('id'):
            log._lock()
            if log.state != 'draft' or log.case_id.state != 'in_progress':
                raise UserError(_('Sólo se edita un parte en borrador durante el trabajo.'))
        return super().write(values)

    @api.constrains('order_line_id', 'case_id', 'quantity')
    def _check_line_quantity(self):
        for log in self:
            line = log.order_line_id
            line.check_access('read')
            if line.order_id.arg_repair_case_id != log.case_id or line.display_type or line.product_id.type != 'service':
                raise ValidationError(_('Elegí un servicio del pedido de esta reparación.'))
            if line.qty_delivered_method != 'manual':
                raise ValidationError(_('Este parte registra servicios con cantidad manual; no sustituye analítica ni partes de horas nativos.'))
            if not math.isfinite(log.quantity) or log.quantity <= 0:
                raise ValidationError(_('La cantidad trabajada debe ser positiva y finita.'))

    def _native_total(self, exclude=None):
        logs = self.case_id.worklog_ids.filtered(lambda log: log.order_line_id == self.order_line_id and log.state == 'confirmed')
        if exclude:
            logs -= exclude
        return sum(logs.mapped('quantity'))

    def _check_native_total(self):
        if float_compare(self.order_line_id.qty_delivered, self._native_total(),
                         precision_rounding=quantity_rounding(self.env)):
            raise UserError(_('La cantidad nativa no coincide con los partes registrados. Revisá su origen antes de continuar.'))

    def action_confirm_work(self):
        self._lock()
        self.case_id._commercial_check(manager=True)
        if self.state == 'confirmed':
            return True
        if self.state != 'draft' or self.case_id.state != 'in_progress':
            raise UserError(_('El parte no está disponible para registrar trabajo.'))
        self.case_id._check_order(self.order_line_id.order_id, confirmed=True)
        if not self.date or self.date < self.case_id.date or self.date > fields.Date.context_today(self):
            raise UserError(_('Indicá la fecha efectiva del trabajo, no futura ni anterior a la recepción.'))
        self._check_line_quantity()
        self._check_native_total()
        total = self._native_total() + self.quantity
        if float_compare(total, self.order_line_id.product_uom_qty, precision_rounding=quantity_rounding(self.env)) > 0:
            raise UserError(_('El trabajo supera la cantidad autorizada; prepará y autorizá el alcance adicional.'))
        repair_engine(self.order_line_id).write({'qty_delivered': total})
        super(RepairIntervention, self).write({'state': 'confirmed', 'confirmed_by': self.env.uid,
                                              'confirmed_at': fields.Datetime.now()})
        return True

    def action_cancel_draft(self):
        self._lock()
        if self.state == 'canceled':
            return True
        if self.state != 'draft':
            raise UserError(_('El trabajo registrado se revierte con constancia, no se cancela como borrador.'))
        return super(RepairIntervention, self).write({'state': 'canceled'})

    def action_reverse_work(self):
        self._lock()
        self.case_id._commercial_check(manager=True)
        if self.state != 'confirmed':
            raise UserError(_('Sólo se revierte un parte registrado.'))
        wizard = repair_engine(self.env['arg.pyme.repair.work.reverse']).create({'worklog_id': self.id})
        return {'type': 'ir.actions.act_window', 'res_model': wizard._name, 'res_id': wizard.id,
                'view_mode': 'form', 'target': 'new', 'name': _('Revertir trabajo registrado')}

    def _reverse_work(self, date, reason):
        self._lock()
        self.case_id._commercial_check(manager=True)
        date = fields.Date.to_date(date)
        reason = reason.strip()
        if self.state == 'reversed':
            if self.reversed_on == date and self.reversal_reason == reason:
                return True
            raise UserError(_('El parte ya fue revertido con otra constancia.'))
        if self.state != 'confirmed' or self.case_id.state not in ('in_progress', 'ready', 'delivered'):
            raise UserError(_('El trabajo no admite esta reversión.'))
        if not date or date < max([self.date] + self.case_id.event_ids.mapped('effective_date')) or date > fields.Date.context_today(self) or not reason:
            raise UserError(_('Indicá fecha efectiva no anterior al último hecho y motivo.'))
        self._check_native_total()
        repair_engine(self.order_line_id).write({'qty_delivered': self._native_total(exclude=self)})
        super(RepairIntervention, self).write({'state': 'reversed', 'reversed_by': self.env.uid,
                                              'reversed_on': date, 'reversal_reason': reason})
        target = 'in_progress' if self.case_id.state == 'ready' else self.case_id.state
        return self.case_id._record('work_correction', target, date, {'part': self.id, 'reason': reason},
                                    request_key='work-reversal:' + str(self.id))

    def _arg_document_relations(self):
        return [{'label': _('Reparación'), 'records': self.case_id},
                {'label': _('Pedido de trabajo'), 'records': self.order_line_id.order_id}]

    def action_arg_print(self):
        self._arg_check_document_access()
        self.case_id._commercial_check()
        return self.env.ref('arg_pyme_reparaciones.action_report_worklog').report_action(self)
