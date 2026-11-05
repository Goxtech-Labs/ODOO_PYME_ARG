from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from .value_event import _VALUE_ENGINE


class TreasuryLine(models.Model):
    _inherit = 'arg.pyme.treasury.line'
    value_instrument_id = fields.Many2one('arg.pyme.value.instrument', string='Cheque', check_company=True, ondelete='restrict')

    @api.onchange('value_instrument_id')
    def _onchange_value_instrument(self):
        if self.value_instrument_id:
            self.amount = self.value_instrument_id.amount
            self.method_id = self.document_id.company_id.arg_value_receipt_method_id


class TreasuryDocument(models.Model):
    _inherit = 'arg.pyme.treasury.document'
    corrected_value_amount = fields.Monetary(string='Valores revertidos', compute='_compute_corrected_values', compute_sudo=False)

    @api.depends('line_ids.amount', 'line_ids.value_instrument_id.state')
    def _compute_corrected_values(self):
        for doc in self:
            doc.corrected_value_amount = sum(doc.line_ids.filtered(lambda l: l.value_instrument_id.state in ('rejected', 'returned')).mapped('amount'))

    def _arg_prepare_confirmation(self):
        super()._arg_prepare_confirmation()
        lines = self.line_ids.filtered('value_instrument_id')
        values = lines.value_instrument_id
        if len(values) != len(lines):
            raise UserError(_('Un mismo cheque no puede aparecer dos veces en el recibo.'))
        for instrument in values.sorted('id'):
            instrument._arg_finance_lock()

    def _arg_check_line_configuration(self, line):
        super()._arg_check_line_configuration(line)
        value = line.value_instrument_id
        if not value:
            if line.method_id == self.company_id.arg_value_receipt_method_id:
                raise UserError(_('Seleccione el cheque para usar el medio de valores.'))
            return
        value._arg_check_receipt(line)

    def _arg_create_line_payment(self, line):
        value = line.value_instrument_id
        if not value:
            return super()._arg_create_line_payment(line)
        debt = self._arg_debt_lines()
        if len(debt.account_id) > 1:
            raise UserError(_('Las facturas usan distintas cuentas. Prepare recibos separados.'))
        payment = self.env['account.payment'].with_context(_arg_value_engine=_VALUE_ENGINE).create({
            'company_id': self.company_id.id, 'partner_id': self.partner_id.commercial_partner_id.id,
            'partner_type': 'customer', 'payment_type': 'inbound', 'date': self.date,
            'currency_id': self.currency_id.id, 'amount': line.amount,
            'journal_id': line.method_id.journal_id.id, 'payment_method_line_id': line.method_id.id,
            'memo': self.arg_number + ' · ' + value.arg_number,
            'arg_treasury_document_id': self.id, 'arg_value_instrument_id': value.id})
        payment.action_post()
        counterpart = payment.move_id.line_ids.filtered(lambda l: l.account_type == 'asset_receivable')
        if debt and debt.account_id != counterpart.account_id:
            raise UserError(_('Las facturas y el cheque deben usar la misma cuenta a cobrar.'))
        for due in debt.sorted(lambda l: (l.date_maturity or l.date, l.id)):
            if not counterpart.reconciled and not due.reconciled:
                (counterpart | due).with_context(_arg_value_engine=_VALUE_ENGINE).reconcile()
        return payment

    def _arg_finalize_line_payment(self, line, payment):
        super()._arg_finalize_line_payment(line, payment)
        if line.value_instrument_id:
            line.value_instrument_id._arg_receive(line, payment)

    def _arg_line_snapshot(self, line):
        result = super()._arg_line_snapshot(line)
        if line.value_instrument_id:
            result.update(instrument_id=line.value_instrument_id.id, instrument=line.value_instrument_id.arg_number,
                          classification='value_pending')
        return result

    def _arg_effect_payments(self):
        return super()._arg_effect_payments().filtered(lambda p: not p.arg_value_instrument_id or p.arg_value_instrument_id.state not in ('rejected', 'returned'))

    def _arg_effect_nominal(self):
        return super()._arg_effect_nominal() - self.corrected_value_amount

    def _arg_payment_expected(self, payment):
        value = payment.arg_value_instrument_id
        if value and value.state in ('rejected', 'returned'):
            inverse = value.rejection_move_id
            return bool(inverse and inverse.state == 'posted' and inverse.reversed_entry_id == payment.move_id)
        return super()._arg_payment_expected(payment)

    @api.depends('line_ids.amount', 'confirmed_at', 'reverted_at', 'payment_ids.state',
                 'payment_ids.move_id.line_ids.amount_residual_currency', 'payment_ids.move_id.state',
                 'line_ids.value_instrument_id.state', 'line_ids.value_instrument_id.rejection_move_id.state')
    def _compute_amounts(self):
        super()._compute_amounts()

    @api.depends('confirmed_at', 'canceled_at', 'reverted_at', 'payment_ids.state', 'payment_ids.move_id.state',
                 'line_ids.value_instrument_id.state', 'line_ids.value_instrument_id.rejection_move_id.state')
    def _compute_status(self):
        super()._compute_status()

    @api.depends('payment_ids.move_id.line_ids.matched_debit_ids', 'payment_ids.move_id.line_ids.matched_credit_ids',
                 'line_ids.value_instrument_id.state')
    def _compute_partials(self):
        super()._compute_partials()

    def _arg_before_reverse(self):
        super()._arg_before_reverse()
        for value in self.line_ids.value_instrument_id.sorted('id'):
            value._arg_finance_lock()
            if value.state not in ('portfolio', 'rejected'):
                raise UserError(_('Antes de revertir el recibo, resuelva el depósito o la acreditación del cheque %s.', value.arg_number))

    def _arg_reverse(self, date, reason, key):
        return super(TreasuryDocument, self._arg_value_operation_context())._arg_reverse(date, reason, key)

    def _arg_apply(self, move, key):
        return super(TreasuryDocument, self._arg_value_operation_context())._arg_apply(move, key)

    def _arg_unapply(self, ids, reason, key):
        return super(TreasuryDocument, self._arg_value_operation_context())._arg_unapply(ids, reason, key)

    def _arg_value_operation_context(self):
        clean = {k: v for k, v in self.env.context.items() if not k.startswith('default_')}
        return self.with_context(clean, _arg_value_engine=_VALUE_ENGINE)

    def _arg_after_reverse(self, inverses, date, reason):
        super()._arg_after_reverse(inverses, date, reason)
        for value in self.line_ids.value_instrument_id.filtered(lambda v: v.state == 'portfolio'):
            inverse = inverses.filtered(lambda m: m.reversed_entry_id == value.receipt_line_id.payment_id.move_id)
            inverse.with_context(_arg_value_engine=_VALUE_ENGINE).write({'arg_value_instrument_id': value.id})
            value.with_context(_arg_value_engine=_VALUE_ENGINE).write({'state': 'returned', 'rejection_move_id': inverse.id})
            value._record_draft_event('receipt_reversed', {'date': str(date), 'reason': reason, 'move_id': inverse.id})

    def _arg_report_payload(self):
        result = super()._arg_report_payload()
        if self.corrected_value_amount:
            result['totals'].append({'label': _('Valores revertidos'), 'amount': self.corrected_value_amount})
        return result


class Company(models.Model):
    _inherit = 'res.company'
    arg_value_receipt_method_id = fields.Many2one('account.payment.method.line', string='Medio de recepción de cheques ARG', check_company=True)

    @api.constrains('arg_value_receipt_method_id', 'arg_receipt_method_id', 'arg_payment_method_id')
    def _check_value_method(self):
        for company in self:
            method = company.arg_value_receipt_method_id
            if not method:
                continue
            account = method.payment_account_id
            if (method.journal_id.company_id != company or method.code != 'manual' or method.payment_type != 'inbound'
                    or method.journal_id.type != 'bank' or not account or account.account_type != 'asset_current'
                    or not account.reconcile or account == method.journal_id.default_account_id):
                raise ValidationError(_('Configure un medio manual de entrada, diario bancario y cuenta conciliable de valores (activo corriente) distinta de la cuenta bancaria.'))
            if method in (company.arg_receipt_method_id | company.arg_payment_method_id):
                raise ValidationError(_('El medio de cheques debe ser distinto del medio habitual de efectivo o banco.'))
            if self.env['account.payment'].search_count([('company_id', '=', company.id),
                    ('payment_method_line_id', '=', method.id), ('arg_value_instrument_id', '=', False)]):
                raise ValidationError(_('Use un medio nuevo para cheques; este medio ya tiene pagos sin instrumento identificado.'))


class AccountMoveMoney(models.Model):
    _inherit = 'account.move'

    def _arg_payment_cash_fraction(self, payment, counterpart, invoice_amount):
        value = payment.arg_value_instrument_id
        if not value:
            if payment.payment_method_line_id == payment.company_id.arg_value_receipt_method_id:
                return None
            return super()._arg_payment_cash_fraction(payment, counterpart, invoice_amount)
        if not value.has_access('read'):
            return None
        if (not payment.has_access('read') or not counterpart.has_access('read') or not payment.move_id.has_access('read')
                or payment.move_id != counterpart.move_id or payment.move_id.state != 'posted'
                or value.receipt_line_id.payment_id != payment or payment.arg_treasury_document_id.reverted_at):
            return None
        if value.state in ('portfolio', 'deposited'):
            return 0.0
        if (value.state == 'settled' and value.settlement_move_id.state == 'posted'
                and payment.move_id.state == 'posted' and value.receipt_line_id.payment_id == payment
                and not payment.arg_treasury_document_id.reverted_at):
            return invoice_amount
        return None

    @api.depends('state', 'amount_total', 'amount_residual', 'line_ids.matched_debit_ids', 'line_ids.matched_credit_ids',
                 'line_ids.matched_debit_ids.debit_move_id.move_id.state', 'line_ids.matched_credit_ids.credit_move_id.move_id.state',
                 'line_ids.matched_debit_ids.debit_move_id.move_id.arg_value_instrument_id.state',
                 'line_ids.matched_credit_ids.credit_move_id.move_id.arg_value_instrument_id.state',
                 'line_ids.matched_debit_ids.debit_move_id.move_id.arg_value_instrument_id.settlement_move_id.state',
                 'line_ids.matched_credit_ids.credit_move_id.move_id.arg_value_instrument_id.settlement_move_id.state')
    def _compute_arg_completion_axes(self):
        super()._compute_arg_completion_axes()
