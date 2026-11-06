import hashlib
import json
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from odoo.tools import SQL
from odoo.addons.arg_pyme_base.tools.quantity import quantity_rounding
from odoo.tools.float_utils import float_compare
from .repair_event import _REPAIR_ENGINE, repair_engine


def order_signature(order):
    return hashlib.sha256(json.dumps({
        'id': order.id, 'company': order.company_id.id, 'partner': order.partner_id.id,
        'currency': order.currency_id.id, 'quotation': order.arg_quotation_id.id,
        'lines': [{'id': line.id, 'product': line.product_id.id, 'unit': line.product_uom_id.id,
                   'quantity': line.product_uom_qty, 'price': line.price_unit,
                   'discount': line.discount, 'taxes': sorted(line.tax_ids.ids)}
                  for line in order.order_line.sorted('id') if not line.display_type],
    }, sort_keys=True).encode()).hexdigest()


class RepairCase(models.Model):
    _inherit = 'arg.pyme.repair.case'

    quotation_root_id = fields.Many2one('arg.pyme.quotation', readonly=True, copy=False,
                                        check_company=True, ondelete='restrict', string='Presupuesto origen')
    current_quotation_id = fields.Many2one(related='quotation_root_id.current_revision_id',
                                           compute_sudo=False, string='Presupuesto vigente',
                                           groups='arg_pyme_base.group_ventas')
    authorization_ids = fields.One2many('arg.pyme.repair.authorization', 'case_id', readonly=True,
                                        copy=False, string='Autorizaciones')
    worklog_ids = fields.One2many('arg.pyme.repair.intervention', 'case_id', readonly=True,
                                  copy=False, string='Partes de trabajo')
    state = fields.Selection(selection_add=[('authorized', 'Autorizado'), ('in_progress', 'En trabajo'),
                                             ('ready', 'Listo para entregar'), ('delivered', 'Entregado reparado')],
                              ondelete={'authorized': 'set default', 'in_progress': 'set default',
                                        'ready': 'set default', 'delivered': 'set default'})
    _quotation_unique = models.Constraint('UNIQUE(quotation_root_id)', 'El presupuesto ya pertenece a otro parte.')

    def _lock_commercial_roots(self):
        for case in self:
            case._arg_check_document_access()
            case._check_repair_role()
            case.check_access('write')
        # Root metadata first, then case. No financial reads/writes or sudo for a receptionist.
        for root in self.mapped('quotation_root_id').sorted('id'):
            self.env.cr.execute('UPDATE arg_pyme_quotation SET write_date=clock_timestamp(),write_uid=%s WHERE id=%s',
                                [self.env.uid, root.id])
            root.invalidate_recordset(['write_date', 'write_uid'])

    def _lock(self):
        self.ensure_one()
        self._lock_commercial_roots()
        return super()._lock()

    @api.model_create_multi
    def create(self, vals_list):
        protected = {'quotation_root_id', 'current_quotation_id', 'authorization_ids', 'worklog_ids'}
        defaults = self.default_get(list(protected))
        if any(defaults.values()) or any('default_' + name in self.env.context for name in protected):
            raise AccessError(_('Los vínculos de reparación se generan mediante sus acciones.'))
        if any(protected & values.keys() for values in vals_list):
            raise AccessError(_('No se precargan presupuesto, autorizaciones ni trabajo realizado.'))
        return super().create(vals_list)

    def write(self, values):
        if {'quotation_root_id', 'current_quotation_id', 'authorization_ids', 'worklog_ids'} & values.keys():
            raise AccessError(_('Conserve los vínculos y use las acciones de reparación.'))
        self._lock_commercial_roots()
        return super().write(values)

    def _commercial_check(self, manager=False):
        self._arg_check_document_access()
        self._check_repair_role()
        if not self.env.user.has_group('arg_pyme_base.group_ventas'):
            raise AccessError(_('Esta operación requiere también Ventas ARG.'))
        if manager and not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('La operación requiere responsable ARG.'))

    def _orders(self):
        # Concrete native references retained by private creation events: do not search away hidden orders.
        orders = self.event_ids.filtered(lambda event: event.kind == 'order').mapped('order_id')
        orders.check_access('read')
        return orders

    def _check_order(self, order, confirmed=False, authorization=True):
        self.ensure_one()
        order.ensure_one()
        order.check_access('read')
        if (order.arg_repair_case_id != self or order.company_id != self.company_id
                or order.partner_id != self.partner_id or order not in self._orders()):
            raise UserError(_('El pedido debe provenir del presupuesto de esta reparación.'))
        if order.arg_commitment_released or order.state == 'cancel':
            raise UserError(_('El pedido está cancelado o su compromiso fue liberado.'))
        if confirmed and order.state != 'sale':
            raise UserError(_('Confirmá el pedido autorizado antes de ejecutar el trabajo.'))
        approvals = self.authorization_ids.filtered(lambda approval: approval.order_id == order)
        if authorization and not approvals:
            raise UserError(_('Registrá la autorización del cliente para este pedido.'))
        return approvals

    def action_repair_quotation(self):
        self._commercial_check()
        self._lock()
        if self.quotation_root_id:
            quote = self.quotation_root_id.current_revision_id
            quote.check_access('read')
        else:
            if self.state != 'diagnosed':
                raise UserError(_('Registrá el diagnóstico antes de preparar el presupuesto.'))
            quote = repair_engine(self.env['arg.pyme.quotation']).with_company(self.company_id).create({
                'company_id': self.company_id.id, 'partner_id': self.partner_id.id,
                'arg_repair_case_id': self.id, 'notes': self.diagnosis,
            })
            self._repair_update({'quotation_root_id': quote.id})
        return {'type': 'ir.actions.act_window', 'res_model': quote._name, 'res_id': quote.id,
                'view_mode': 'form', 'views': [(self.env.ref('arg_pyme_ventas.quotation_form').id, 'form')]}

    def action_repair_orders(self):
        self._commercial_check()
        orders = self._orders()
        return {'type': 'ir.actions.act_window', 'name': _('Pedidos de la reparación'),
                'res_model': 'sale.order', 'view_mode': 'list,form', 'domain': [('id', 'in', orders.ids)],
                'views': [(self.env.ref('arg_pyme_ventas.order_list').id, 'list'),
                          (self.env.ref('arg_pyme_ventas.order_form').id, 'form')], 'context': {'create': False}}

    def action_repair_authorize(self):
        self._commercial_check(manager=True)
        self._lock()
        if self.state not in ('diagnosed', 'authorized', 'in_progress'):
            raise UserError(_('La reparación no está disponible para autorizar trabajo.'))
        return self._open_work_operation('authorize')

    def _open_work_operation(self, mode):
        wizard = repair_engine(self.env['arg.pyme.repair.work.operation']).create({'case_id': self.id, 'mode': mode})
        return {'type': 'ir.actions.act_window', 'name': _('Operación de reparación'), 'res_model': wizard._name,
                'res_id': wizard.id, 'view_mode': 'form', 'target': 'new'}

    def _authorize_order(self, order, date, authorized_by, reference, coverage):
        self._commercial_check(manager=True)
        self._lock()
        self._check_order(order, authorization=False)
        evidence = {'authorized_by': authorized_by.strip(), 'reference': reference.strip(), 'coverage': coverage}
        previous = self.authorization_ids.filtered(lambda approval: approval.order_id == order)
        date = fields.Date.to_date(date)
        if previous:
            if (previous.date == date and previous.authorized_by == evidence['authorized_by']
                    and previous.reference == evidence['reference'] and previous.coverage == coverage):
                return True
            raise UserError(_('El pedido ya tiene otra constancia de autorización.'))
        if self.state not in ('diagnosed', 'authorized', 'in_progress'):
            raise UserError(_('No se autoriza trabajo en este estado.'))
        if not date or date < self.date or date > fields.Date.context_today(self) or not all(evidence.values()):
            raise UserError(_('Indicá fecha efectiva, quién autoriza, constancia y cobertura.'))
        if coverage not in ('paid', 'warranty', 'mixed'):
            raise UserError(_('La cobertura debe estar declarada.'))
        repair_engine(self.env['arg.pyme.repair.authorization']).create({
            'case_id': self.id, 'order_id': order.id, 'date': date, **evidence,
            'actor_id': self.env.uid, 'terms_hash': order_signature(order), 'terms_snapshot': order.arg_quote_snapshot,
        })
        return self._record('authorize', self.state if self.state == 'in_progress' else 'authorized', date,
                            evidence, request_key='authorize:' + str(order.id), order_id=order.id)

    def action_start_work(self):
        self._commercial_check(manager=True)
        self._lock()
        if self.event_ids.filtered(lambda event: event.kind == 'start'):
            return True
        if self.state != 'authorized':
            raise UserError(_('Registrá la autorización antes de iniciar el trabajo.'))
        orders = self._orders().filtered(lambda order: order.state == 'sale' and not order.arg_commitment_released)
        if not orders:
            raise UserError(_('Confirmá al menos un pedido autorizado.'))
        for order in orders:
            approval = self._check_order(order, confirmed=True)
            if approval.terms_hash != order_signature(order):
                raise UserError(_('Las condiciones difieren de la autorización conservada.'))
        return self._record('start', 'in_progress', fields.Date.context_today(self), {'orders': orders.ids})

    def _check_work_complete(self):
        orders = self._orders()
        active = orders.filtered(lambda order: order.state == 'sale' and not order.arg_commitment_released)
        if not active:
            raise UserError(_('No hay un trabajo confirmado para entregar como reparado.'))
        if orders.filtered(lambda order: order.state in ('draft', 'sent') or (order.state == 'cancel' and not order.arg_commitment_released)):
            raise UserError(_('Resolvé los pedidos pendientes o cancelados sin liberar antes de cerrar el trabajo.'))
        quote = self.quotation_root_id.current_revision_id
        committed = quote._committed_map()
        if any(float_compare(line.accepted_target_total, committed.get(line.commercial_line_key, 0),
                             precision_rounding=quantity_rounding(self.env)) > 0 for line in quote.line_ids):
            raise UserError(_('Hay cantidades de presupuesto confirmadas sin pedido. Completá su alcance o prepará una revisión explícita.'))
        for order in active:
            self._check_order(order, confirmed=True)
            for line in order.order_line.filtered(lambda row: not row.display_type and not row.is_downpayment):
                actual = line.qty_delivered
                if line.product_id.type == 'service':
                    recorded = sum(self.worklog_ids.filtered(lambda log: log.order_line_id == line and log.state == 'confirmed').mapped('quantity'))
                    if line.qty_delivered_method != 'manual' or float_compare(recorded, line.qty_delivered, precision_rounding=quantity_rounding(self.env)):
                        raise UserError(_('El servicio requiere cantidades explicadas por sus partes de trabajo.'))
                elif line.product_id.type == 'consu':
                    actual = line._arg_repair_stock_quantity()
                    if line.qty_delivered_method != 'stock_move' or float_compare(actual, line.qty_delivered, precision_rounding=quantity_rounding(self.env)):
                        raise UserError(_('El repuesto requiere cumplimiento explicado por movimientos actuales.'))
                if float_compare(actual, line.product_uom_qty,
                                 precision_rounding=quantity_rounding(self.env)) < 0:
                    raise UserError(_('Faltan repuestos entregados o servicios registrados: %s', line.name))

    def action_work_ready(self):
        self._commercial_check(manager=True)
        self._lock()
        if self.state != 'in_progress':
            raise UserError(_('El trabajo debe estar en curso.'))
        return self._open_work_operation('ready')

    def action_resume_work(self):
        self._commercial_check(manager=True)
        self._lock()
        if self.state != 'ready':
            raise UserError(_('Sólo se retoma un trabajo listo aún no entregado.'))
        return self._open_work_operation('resume')

    def action_deliver_repaired(self):
        self._commercial_check(manager=True)
        self._lock()
        if self.state != 'ready':
            raise UserError(_('Marcá el trabajo listo antes de entregar el equipo reparado.'))
        return self._open_work_operation('deliver')

    def _work_transition(self, mode, key, date, reference, recipient):
        self._commercial_check(manager=True)
        self._lock()
        if mode not in ('ready', 'resume', 'deliver'):
            raise UserError(_('Operación de trabajo desconocida.'))
        evidence = {'reference': reference.strip(), 'recipient': recipient.strip() if mode == 'deliver' else ''}
        date = fields.Date.to_date(date)
        previous = self.event_ids.filtered(lambda event: event.request_key == key)
        if previous:
            return self._record(mode, self.state, date, evidence, request_key=key)
        if not date or date < max(self.event_ids.mapped('effective_date')) or date > fields.Date.context_today(self) or (mode == 'resume' and not evidence['reference']):
            raise UserError(_('Indicá fecha efectiva no anterior al último hecho; retomar trabajo requiere motivo.'))
        expected, target = {'ready': ('in_progress', 'ready'), 'resume': ('ready', 'in_progress'),
                            'deliver': ('ready', 'delivered')}[mode]
        if self.state != expected:
            raise UserError(_('El estado actual no permite esta operación.'))
        if mode in ('ready', 'deliver'):
            self._check_work_complete()
        if mode == 'deliver' and not evidence['recipient']:
            raise UserError(_('Indicá quién retira el equipo.'))
        return self._record(mode, target, date, evidence, request_key=key)

    def _return_unrepaired(self, date, recipient, reason):
        self._lock()
        if self.quotation_root_id:
            self._commercial_check(manager=True)
            orders = self._orders()
            if orders.filtered(lambda order: order.state != 'cancel' or not order.arg_commitment_released):
                raise UserError(_('Cancelá y liberá los pedidos pendientes antes de devolver sin reparar.'))
            if self.worklog_ids.filtered(lambda log: log.state == 'confirmed') or orders.order_line.filtered('qty_delivered'):
                raise UserError(_('Hay trabajo o repuestos registrados; prepará su corrección antes de devolver sin reparar.'))
        return super()._return_unrepaired(date, recipient, reason)

    def _arg_document_relations(self):
        return super()._arg_document_relations() + [
            {'label': _('Presupuesto origen'), 'records': self.quotation_root_id},
            {'label': _('Pedidos de trabajo'), 'records': self.event_ids.filtered(lambda event: event.kind == 'order').mapped('order_id')},
            {'label': _('Partes de trabajo'), 'records': self.worklog_ids},
        ]


class RepairAuthorization(models.Model):
    _name = 'arg.pyme.repair.authorization'
    _description = 'Autorización del cliente ARG'
    _check_company_auto = True
    _order = 'id desc'

    case_id = fields.Many2one('arg.pyme.repair.case', required=True, check_company=True, ondelete='restrict')
    company_id = fields.Many2one(related='case_id.company_id', store=True, index=True)
    order_id = fields.Many2one('sale.order', required=True, check_company=True, ondelete='restrict', string='Pedido autorizado')
    date = fields.Date(required=True, string='Fecha de autorización')
    authorized_by = fields.Char(required=True, string='Autoriza el cliente')
    reference = fields.Text(required=True, string='Constancia / referencia')
    coverage = fields.Selection([('paid', 'A cargo del cliente'), ('warranty', 'Garantía declarada'),
                                 ('mixed', 'Cobertura mixta')], required=True, default='paid', string='Cobertura')
    actor_id = fields.Many2one('res.users', default=lambda self: self.env.user, required=True, ondelete='restrict')
    terms_hash = fields.Char(required=True, groups='arg_pyme_base.group_ventas')
    terms_snapshot = fields.Json(required=True, groups='arg_pyme_base.group_ventas')
    _order_unique = models.Constraint('UNIQUE(order_id)', 'El pedido ya tiene una autorización conservada.')

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('_arg_repair_engine') is not _REPAIR_ENGINE:
            raise AccessError(_('Registrá la autorización desde el parte.'))
        return super().create(vals_list)

    def write(self, values):
        raise UserError(_('La autorización conserva condiciones y constancia. Prepará otro pedido para nuevos alcances.'))

    def unlink(self):
        raise UserError(_('Las autorizaciones se conservan.'))
