from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from .value_event import _VALUE_ENGINE, value_engine


class Payment(models.Model):
    _inherit = 'account.payment'
    arg_value_instrument_id = fields.Many2one('arg.pyme.value.instrument', readonly=True, copy=False, check_company=True, ondelete='restrict', index=True)

    @api.model_create_multi
    def create(self, vals_list):
        if not value_engine(self.env):
            ids = [v.get('move_id') or self.env.context.get('default_move_id') for v in vals_list]
            if self.env['account.move'].browse([i for i in ids if i]).arg_value_instrument_id:
                raise AccessError(_('El asiento de un valor no puede asociarse a otro pago.'))
        for vals in vals_list:
            value_id = vals.get('arg_value_instrument_id') or self.env.context.get('default_arg_value_instrument_id')
            if value_id and not value_engine(self.env):
                raise AccessError(_('El vínculo del cheque se asigna desde su recibo.'))
            method_id = vals.get('payment_method_line_id') or self.env.context.get('default_payment_method_line_id')
            if method_id:
                method = self.env['account.payment.method.line'].browse(method_id)
                if method == method.company_id.arg_value_receipt_method_id and not value_id:
                    raise UserError(_('Use un recibo ARG con el cheque identificado para este medio.'))
        records = super().create(vals_list)
        records._check_value_payment_method()
        return records

    def write(self, vals):
        if 'arg_value_instrument_id' in vals and not value_engine(self.env):
            raise AccessError(_('El pago conserva el cheque de origen.'))
        if vals.get('move_id') and not value_engine(self.env) and self.env['account.move'].browse(vals['move_id']).arg_value_instrument_id:
            raise AccessError(_('El asiento del valor no se reasigna a otro pago.'))
        result = super().write(vals)
        self._check_value_payment_method()
        return result

    def _check_value_payment_method(self):
        for payment in self:
            if (payment.payment_method_line_id and payment.payment_method_line_id == payment.company_id.arg_value_receipt_method_id
                    and not payment.arg_value_instrument_id):
                raise UserError(_('El medio de cheques requiere un cheque identificado por su recibo ARG.'))

    def action_post(self):
        self._check_value_payment_method()
        return super().action_post()

    @api.depends('state', 'move_id.state', 'arg_treasury_document_id.reverted_at', 'move_id.reversal_move_ids.state',
                 'arg_value_instrument_id.state', 'arg_value_instrument_id.rejection_move_id.state')
    def _compute_arg_payment_effect(self):
        super()._compute_arg_payment_effect()
        for payment in self:
            value = payment.arg_value_instrument_id
            if value.state in ('rejected', 'returned') and value.rejection_move_id.state == 'posted':
                payment.arg_payment_effect = 'reverted'

    def _generate_move_vals(self, *args, **kwargs):
        result = super()._generate_move_vals(*args, **kwargs)
        if self.arg_value_instrument_id:
            result['arg_value_instrument_id'] = self.arg_value_instrument_id.id
        return result


class Move(models.Model):
    _inherit = 'account.move'
    arg_value_instrument_id = fields.Many2one('arg.pyme.value.instrument', readonly=True, copy=False, check_company=True, ondelete='restrict', index=True)

    @api.model_create_multi
    def create(self, vals_list):
        if not value_engine(self.env) and (any('arg_value_instrument_id' in v for v in vals_list) or 'default_arg_value_instrument_id' in self.env.context):
            raise AccessError(_('Los asientos de valores se generan desde su operación.'))
        return super().create(vals_list)

    def write(self, vals):
        if not value_engine(self.env):
            if 'arg_value_instrument_id' in vals or (self.arg_value_instrument_id and
                    {'line_ids', 'state', 'date', 'journal_id', 'company_id', 'partner_id', 'currency_id', 'origin_payment_id',
                     'reversed_entry_id', 'name', 'ref', 'auto_post', 'posted_before'} & vals.keys()):
                raise UserError(_('Conserve el asiento del valor y use su operación de corrección.'))
        return super().write(vals)

    def unlink(self):
        if self.arg_value_instrument_id:
            raise UserError(_('Los asientos de valores se conservan.'))
        return super().unlink()

    def _reverse_moves(self, *args, **kwargs):
        if self.arg_value_instrument_id and not value_engine(self.env):
            raise UserError(_('Realice la corrección desde la operación del valor.'))
        return super()._reverse_moves(*args, **kwargs)


class MoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model_create_multi
    def create(self, vals_list):
        if not value_engine(self.env):
            ids = [v.get('move_id') or self.env.context.get('default_move_id') for v in vals_list]
            if self.env['account.move'].browse([i for i in ids if i]).arg_value_instrument_id:
                raise AccessError(_('Los apuntes del valor se generan desde su operación.'))
        return super().create(vals_list)

    def write(self, vals):
        if not value_engine(self.env):
            moves = self.move_id
            if vals.get('move_id'):
                moves |= self.env['account.move'].browse(vals['move_id'])
            if moves.arg_value_instrument_id and {'move_id', 'company_id', 'partner_id', 'account_id', 'currency_id', 'date',
                    'date_maturity', 'balance', 'debit', 'credit', 'amount_currency', 'amount_residual', 'amount_residual_currency',
                    'tax_ids', 'tax_line_id', 'matched_debit_ids', 'matched_credit_ids', 'parent_state', 'reconciled',
                    'full_reconcile_id', 'payment_id', 'statement_line_id', 'journal_id', 'account_type', 'company_currency_id'} & vals.keys():
                raise UserError(_('Los apuntes del valor conservan importes y dimensiones.'))
        return super().write(vals)

    def unlink(self):
        if self.move_id.arg_value_instrument_id:
            raise UserError(_('Los apuntes de valores se conservan.'))
        return super().unlink()

    def _reconcile_plan(self, reconciliation_plan):
        lines = self.env['account.move.line']
        def collect(part):
            nonlocal lines
            if isinstance(part, (list, tuple)):
                for nested in part:
                    collect(nested)
            elif getattr(part, '_name', None) == 'account.move.line':
                lines |= part
        collect(reconciliation_plan)
        values = lines.move_id.arg_value_instrument_id
        if values:
            if not value_engine(self.env):
                raise UserError(_('Realice la aplicación o acreditación desde el recibo o el cheque ARG.'))
            for doc in lines.move_id.arg_treasury_document_id.sorted('id'):
                doc._arg_lock()
            for value in values.sorted('id'):
                value._arg_finance_lock()
            return super(MoveLine, self.with_context(_arg_value_engine=_VALUE_ENGINE))._reconcile_plan(reconciliation_plan)
        return super()._reconcile_plan(reconciliation_plan)


class Partial(models.Model):
    _inherit = 'account.partial.reconcile'

    @api.model_create_multi
    def create(self, vals_list):
        if not value_engine(self.env):
            ids = [v.get(key) for v in vals_list for key in ('debit_move_id', 'credit_move_id') if v.get(key)]
            if self.env['account.move.line'].browse(ids).move_id.arg_value_instrument_id:
                raise AccessError(_('Aplique el valor desde su documento ARG.'))
        return super().create(vals_list)

    def write(self, vals):
        lines = self.debit_move_id | self.credit_move_id
        ids = [vals[k] for k in ('debit_move_id', 'credit_move_id') if vals.get(k)]
        lines |= self.env['account.move.line'].browse(ids)
        if lines.move_id.arg_value_instrument_id and not value_engine(self.env):
            raise UserError(_('Las aplicaciones del valor se corrigen desde su documento ARG.'))
        return super().write(vals)

    def unlink(self):
        if (self.debit_move_id | self.credit_move_id).move_id.arg_value_instrument_id and not value_engine(self.env):
            raise UserError(_('Desaplique el valor desde su recibo ARG.'))
        return super().unlink()
