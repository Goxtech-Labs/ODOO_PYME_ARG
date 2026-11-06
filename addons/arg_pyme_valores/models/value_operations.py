import json
import hashlib
import uuid
from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.addons.arg_pyme_administracion.models.treasury_document import _TREASURY_ENGINE, engine, check_manager
from .value_event import _VALUE_ENGINE, value_engine


class ValueOperations(models.Model):
    _inherit = 'arg.pyme.value.instrument'
    receipt_line_id = fields.Many2one('arg.pyme.treasury.line', readonly=True, copy=False, check_company=True, ondelete='restrict')
    financial_confirmed_at = fields.Datetime(readonly=True, copy=False)
    portfolio_account_id = fields.Many2one('account.account', readonly=True, copy=False, check_company=True, ondelete='restrict')
    deposit_journal_id = fields.Many2one('account.journal', readonly=True, copy=False, check_company=True, ondelete='restrict', string='Banco de depósito')
    deposited_on = fields.Date(readonly=True, copy=False, string='Depositado el')
    settlement_move_id = fields.Many2one('account.move', readonly=True, copy=False, check_company=True, ondelete='restrict', string='Asiento de acreditación')
    rejection_move_id = fields.Many2one('account.move', readonly=True, copy=False, check_company=True, ondelete='restrict', string='Asiento inverso')
    portfolio_amount = fields.Monetary(string='Nominal en gestión', compute='_compute_value_amounts', compute_sudo=False)
    credited_amount = fields.Monetary(string='Acreditación registrada', compute='_compute_value_amounts', compute_sudo=False)
    _receipt_line_unique = models.Constraint('UNIQUE(receipt_line_id)', 'El medio ya está vinculado a otro valor.')

    @api.depends('state', 'amount', 'settlement_move_id.state')
    def _compute_value_amounts(self):
        for value in self:
            value.portfolio_amount = value.amount if value.state in ('portfolio', 'deposited') else 0
            value.credited_amount = value.amount if value.state == 'settled' and value.settlement_move_id.state == 'posted' else 0

    @api.model
    def _value_effect_fields(self):
        return {'receipt_line_id', 'financial_confirmed_at', 'portfolio_account_id', 'deposit_journal_id',
                'deposited_on', 'settlement_move_id', 'rejection_move_id', 'portfolio_amount', 'credited_amount'}

    @api.model_create_multi
    def create(self, vals_list):
        protected = self._value_effect_fields()
        if any(protected & v.keys() for v in vals_list) or any('default_' + k in self.env.context for k in protected):
            raise AccessError(_('Los efectos del valor se asignan desde su operación.'))
        return super().create(vals_list)

    def write(self, vals):
        if self._value_effect_fields() & vals.keys() and not value_engine(self.env):
            raise AccessError(_('Los efectos financieros del valor no se editan manualmente.'))
        terms = self._value_business_fields() | {'date', 'partner_id', 'company_id', 'currency_id',
                                               'amount', 'cheque_type', 'payable_on', 'beneficiary_id'}
        if terms & vals.keys() and any(value.financial_confirmed_at for value in self):
            raise UserError(_('El título recibido conserva su nominal, identidad y condiciones. Corrija mediante un evento vinculado.'))
        return super().write(vals)

    def _arg_finance_lock(self, extra_documents=None):
        self.ensure_one()
        check_manager(self.env)
        self._arg_value_lock()
        docs = self._arg_finance_documents()
        if extra_documents:
            docs |= extra_documents
        for doc in docs.sorted('id'):
            doc._arg_lock_document_only()

    def _arg_check_receipt(self, line):
        self.ensure_one()
        doc = line.document_id
        self._arg_value_check()
        doc.company_id._check_value_method()
        if (doc.kind != 'REC' or self.instrument_kind != 'cheque' or self.ownership != 'third_party'
                or self.state != 'draft' or self.financial_confirmed_at or self.receipt_line_id):
            raise UserError(_('Seleccione un cheque de tercero en borrador, sin recepción previa, para este recibo.'))
        if (self.company_id != doc.company_id or self.currency_id != doc.currency_id
                or self.partner_id.commercial_partner_id != doc.partner_id.commercial_partner_id
                or self.currency_id.compare_amounts(self.amount, line.amount)):
            raise UserError(_('Cheque y recibo deben coincidir en compañía, tercero, moneda e importe completo.'))
        if not doc.company_id.arg_value_receipt_method_id or line.method_id != doc.company_id.arg_value_receipt_method_id:
            raise UserError(_('Configure y seleccione el medio de recepción de cheques de esta compañía.'))
        if self.support != 'paper':
            raise UserError(_('La recepción ECHEQ necesita el circuito de aceptación externa, todavía pendiente.'))
        if not self.identity_key or not self.issuer_id or not self.issued_on or not self.payable_on or not self.bank_name:
            raise UserError(_('Complete banco, cuenta y número, librador, emisión y fecha de pago del cheque antes de confirmar.'))
        if self.date > doc.date:
            raise UserError(_('La fecha del recibo no puede preceder al registro del cheque.'))

    def _arg_receive(self, line, payment):
        self.ensure_one()
        if not engine(self.env):
            raise AccessError(_('Reciba el cheque desde la confirmación del recibo.'))
        self._arg_check_receipt(line)
        self.with_context(_arg_value_engine=_VALUE_ENGINE).write({
            'state': 'portfolio', 'receipt_line_id': line.id, 'financial_confirmed_at': fields.Datetime.now(),
            'portfolio_account_id': payment.outstanding_account_id.id})
        self._record_draft_event('received', {'date': str(line.document_id.date), 'receipt_id': line.document_id.id,
                                            'line_id': line.id, 'payment_id': payment.id, 'move_id': payment.move_id.id,
                                            'nominal': self.amount, 'currency_id': self.currency_id.id})

    def action_value_operation(self):
        self._arg_value_check()
        check_manager(self.env)
        return {'type': 'ir.actions.act_window', 'name': _('Operación de cheque ARG'),
                'res_model': 'arg.pyme.value.operation.wizard', 'views': [(False, 'form')], 'target': 'new',
                'context': {'default_instrument_id': self.id, 'default_treasury_line_id': self.outgoing_line_id.id,
                            'default_operation': {'portfolio':'deposited','deposited':'settled','own_issued':'own_debited',
                                                  'transferred':'delivery_returned','disputed':'rejected'}.get(self.state)}}

    def _arg_operation_value(self, operation, date, reference, journal, request_key):
        self._arg_finance_lock()
        try:
            request_key = str(uuid.UUID(request_key))
            date = fields.Date.to_date(date)
        except (ValueError, TypeError, AttributeError):
            raise ValidationError(_('Referencia de operación o fecha inválida.'))
        if operation not in ('deposited', 'settled', 'rejected') or not date or not (reference or '').strip():
            raise ValidationError(_('Seleccione operación, fecha y constancia o motivo.'))
        payload = {'date': str(date), 'reference': reference.strip(), 'journal_id': journal.id if journal else False}
        digest = hashlib.sha256(json.dumps({'kind': operation, 'payload': payload}, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        previous = self.env['arg.pyme.value.event'].search([('instrument_id', '=', self.id), ('request_key', '=', request_key)], limit=1)
        if previous:
            if previous.kind != operation or previous.payload.get('request_hash') != digest:
                raise UserError(_('La referencia de operación ya se utilizó con otros datos.'))
            return self._value_action()
        receipt = self.receipt_line_id.document_id
        if not receipt or receipt.reverted_at or date < receipt.date or (self.deposited_on and date < self.deposited_on):
            raise UserError(_('Revise la recepción y la fecha de la operación.'))
        scoped = self.with_company(self.company_id)
        clean = {k: v for k, v in scoped.env.context.items() if not k.startswith('default_')}
        protected = scoped.with_context(clean, _arg_value_engine=_VALUE_ENGINE,
                        _arg_treasury_engine=_TREASURY_ENGINE, _arg_value_lock_scope=_VALUE_ENGINE, tracking_disable=True, mail_notrack=True)
        if operation == 'deposited':
            if self.state != 'portfolio':
                raise UserError(_('Sólo puede depositar un cheque disponible en cartera.'))
            self._arg_check_bank_journal(journal)
            protected.write({'state': 'deposited', 'deposit_journal_id': journal.id, 'deposited_on': date})
        elif operation == 'settled':
            if self.state != 'deposited':
                raise UserError(_('Registre primero el depósito del cheque.'))
            if journal and journal != self.deposit_journal_id:
                raise UserError(_('La acreditación debe usar el banco del depósito.'))
            move = protected._arg_settle_value(date, reference)
            protected.write({'state': 'settled', 'settlement_move_id': move.id})
            payload['move_id'] = move.id
        else:
            if self.state not in ('portfolio', 'deposited', 'disputed') or self.settlement_move_id:
                raise UserError(_('Este rechazo requiere un valor pendiente, sin acreditación ni transmisión.'))
            payment = self.receipt_line_id.payment_id
            if payment.move_id.state != 'posted' or payment.move_id.reversal_move_ids.filtered(lambda m: m.state == 'posted'):
                raise UserError(_('El efecto original ya no está disponible para revertir.'))
            portfolio = payment.move_id.line_ids.filtered(lambda l: l.account_id == self.portfolio_account_id)
            if portfolio.matched_debit_ids or portfolio.matched_credit_ids:
                raise UserError(_('El valor tiene aplicaciones contables posteriores. Revise su recuperación antes de rechazar.'))
            inverse = payment.move_id.with_context(protected.env.context)._reverse_moves([{
                'date': date, 'ref': self.arg_number + ' · ' + reference,
                'arg_treasury_document_id': receipt.id, 'arg_value_instrument_id': self.id}], cancel=True)
            self.receipt_line_id.with_context(protected.env.context).write({'value_reversal_move_id': inverse.id})
            protected.write({'state': 'rejected', 'rejection_move_id': inverse.id})
            payload['move_id'] = inverse.id
        payload['request_hash'] = digest
        protected.env['arg.pyme.value.event'].create({'instrument_id': self.id, 'kind': operation,
                                                    'request_key': request_key, 'payload': payload})
        return self._value_action()

    def _arg_check_bank_journal(self, journal):
        journal.ensure_one()
        journal.check_access('read')
        if (journal.company_id != self.company_id or journal.type != 'bank' or not journal.default_account_id
                or journal.default_account_id.account_type != 'asset_cash'
                or journal.default_account_id == self.portfolio_account_id
                or (journal.currency_id and journal.currency_id != self.currency_id)):
            raise UserError(_('Seleccione un banco de la compañía, con cuenta de banco y moneda compatibles.'))

    def _arg_settle_value(self, date, reference):
        self.ensure_one()
        if not value_engine(self.env):
            raise AccessError(_('Registre la acreditación desde la operación del cheque.'))
        journal = self.deposit_journal_id
        self._arg_check_bank_journal(journal)
        company_currency = self.company_id.currency_id
        company_currency._arg_require_conversion(self.currency_id, self.company_id, date)
        balance = self.currency_id._convert(self.amount, company_currency, self.company_id, date)
        if company_currency.compare_amounts(balance, 0) <= 0:
            raise UserError(_('La conversión no produce un importe positivo en moneda de la compañía.'))
        original = self.receipt_line_id.payment_id.move_id.line_ids.filtered(lambda l: l.account_id == self.portfolio_account_id)
        if (len(original) != 1 or original.parent_state != 'posted' or original.currency_id != self.currency_id
                or original.matched_debit_ids or original.matched_credit_ids
                or self.currency_id.compare_amounts(original.amount_residual_currency, self.amount)):
            raise UserError(_('El apunte de cartera cambió. Revise su origen antes de acreditar.'))
        move = self.env['account.move'].create({'move_type': 'entry', 'company_id': self.company_id.id,
            'journal_id': journal.id, 'date': date, 'ref': self.arg_number + ' · ' + reference,
            'arg_value_instrument_id': self.id, 'line_ids': [
                Command.create({'name': self.arg_number, 'account_id': journal.default_account_id.id,
                                'partner_id': self.partner_id.commercial_partner_id.id, 'currency_id': self.currency_id.id,
                                'amount_currency': self.amount, 'debit': balance, 'credit': 0}),
                Command.create({'name': self.arg_number, 'account_id': self.portfolio_account_id.id,
                                'partner_id': self.partner_id.commercial_partner_id.id, 'currency_id': self.currency_id.id,
                                'amount_currency': -self.amount, 'debit': 0, 'credit': balance})]})
        move.action_post()
        credit = move.line_ids.filtered(lambda l: l.account_id == self.portfolio_account_id)
        if len(original) != 1 or len(credit) != 1 or original.reconciled:
            raise UserError(_('El apunte de cartera cambió. Revise su origen antes de acreditar.'))
        (original | credit).reconcile()
        return move

    def _arg_document_relations(self):
        return [{'label': 'Recibo de origen', 'records': self.receipt_line_id.document_id},
                {'label': 'Pago nativo del valor', 'records': self.receipt_line_id.payment_id},
                {'label': 'Acreditación', 'records': self.settlement_move_id},
                {'label': 'Reversión del valor', 'records': self.rejection_move_id}]

    def _arg_report_payload(self):
        result = super()._arg_report_payload()
        if self.financial_confirmed_at:
            result['notes'] = _('Registro interno del cheque. Recibo de origen: %s. Depósito y acreditación se registran por separado.', self.receipt_line_id.document_id.arg_number)
            result['totals'] += [{'label': _('Nominal en gestión'), 'amount': self.portfolio_amount},
                                 {'label': _('Acreditación registrada'), 'amount': self.credited_amount}]
        return result
