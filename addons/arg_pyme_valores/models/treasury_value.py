from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.addons.arg_pyme_administracion.models.treasury_document import _TREASURY_ENGINE, check_manager
from .value_event import _VALUE_ENGINE, value_engine


class TreasuryLine(models.Model):
    _inherit = 'arg.pyme.treasury.line'
    value_instrument_id = fields.Many2one('arg.pyme.value.instrument', string='Cheque', check_company=True, ondelete='restrict')

    value_transmission = fields.Selection([('endorsement', 'Endoso registrado'), ('assignment', 'Cesión registrada'),
                                          ('delivery', 'Entrega sin nuevo endoso'), ('own_delivery', 'Entrega de propio')], string='Transmisión')
    value_title_clause = fields.Selection([('order', 'A la orden'), ('not_order', 'No a la orden'),
                                          ('bearer', 'Al portador'), ('blank', 'Endoso previo en blanco')], string='Cláusula conocida')
    value_reference = fields.Char(string='Constancia de entrega')
    value_recourse_condition = fields.Selection([('with_recourse', 'Con responsabilidad declarada'),
                                                ('without_recourse', 'Sin responsabilidad declarada'),
                                                ('unknown', 'Por determinar')], default='unknown', string='Alcance declarado')
    value_reversal_move_id = fields.Many2one('account.move', readonly=True, copy=False, check_company=True, ondelete='restrict')
    value_bank_move_id = fields.Many2one('account.move', readonly=True, copy=False, check_company=True, ondelete='restrict')
    value_exposure_open = fields.Boolean(readonly=True, copy=False)
    value_exposure_closed_on = fields.Date(readonly=True, copy=False)
    value_exposure_reference = fields.Char(readonly=True, copy=False)

    @api.depends('document_id.arg_number','value_instrument_id.arg_number','method_id.name')
    def _compute_display_name(self):
        for line in self:
            line.display_name = '%s · %s' % (line.document_id.arg_number or _('Borrador'),
                                            line.value_instrument_id.arg_number or line.method_id.name or _('Medio'))

    def _arg_value_role(self):
        self.ensure_one()
        return 'receipt' if self.document_id.kind == 'REC' else ('own_out' if self.value_instrument_id.ownership == 'own' else 'third_out')

    def _arg_value_inverse(self):
        self.ensure_one()
        inverse = self.value_reversal_move_id
        if not inverse and self.document_id.kind == 'REC':
            legacy = self.value_instrument_id.rejection_move_id
            if legacy.reversed_entry_id == self.payment_id.move_id:
                inverse = legacy
        return inverse if inverse and inverse.state == 'posted' and inverse.reversed_entry_id == self.payment_id.move_id else self.env['account.move']

    @api.model
    def _value_line_effect_fields(self):
        return {'value_reversal_move_id', 'value_bank_move_id', 'value_exposure_open',
                'value_exposure_closed_on', 'value_exposure_reference'}

    @api.model_create_multi
    def create(self, vals_list):
        keys = self._value_line_effect_fields()
        if not value_engine(self.env) and (any(keys & v.keys() for v in vals_list) or any('default_'+k in self.env.context for k in keys)):
            raise AccessError(_('Los efectos del cheque se asignan desde su operación.'))
        return super().create(vals_list)

    def write(self, vals):
        if not value_engine(self.env):
            if self._value_line_effect_fields() & vals.keys():
                raise AccessError(_('Los efectos del cheque no se editan manualmente.'))
            if {'value_instrument_id', 'amount', 'method_id', 'document_id'} & vals.keys():
                for line in self:
                    if line.value_instrument_id.reservation_line_id == line:
                        raise UserError(_('Libere la reserva antes de cambiar este medio.'))
        return super().write(vals)

    def unlink(self):
        if any(line.value_instrument_id.reservation_line_id == line for line in self):
            raise UserError(_('Libere la reserva antes de eliminar el medio.'))
        return super().unlink()

    @api.onchange('value_instrument_id')
    def _onchange_value_instrument(self):
        if self.value_instrument_id:
            self.amount = self.value_instrument_id.amount
            company = self.document_id.company_id
            role = self._arg_value_role()
            self.method_id = company._arg_value_default_method(role)
            self.value_transmission = 'own_delivery' if role == 'own_out' else False


class TreasuryDocument(models.Model):
    _inherit = 'arg.pyme.treasury.document'
    corrected_value_amount = fields.Monetary(string='Valores revertidos', compute='_compute_corrected_values', compute_sudo=False)

    @api.depends('line_ids.amount', 'line_ids.value_reversal_move_id.state', 'line_ids.value_instrument_id.rejection_move_id.state')
    def _compute_corrected_values(self):
        for doc in self:
            doc.corrected_value_amount = sum(doc.line_ids.filtered(lambda l: l.value_instrument_id and l._arg_value_inverse()).mapped('amount'))

    def _arg_lock_document_only(self):
        return super()._arg_lock()

    def _arg_lock(self):
        self.ensure_one()
        self._arg_check(manager=True)
        if self.env.context.get('_arg_value_lock_scope') is not _VALUE_ENGINE:
            for value in self.line_ids.value_instrument_id.sorted('id'):
                value._arg_value_lock()
        return super()._arg_lock()

    def _arg_prepare_confirmation(self):
        super()._arg_prepare_confirmation()
        lines = self.line_ids.filtered('value_instrument_id')
        values = lines.value_instrument_id
        if len(values) != len(lines):
            raise UserError(_('Un mismo cheque no puede aparecer dos veces en el recibo.'))
        for instrument in values.sorted('id'):
            instrument._arg_finance_lock()
        if self.kind == 'OPA':
            for line in lines.sorted('id'):
                line.value_instrument_id._arg_reserve_delivery(line)

    def _arg_check_line_configuration(self, line):
        super()._arg_check_line_configuration(line)
        value = line.value_instrument_id
        if not value:
            if self.company_id._arg_value_method_role(line.method_id):
                raise UserError(_('Seleccione el cheque para usar el medio de valores.'))
            return
        if self.kind == 'REC':
            value._arg_check_receipt(line)
        else:
            value._arg_check_delivery(line)

    def _arg_create_line_payment(self, line):
        value = line.value_instrument_id
        if not value:
            return super()._arg_create_line_payment(line)
        debt = self._arg_debt_lines()
        if len(debt.account_id) > 1:
            raise UserError(_('Las facturas usan distintas cuentas. Prepare recibos separados.'))
        payment = self.env['account.payment'].with_context(_arg_value_engine=_VALUE_ENGINE, _arg_value_lock_scope=_VALUE_ENGINE).create({
            'company_id': self.company_id.id, 'partner_id': self.partner_id.commercial_partner_id.id,
            'partner_type': 'customer' if self.kind == 'REC' else 'supplier',
            'payment_type': 'inbound' if self.kind == 'REC' else 'outbound', 'date': self.date,
            'currency_id': self.currency_id.id, 'amount': line.amount,
            'journal_id': line.method_id.journal_id.id, 'payment_method_line_id': line.method_id.id,
            'memo': self.arg_number + ' · ' + value.arg_number,
            'arg_treasury_document_id': self.id, 'arg_value_instrument_id': value.id,
            'arg_value_line_id': line.id, 'arg_value_role': line._arg_value_role()})
        payment.action_post()
        counterpart = payment.move_id.line_ids.filtered(lambda l: l.account_type == ('asset_receivable' if self.kind == 'REC' else 'liability_payable'))
        if debt and debt.account_id != counterpart.account_id:
            raise UserError(_('Las facturas y el cheque deben usar la misma cuenta a cobrar.'))
        for due in debt.sorted(lambda l: (l.date_maturity or l.date, l.id)):
            if not counterpart.reconciled and not due.reconciled:
                (counterpart | due).with_context(_arg_value_engine=_VALUE_ENGINE).reconcile()
        return payment

    def _arg_finalize_line_payment(self, line, payment):
        super()._arg_finalize_line_payment(line, payment)
        if line.value_instrument_id:
            if self.kind == 'REC':
                line.value_instrument_id._arg_receive(line, payment)
            else:
                line.value_instrument_id._arg_deliver(line, payment)

    def _arg_line_snapshot(self, line):
        result = super()._arg_line_snapshot(line)
        if line.value_instrument_id:
            result.update(instrument_id=line.value_instrument_id.id, instrument=line.value_instrument_id.arg_number,
                          classification=line._arg_value_role(), transmission=line.value_transmission, reference=line.value_reference or self.arg_reference)
        return result

    def _arg_effect_payments(self):
        return super()._arg_effect_payments().filtered(lambda p: not p.arg_value_instrument_id or not p._arg_value_line() or not p._arg_value_line()._arg_value_inverse())

    def _arg_effect_nominal(self):
        return super()._arg_effect_nominal() - self.corrected_value_amount

    def _arg_payment_expected(self, payment):
        line = payment._arg_value_line() if payment.arg_value_instrument_id else self.env['arg.pyme.treasury.line']
        inverse = line._arg_value_inverse() if line else self.env['account.move']
        if inverse:
            return True
        if payment.arg_value_instrument_id and not line:
            return False
        return super()._arg_payment_expected(payment)

    @api.depends('line_ids.amount', 'confirmed_at', 'reverted_at', 'payment_ids.state',
                 'payment_ids.move_id.line_ids.amount_residual_currency', 'payment_ids.move_id.state',
                 'line_ids.value_instrument_id.state', 'line_ids.value_instrument_id.rejection_move_id.state', 'line_ids.value_reversal_move_id.state')
    def _compute_amounts(self):
        super()._compute_amounts()

    @api.depends('confirmed_at', 'canceled_at', 'reverted_at', 'payment_ids.state', 'payment_ids.move_id.state',
                 'line_ids.value_instrument_id.state', 'line_ids.value_instrument_id.rejection_move_id.state', 'line_ids.value_reversal_move_id.state')
    def _compute_status(self):
        super()._compute_status()

    @api.depends('payment_ids.move_id.line_ids.matched_debit_ids', 'payment_ids.move_id.line_ids.matched_credit_ids',
                 'line_ids.value_instrument_id.state', 'line_ids.value_reversal_move_id.state')
    def _compute_partials(self):
        super()._compute_partials()

    def _arg_before_reverse(self):
        super()._arg_before_reverse()
        for line in self.line_ids.filtered('value_instrument_id'):
            value = line.value_instrument_id
            value._arg_finance_lock()
            if line._arg_value_inverse():
                continue
            if self.kind == 'OPA':
                raise UserError(_('Registre la devolución del cheque %s antes de revertir la orden de pago.', value.arg_number))
            if value.state != 'portfolio' or value.reservation_line_id:
                raise UserError(_('Resuelva la reserva, depósito o salida del cheque %s antes de revertir el recibo.', value.arg_number))

    def _arg_reverse(self, date, reason, key):
        self._arg_lock()
        corrected = self.line_ids and all(l.value_instrument_id and l._arg_value_inverse() for l in self.line_ids)
        if self.confirmed_at and not self.reverted_at and corrected:
            date = fields.Date.to_date(date)
            if not date or not (reason or '').strip():
                raise UserError(_('Complete fecha y motivo de reversión.'))
            if not self._arg_operation(key, 'reverse_request', {'date': str(date), 'reason': reason}):
                return self._arg_action()
            doc = self._arg_value_operation_context().with_context(_arg_treasury_engine=_TREASURY_ENGINE)
            inverses = self.env['account.move']
            for line in self.line_ids:
                inverses |= line._arg_value_inverse()
            doc.write({'reverted_at': fields.Datetime.now(), 'reversal_move_ids': [Command.set(inverses.ids)]})
            doc._arg_event('reverse', {'date': str(date), 'reason': reason, 'move_ids': inverses.ids, 'already_corrected': True})
            return self._arg_action()
        return super(TreasuryDocument, self._arg_value_operation_context())._arg_reverse(date, reason, key)

    def _arg_apply(self, move, key):
        self._arg_lock()
        return super(TreasuryDocument, self._arg_value_operation_context())._arg_apply(move, key)

    def _arg_unapply(self, ids, reason, key):
        self._arg_lock()
        return super(TreasuryDocument, self._arg_value_operation_context())._arg_unapply(ids, reason, key)

    def _arg_value_operation_context(self):
        clean = {k: v for k, v in self.env.context.items() if not k.startswith('default_')}
        return self.with_context(clean, _arg_value_engine=_VALUE_ENGINE, _arg_value_lock_scope=_VALUE_ENGINE)

    def _arg_after_reverse(self, inverses, date, reason):
        super()._arg_after_reverse(inverses, date, reason)
        for line in self.line_ids.filtered(lambda l: l.value_instrument_id and not l._arg_value_inverse()):
            value = line.value_instrument_id
            inverse = inverses.filtered(lambda m: m.reversed_entry_id == line.payment_id.move_id)
            inverse.with_context(_arg_value_engine=_VALUE_ENGINE).write({'arg_value_instrument_id': value.id})
            line.with_context(_arg_value_engine=_VALUE_ENGINE).write({'value_reversal_move_id': inverse.id})
            value.with_context(_arg_value_engine=_VALUE_ENGINE).write({'state': 'returned', 'rejection_move_id': inverse.id})
            value._record_draft_event('receipt_reversed', {'date': str(date), 'reason': reason, 'move_id': inverse.id})

    def action_reserve_values(self):
        self._arg_lock()
        if self.kind != 'OPA' or self.confirmed_at or self.canceled_at:
            raise UserError(_('Reserve cheques desde una OPA en borrador.'))
        self._arg_prepare_confirmation()
        return self._arg_action()

    def action_release_values(self):
        self._arg_lock()
        if self.confirmed_at or self.canceled_at:
            raise UserError(_('La liberación corresponde a reservas de borradores.'))
        for value in self.line_ids.value_instrument_id.sorted('id'):
            value._arg_finance_lock()
            if value.reservation_line_id.document_id == self:
                value._arg_release_delivery(value.reservation_line_id)
        return self._arg_action()

    def action_cancel_draft(self):
        self._arg_lock()
        if not self.confirmed_at:
            for value in self.line_ids.value_instrument_id.sorted('id'):
                value._arg_finance_lock()
                if value.reservation_line_id.document_id == self:
                    value._arg_release_delivery(value.reservation_line_id)
        return super().action_cancel_draft()

    def _arg_report_payload(self):
        result = super()._arg_report_payload()
        if self.corrected_value_amount:
            result['totals'].append({'label': _('Valores revertidos'), 'amount': self.corrected_value_amount})
        return result


class Company(models.Model):
    _inherit = 'res.company'
    arg_value_receipt_method_id = fields.Many2one('account.payment.method.line', string='Medio de recepción de cheques ARG', check_company=True)

    arg_value_third_out_method_id = fields.Many2one('account.payment.method.line', string='Medio de entrega de cheques de terceros ARG', check_company=True)
    arg_value_own_out_method_id = fields.Many2one('account.payment.method.line', string='Medio de entrega de cheques propios ARG', check_company=True)

    def _arg_value_default_method(self, role):
        self.ensure_one()
        return self[{'receipt': 'arg_value_receipt_method_id', 'third_out': 'arg_value_third_out_method_id', 'own_out': 'arg_value_own_out_method_id'}[role]]

    def _arg_value_method_role(self, method):
        self.ensure_one()
        if not method:
            return False
        if method.arg_value_kind:
            return method.arg_value_kind
        current = next((role for role in ('receipt','third_out','own_out') if method == self._arg_value_default_method(role)), False)
        if current:
            return current
        account = method.payment_account_id
        if not account:
            return False
        registered = self.env['account.payment.method.line'].search_count([
            ('company_id','=',self.id), ('payment_account_id','=',account.id), ('arg_value_kind','!=',False)])
        historical = self.env['account.payment'].search_count([
            ('company_id','=',self.id), ('outstanding_account_id','=',account.id), ('arg_value_instrument_id','!=',False)])
        if registered or historical:
            if account.account_type == 'liability_current' and method.payment_type == 'outbound':
                return 'own_out'
            if account.account_type == 'asset_current':
                return 'receipt' if method.payment_type == 'inbound' else 'third_out'
            return 'restricted'
        return False

    def _arg_tag_value_methods(self):
        for company in self:
            for role in ('receipt','third_out','own_out'):
                method = company._arg_value_default_method(role)
                if method and not method.arg_value_kind:
                    method.with_context(_arg_value_engine=_VALUE_ENGINE).write({'arg_value_kind': role})

    def write(self, vals):
        profile_keys = {'arg_value_receipt_method_id','arg_value_third_out_method_id','arg_value_own_out_method_id'}
        if profile_keys & vals.keys():
            if not self.env.user.has_group('base.group_system'):
                raise AccessError(_('La configuración de medios de valores requiere un administrador.'))
            self._arg_tag_value_methods()
        result = super().write(vals)
        if profile_keys & vals.keys():
            self._arg_tag_value_methods()
        return result

    @api.constrains('arg_value_receipt_method_id','arg_value_third_out_method_id','arg_value_own_out_method_id',
                    'arg_receipt_method_id','arg_payment_method_id')
    def _check_value_method(self):
        for company in self:
            for role in ('receipt','third_out','own_out'):
                method = company._arg_value_default_method(role)
                if not method:
                    continue
                method._arg_validate_value_kind(role)
                if method.journal_id.company_id != company or (method.arg_value_kind and method.arg_value_kind != role):
                    raise ValidationError(_('El medio no corresponde al rol o compañía configurados.'))
                if method in (company.arg_receipt_method_id | company.arg_payment_method_id):
                    raise ValidationError(_('Los medios de cheques deben ser distintos de los medios habituales de efectivo o banco.'))
                if self.env['account.payment'].search_count([('company_id','=',company.id), ('payment_method_line_id','=',method.id), ('arg_value_instrument_id','=',False)]):
                    raise ValidationError(_('Use un medio sin pagos históricos anónimos para registrar cheques.'))
            for regular in company.arg_receipt_method_id | company.arg_payment_method_id:
                if company._arg_value_method_role(regular):
                    raise ValidationError(_('El medio habitual de caja/banco no puede reutilizar una cuenta de valores u obligaciones de cheques.'))


class AccountMoveMoney(models.Model):
    _inherit = 'account.move'

    def _arg_payment_cash_fraction(self, payment, counterpart, invoice_amount):
        value = payment.arg_value_instrument_id
        if not value:
            if payment.company_id._arg_value_method_role(payment.payment_method_line_id):
                return None
            return super()._arg_payment_cash_fraction(payment, counterpart, invoice_amount)
        if not value.has_access('read') or not payment.has_access('read') or not counterpart.has_access('read') or not payment.move_id.has_access('read'):
            return None
        line = payment._arg_value_line()
        if (not line or payment.move_id != counterpart.move_id or payment.move_id.state != 'posted'
                or payment.arg_treasury_document_id.reverted_at or line._arg_value_inverse()):
            return None
        role = payment._arg_value_effect_role()
        if role == 'receipt':
            if value.state == 'settled' and value.settlement_move_id.state == 'posted':
                return invoice_amount
            return 0.0 if value.state in ('portfolio','deposited','reserved','transferred','transferred_closed','disputed') else None
        if role == 'third_out':
            return 0.0
        if role == 'own_out':
            return invoice_amount if line.value_bank_move_id.state == 'posted' else 0.0
        return None

    @api.depends('state', 'amount_total', 'amount_residual', 'line_ids.matched_debit_ids', 'line_ids.matched_credit_ids',
                 'line_ids.matched_debit_ids.debit_move_id.move_id.state', 'line_ids.matched_credit_ids.credit_move_id.move_id.state',
                 'line_ids.matched_debit_ids.debit_move_id.move_id.arg_value_instrument_id.state',
                 'line_ids.matched_credit_ids.credit_move_id.move_id.arg_value_instrument_id.state',
                 'line_ids.matched_debit_ids.debit_move_id.move_id.arg_value_instrument_id.settlement_move_id.state',
                 'line_ids.matched_credit_ids.credit_move_id.move_id.arg_value_instrument_id.settlement_move_id.state',
                 'line_ids.matched_debit_ids.debit_move_id.payment_id.arg_value_line_id.value_bank_move_id.state',
                 'line_ids.matched_credit_ids.credit_move_id.payment_id.arg_value_line_id.value_bank_move_id.state')
    def _compute_arg_completion_axes(self):
        super()._compute_arg_completion_axes()
