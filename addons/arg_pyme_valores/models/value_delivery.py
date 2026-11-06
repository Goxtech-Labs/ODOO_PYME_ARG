import hashlib
import json
import uuid
from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.addons.arg_pyme_administracion.models.treasury_document import _TREASURY_ENGINE, engine, check_manager
from .value_event import _VALUE_ENGINE, value_engine


class ValueDelivery(models.Model):
    _inherit = 'arg.pyme.value.instrument'
    reservation_line_id = fields.Many2one('arg.pyme.treasury.line', readonly=True, copy=False, check_company=True, ondelete='restrict', string='Reservado para')
    reserved_from_state = fields.Selection([('draft', 'Propio preparado'), ('portfolio', 'En cartera'), ('own_returned', 'Propio devuelto')], readonly=True, copy=False)
    outgoing_line_id = fields.Many2one('arg.pyme.treasury.line', readonly=True, copy=False, check_company=True, ondelete='restrict', string='Última entrega')
    linked_treasury_line_ids = fields.One2many('arg.pyme.treasury.line', 'value_instrument_id', readonly=True, copy=False, string='Recibos y entregas')
    own_liability_account_id = fields.Many2one('account.account', readonly=True, copy=False, check_company=True, ondelete='restrict')
    own_bank_journal_id = fields.Many2one('account.journal', readonly=True, copy=False, check_company=True, ondelete='restrict')
    own_bank_ledger_account_id = fields.Many2one('account.account', readonly=True, copy=False, check_company=True, ondelete='restrict')
    available_amount = fields.Monetary(string='Nominal disponible para salida', compute='_compute_delivery_amounts', compute_sudo=False, aggregator=False)
    exposure_amount = fields.Monetary(string='Nominal con seguimiento abierto', compute='_compute_delivery_amounts', compute_sudo=False, aggregator=False)
    exposure_unknown = fields.Boolean(string='Alcance por determinar', compute='_compute_delivery_amounts', compute_sudo=False, aggregator=False)

    @api.model
    def _value_effect_fields(self):
        return super()._value_effect_fields() | {'reservation_line_id', 'reserved_from_state', 'outgoing_line_id',
                'linked_treasury_line_ids', 'own_liability_account_id', 'own_bank_journal_id',
                'own_bank_ledger_account_id', 'available_amount', 'exposure_amount', 'exposure_unknown'}

    @api.depends('state', 'ownership', 'amount', 'reservation_line_id', 'outgoing_line_id.payment_id',
                 'linked_treasury_line_ids.value_exposure_open', 'linked_treasury_line_ids.value_recourse_condition',
                 'outgoing_line_id.value_bank_move_id.state', 'outgoing_line_id.value_reversal_move_id.state')
    def _compute_delivery_amounts(self):
        for value in self:
            available = value.state == 'portfolio' or (value.ownership == 'own' and value.state in ('draft', 'own_returned'))
            value.available_amount = value.amount if available and not value.reservation_line_id else 0
            pending = value.linked_treasury_line_ids.filtered('value_exposure_open')
            own_pending = (value.ownership == 'own' and value.outgoing_line_id.payment_id
                           and not value.outgoing_line_id._arg_value_inverse()
                           and value.outgoing_line_id.value_bank_move_id.state != 'posted')
            value.exposure_amount = value.amount if pending or own_pending else 0
            value.exposure_unknown = any(not l.value_recourse_condition or l.value_recourse_condition == 'unknown' for l in pending)

    @api.depends('state', 'ownership', 'amount', 'reserved_from_state', 'settlement_move_id.state')
    def _compute_value_amounts(self):
        super()._compute_value_amounts()
        for value in self:
            if value.ownership == 'third_party' and (value.state == 'disputed' or (value.state == 'reserved' and value.reserved_from_state == 'portfolio')):
                value.portfolio_amount = value.amount

    def _arg_finance_documents(self):
        return self.receipt_line_id.document_id | self.outgoing_line_id.document_id | self.reservation_line_id.document_id

    def _arg_delivery_context(self):
        scoped = self.with_company(self.company_id)
        clean = {k: v for k, v in scoped.env.context.items() if not k.startswith('default_')}
        return scoped.with_context(clean, _arg_value_engine=_VALUE_ENGINE, _arg_treasury_engine=_TREASURY_ENGINE, _arg_value_lock_scope=_VALUE_ENGINE,
                                   tracking_disable=True, mail_notrack=True)

    def _arg_check_delivery(self, line):
        self.ensure_one()
        doc = line.document_id
        doc._arg_check(manager=True)
        self._arg_value_check()
        if (doc.kind != 'OPA' or self.instrument_kind != 'cheque' or self.support != 'paper'
                or self.company_id != doc.company_id or self.currency_id != doc.currency_id
                or self.currency_id.compare_amounts(self.amount, line.amount)):
            raise UserError(_('La salida requiere un cheque en papel completo, de la misma compañía y moneda que la OPA.'))
        if self.reservation_line_id and self.reservation_line_id != line:
            raise UserError(_('El cheque %s está reservado para otra orden de pago.', self.arg_number))
        state = self.reserved_from_state if self.state == 'reserved' and self.reservation_line_id == line else self.state
        role = line._arg_value_role()
        method = line.method_id
        doc.company_id._check_value_method()
        if doc.company_id._arg_value_method_role(method) != role:
            raise UserError(_('Seleccione el medio específico de cheques propios o de terceros correspondiente.'))
        if self.date > doc.date:
            raise UserError(_('La OPA no puede preceder al registro del título.'))
        if role == 'third_out':
            if state != 'portfolio' or not self.receipt_line_id or self.receipt_line_id.document_id.reverted_at:
                raise UserError(_('Seleccione un cheque recibido y disponible en cartera.'))
            if method.payment_account_id != self.portfolio_account_id:
                raise UserError(_('El medio de salida debe usar la misma cuenta de cartera del cheque recibido.'))
            if doc.date < self.receipt_line_id.document_id.date:
                raise UserError(_('La entrega no puede preceder a la recepción.'))
        else:
            if state not in ('draft', 'own_returned'):
                raise UserError(_('El cheque propio no está disponible para entrega.'))
            if self.partner_id.commercial_partner_id != doc.partner_id.commercial_partner_id:
                raise UserError(_('El beneficiario del cheque propio debe coincidir con el proveedor de la OPA.'))
            if self.beneficiary_id and self.beneficiary_id.commercial_partner_id != doc.partner_id.commercial_partner_id:
                raise UserError(_('Revise el beneficiario indicado en el título.'))
            account = self.bank_account_id
            journal = method.journal_id
            if (not account or journal.bank_account_id != account
                    or account.partner_id.commercial_partner_id != self.company_id.partner_id.commercial_partner_id
                    or self.issuer_id.commercial_partner_id != self.company_id.partner_id.commercial_partner_id):
                raise UserError(_('Seleccione la cuenta libradora y el banco de la compañía, con la compañía como librador.'))
            norm = lambda x: ''.join((x or '').split()).upper()
            if norm(account.account_number) != norm(self.issuer_account):
                raise UserError(_('La cuenta registrada y la cuenta del título no coinciden.'))
            if not self.identity_key or not self.bank_name or not self.issued_on or not self.payable_on:
                raise UserError(_('Complete identificación, banco y fechas del cheque propio antes de entregarlo.'))
            if not journal.default_account_id or journal.default_account_id.account_type != 'asset_cash':
                raise UserError(_('El banco propio necesita su cuenta de liquidez configurada.'))

    def _arg_check_transmission(self, line):
        reference = line.value_reference or line.document_id.arg_reference
        if not (reference or '').strip():
            raise UserError(_('Indique la constancia de entrega en el medio o en la referencia de la OPA.'))
        if self.ownership == 'own':
            if line.value_transmission != 'own_delivery':
                raise UserError(_('Seleccione Entrega de propio como transmisión.'))
        else:
            if line.value_recourse_condition not in ('with_recourse','without_recourse','unknown'):
                raise UserError(_('Indique el alcance declarado o Por determinar.'))
            if line.value_transmission not in ('endorsement', 'assignment', 'delivery') or not line.value_title_clause:
                raise UserError(_('Indique transmisión y cláusula conocida del título.'))
            if line.value_transmission == 'endorsement' and line.value_title_clause == 'not_order':
                raise UserError(_('Este circuito de endoso estándar no cubre el título no a la orden. Registre la cesión realizada o use un perfil específico documentado.'))
            if line.value_transmission == 'delivery' and line.value_title_clause not in ('bearer', 'blank'):
                raise UserError(_('La entrega sin nuevo endoso requiere constancia de portador o endoso previo en blanco.'))

    def _arg_reserve_delivery(self, line):
        self._arg_check_delivery(line)
        if self.reservation_line_id == line:
            return
        original = self.state
        protected = self._arg_delivery_context()
        protected.write({'reservation_line_id': line.id, 'reserved_from_state': original, 'state': 'reserved'})
        protected._record_draft_event('reserved', {'date': str(line.document_id.date), 'line_id': line.id, 'document_id': line.document_id.id})

    def _arg_release_delivery(self, line):
        self._arg_value_check()
        check_manager(self.env)
        if self.reservation_line_id != line:
            return
        protected = self._arg_delivery_context()
        protected.write({'state': self.reserved_from_state, 'reservation_line_id': False, 'reserved_from_state': False})
        protected._record_draft_event('reservation_released', {'line_id': line.id, 'document_id': line.document_id.id})

    def _arg_deliver(self, line, payment):
        if not engine(self.env):
            raise AccessError(_('Entregue el cheque desde la confirmación de la OPA.'))
        self._arg_check_delivery(line)
        self._arg_check_transmission(line)
        protected = self._arg_delivery_context()
        updates = {'state': 'transferred' if self.ownership == 'third_party' else 'own_issued',
                   'outgoing_line_id': line.id, 'reservation_line_id': False, 'reserved_from_state': False}
        if self.ownership == 'third_party':
            original = self.receipt_line_id.payment_id.move_id.line_ids.filtered(lambda l: l.account_id == self.portfolio_account_id)
            outgoing = payment.move_id.line_ids.filtered(lambda l: l.account_id == self.portfolio_account_id)
            if (len(original) != 1 or len(outgoing) != 1 or original.matched_debit_ids or original.matched_credit_ids
                    or self.currency_id.compare_amounts(original.amount_residual_currency, self.amount)):
                raise UserError(_('El apunte de cartera ya no está libre por el nominal completo.'))
            (original | outgoing).with_context(protected.env.context).reconcile()
            line.with_context(protected.env.context).write({'value_exposure_open': True})
        else:
            updates.update(financial_confirmed_at=fields.Datetime.now(), own_liability_account_id=payment.outstanding_account_id.id,
                           own_bank_journal_id=payment.journal_id.id, own_bank_ledger_account_id=payment.journal_id.default_account_id.id)
        protected.write(updates)
        protected._record_draft_event('delivered', {'date': str(line.document_id.date), 'line_id': line.id, 'payment_id': payment.id,
            'move_id': payment.move_id.id, 'role': line._arg_value_role(), 'transmission': line.value_transmission,
            'title_clause': line.value_title_clause, 'reference': line.value_reference or line.document_id.arg_reference,
            'recourse': line.value_recourse_condition, 'recipient_id': line.document_id.partner_id.id})

    def _arg_operation_value(self, operation, date, reference, journal, request_key, treasury_line=None):
        if operation not in ('delivery_returned', 'delivery_rejected', 'own_debited', 'recourse_released'):
            if self.reservation_line_id or self._arg_active_outgoing():
                raise UserError(_('Resuelva la reserva o la entrega vigente antes de operar sobre la recepción.'))
            return super()._arg_operation_value(operation, date, reference, journal, request_key)
        line = treasury_line
        if not line:
            raise UserError(_('Seleccione la entrega objetivo de la operación.'))
        line.check_access('read')
        if line.value_instrument_id != self:
            raise UserError(_('La entrega no corresponde a este cheque.'))
        self._arg_finance_lock(line.document_id)
        try:
            date = fields.Date.to_date(date)
            request_key = str(uuid.UUID(request_key))
        except (TypeError, ValueError, AttributeError):
            raise ValidationError(_('Fecha o referencia de operación inválida.'))
        if not date or not (reference or '').strip():
            raise UserError(_('Complete fecha y constancia de la operación.'))
        if not line:
            raise UserError(_('Seleccione la entrega a la que corresponde esta operación.'))
        line.check_access('read')
        if line.value_instrument_id != self or line.document_id.kind != 'OPA' or date < line.document_id.date:
            raise UserError(_('La operación debe corresponder a una entrega de este cheque, con fecha coherente.'))
        payload = {'date': str(date), 'reference': reference.strip(), 'line_id': line.id}
        digest = hashlib.sha256(json.dumps({'kind': operation, 'payload': payload}, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        previous = self.env['arg.pyme.value.event'].search([('instrument_id', '=', self.id), ('request_key', '=', request_key)], limit=1)
        if previous:
            if previous.kind != operation or previous.payload.get('request_hash') != digest:
                raise UserError(_('La referencia se usó con otros datos.'))
            return self._value_action()
        protected = self._arg_delivery_context()
        line = line.with_context(protected.env.context)
        if operation == 'recourse_released':
            if self.ownership != 'third_party' or not line.value_exposure_open or not line.document_id.confirmed_at:
                raise UserError(_('Esa transmisión no tiene un seguimiento abierto para cerrar.'))
            line.write({'value_exposure_open': False, 'value_exposure_closed_on': date, 'value_exposure_reference': reference.strip()})
            if line == self.outgoing_line_id and self.state == 'transferred':
                protected.write({'state': 'transferred_closed'})
        else:
            if line != self._arg_active_outgoing() or line.document_id.reverted_at:
                raise UserError(_('La entrega ya no tiene un efecto vigente.'))
            if operation == 'own_debited':
                if self.ownership != 'own' or self.state != 'own_issued':
                    raise UserError(_('El débito requiere un cheque propio entregado, aún pendiente.'))
                move = protected._arg_post_own_debit(line, date, reference)
                line.write({'value_bank_move_id': move.id})
                protected.write({'state': 'own_debited'})
            else:
                if line.value_bank_move_id or self.state not in ('transferred', 'own_issued'):
                    raise UserError(_('La devolución simple no cubre títulos ya debitados o con cierre informado.'))
                payment = line.payment_id
                if payment.move_id.state != 'posted' or payment.move_id.reversal_move_ids.filtered(lambda m: m.state == 'posted'):
                    raise UserError(_('Revise el efecto original antes de registrar devolución.'))
                move = payment.move_id.with_context(protected.env.context)._reverse_moves([{
                    'date': date, 'ref': self.arg_number + ' · ' + reference,
                    'arg_treasury_document_id': line.document_id.id, 'arg_value_instrument_id': self.id}], cancel=True)
                line.write({'value_reversal_move_id': move.id})
                state = 'disputed' if operation == 'delivery_rejected' else ('portfolio' if self.ownership == 'third_party' else 'own_returned')
                protected.write({'state': state})
            payload['move_id'] = move.id
        payload['request_hash'] = digest
        protected.env['arg.pyme.value.event'].create({'instrument_id': self.id, 'kind': operation, 'request_key': request_key, 'payload': payload})
        return self._value_action()

    def _arg_active_outgoing(self):
        self.ensure_one()
        line = self.outgoing_line_id
        return line if line.payment_id and not line._arg_value_inverse() and not line.document_id.reverted_at else self.env['arg.pyme.treasury.line']

    def _arg_post_own_debit(self, line, date, reference):
        if not value_engine(self.env):
            raise AccessError(_('Use la operación del cheque para registrar el débito.'))
        journal = self.own_bank_journal_id
        if (journal.type != 'bank' or self.own_bank_ledger_account_id.account_type != 'asset_cash'
                or journal.company_id != self.company_id or journal.bank_account_id != self.bank_account_id
                or (journal.currency_id and journal.currency_id != self.currency_id)):
            raise UserError(_('Revise la cuenta bancaria de origen del cheque.'))
        original = line.payment_id.move_id.line_ids.filtered(lambda l: l.account_id == self.own_liability_account_id)
        if (len(original) != 1 or original.matched_debit_ids or original.matched_credit_ids
                or original.parent_state != 'posted' or self.currency_id.compare_amounts(original.amount_residual_currency, -self.amount)):
            raise UserError(_('La obligación del cheque ya no está pendiente por su nominal completo.'))
        company_currency = self.company_id.currency_id
        company_currency._arg_require_conversion(self.currency_id, self.company_id, date)
        balance = self.currency_id._convert(self.amount, company_currency, self.company_id, date)
        if company_currency.compare_amounts(balance, 0) <= 0:
            raise UserError(_('La conversión debe producir un importe positivo.'))
        move = self.env['account.move'].create({'move_type': 'entry', 'company_id': self.company_id.id,
            'journal_id': journal.id, 'date': date, 'ref': self.arg_number + ' · ' + reference, 'arg_value_instrument_id': self.id,
            'line_ids': [Command.create({'name': self.arg_number, 'account_id': self.own_liability_account_id.id,
                'partner_id': line.document_id.commercial_partner_id.id, 'currency_id': self.currency_id.id,
                'amount_currency': self.amount, 'debit': balance, 'credit': 0}),
                Command.create({'name': self.arg_number, 'account_id': self.own_bank_ledger_account_id.id,
                'partner_id': line.document_id.commercial_partner_id.id, 'currency_id': self.currency_id.id,
                'amount_currency': -self.amount, 'debit': 0, 'credit': balance})]})
        move.action_post()
        (original | move.line_ids.filtered(lambda l: l.account_id == self.own_liability_account_id)).reconcile()
        return move

    def _arg_document_relations(self):
        return super()._arg_document_relations() + [{'label': 'Última OPA', 'records': self.outgoing_line_id.document_id},
                {'label': 'OPA con historial de entregas', 'records': self.linked_treasury_line_ids.filtered(lambda l: l.document_id.kind == 'OPA').document_id},
                {'label': 'Débito propio', 'records': self.outgoing_line_id.value_bank_move_id}]

    def _arg_report_payload(self):
        result = super()._arg_report_payload()
        if self.ownership == 'own' and self.financial_confirmed_at:
            result['notes'] = _('Cheque propio registrado. OPA de última entrega: %s. El débito bancario es una operación separada.', self.outgoing_line_id.document_id.arg_number)
            result['totals'] = [{'label': _('Nominal'), 'amount': self.amount},
                                {'label': _('Débito propio registrado'), 'amount': self.amount if self.outgoing_line_id.value_bank_move_id.state == 'posted' else 0}]
        result['totals'] += [{'label': _('Disponible para salida'), 'amount': self.available_amount},
                             {'label': _('Nominal con seguimiento abierto'), 'amount': self.exposure_amount}]
        return result
