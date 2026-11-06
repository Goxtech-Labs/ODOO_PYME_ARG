from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from .value_event import _VALUE_ENGINE, value_engine


class PaymentMethod(models.Model):
    _inherit = 'account.payment.method.line'
    arg_value_kind = fields.Selection([('receipt','Recepción de cheque'), ('third_out','Entrega de tercero'),
                                       ('own_out','Entrega de propio')], readonly=True, copy=False, string='Uso en Valores ARG')

    @api.model_create_multi
    def create(self, vals_list):
        if not value_engine(self.env) and (any(v.get('arg_value_kind') for v in vals_list) or self.env.context.get('default_arg_value_kind')):
            raise AccessError(_('El uso de valores se configura desde la compañía.'))
        result = super().create(vals_list)
        for method in result.filtered('arg_value_kind'):
            method._arg_validate_value_kind(method.arg_value_kind)
        return result

    def write(self, vals):
        if 'arg_value_kind' in vals:
            if not value_engine(self.env):
                raise AccessError(_('El uso del medio se configura desde la compañía.'))
            if any(m.arg_value_kind and vals['arg_value_kind'] != m.arg_value_kind for m in self):
                raise UserError(_('El medio conserva su uso; configure otro para un rol distinto.'))
        result = super().write(vals)
        for method in self.filtered('arg_value_kind'):
            method._arg_validate_value_kind(method.arg_value_kind)
        return result

    def _arg_validate_value_kind(self, role):
        self.ensure_one()
        account = self.payment_account_id
        direction = 'inbound' if role == 'receipt' else 'outbound'
        account_type = 'liability_current' if role == 'own_out' else 'asset_current'
        if (self.code != 'manual' or self.payment_type != direction or self.journal_id.type != 'bank'
                or not account or account.account_type != account_type or not account.reconcile
                or account == self.journal_id.default_account_id):
            raise ValidationError(_('Use un medio bancario manual del sentido correcto y una cuenta conciliable de cartera/obligación, distinta de banco.'))
        if self.env['account.payment'].search_count([('payment_method_line_id','=',self.id), ('arg_value_instrument_id','=',False)]):
            raise ValidationError(_('Ese medio tiene pagos sin instrumento; configure otro.'))
        if self.env['account.payment'].search_count([('company_id','=',self.company_id.id),
                ('outstanding_account_id','=',account.id), ('arg_value_instrument_id','=',False)]):
            raise ValidationError(_('La cuenta tiene pagos históricos sin instrumento. Use una cuenta exclusiva de valores.'))


class Payment(models.Model):
    _inherit = 'account.payment'
    arg_value_instrument_id = fields.Many2one('arg.pyme.value.instrument', readonly=True, copy=False, check_company=True, ondelete='restrict', index=True)

    arg_value_line_id = fields.Many2one('arg.pyme.treasury.line', readonly=True, copy=False, check_company=True, ondelete='restrict', index=True)
    arg_value_role = fields.Selection([('receipt','Recepción'), ('third_out','Salida de tercero'), ('own_out','Salida propia')], readonly=True, copy=False)
    arg_value_pre12_payment = fields.Boolean(readonly=True, copy=False, string='Pago anterior a la política de valores1.2')

    @api.model_create_multi
    def create(self, vals_list):
        if not value_engine(self.env):
            keys = {'arg_value_line_id','arg_value_role','arg_value_pre12_payment'}
            if any(keys & v.keys() for v in vals_list) or any('default_'+k in self.env.context for k in keys):
                raise AccessError(_('El rol y medio de origen se generan desde REC/OPA.'))
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
                if method.company_id._arg_value_method_role(method) and not value_id:
                    raise UserError(_('Use un recibo ARG con el cheque identificado para este medio.'))
        records = super().create(vals_list)
        records._check_value_payment_method(strict=True)
        return records

    def write(self, vals):
        posting_ids = set()
        if vals.get('state') in ('paid','reconciled'):
            posting_ids = {p.id for p in self if p.state not in ('paid','reconciled') or p.move_id.state != 'posted'}
        if {'arg_value_instrument_id','arg_value_line_id','arg_value_role','arg_value_pre12_payment'} & vals.keys() and not value_engine(self.env):
            raise AccessError(_('El pago conserva el cheque de origen.'))
        if vals.get('move_id') and not value_engine(self.env) and self.env['account.move'].browse(vals['move_id']).arg_value_instrument_id:
            raise AccessError(_('El asiento del valor no se reasigna a otro pago.'))
        result = super().write(vals)
        effect_fields = {'date','amount','payment_type','partner_type','currency_id','partner_id','company_id',
                         'journal_id','payment_method_line_id','destination_account_id','outstanding_account_id','move_id'}
        for payment in self:
            payment._check_value_payment_method(strict=bool(effect_fields & vals.keys()) or payment.id in posting_ids)
        return result

    def _arg_value_line(self):
        self.ensure_one()
        if self.arg_value_line_id:
            return self.arg_value_line_id
        legacy = self.arg_value_instrument_id.receipt_line_id
        return legacy if legacy.payment_id == self else self.env['arg.pyme.treasury.line']

    def _arg_value_effect_role(self):
        self.ensure_one()
        return self.arg_value_role or ('receipt' if self._arg_value_line().document_id.kind == 'REC' else False)

    def _check_value_payment_method(self, strict=False):
        for payment in self:
            role = payment.company_id._arg_value_method_role(payment.payment_method_line_id)
            if role and not payment.arg_value_instrument_id and (strict or not payment.arg_value_pre12_payment):
                raise UserError(_('El medio de cheques requiere un instrumento identificado por REC/OPA.'))
            if payment.arg_value_instrument_id:
                line = payment._arg_value_line()
                if (not role and not payment.arg_value_role and not payment.arg_value_line_id and line
                        and line.document_id.kind == 'REC' and line.payment_id == payment
                        and payment.arg_value_instrument_id.receipt_line_id == line
                        and payment.outstanding_account_id == payment.arg_value_instrument_id.portfolio_account_id):
                    role = 'receipt'
                if (not line or line.document_id != payment.arg_treasury_document_id
                        or line.value_instrument_id != payment.arg_value_instrument_id
                        or (line.payment_id and line.payment_id != payment)
                        or payment._arg_value_effect_role() != line._arg_value_role() or role != line._arg_value_role()
                        or payment.company_id != line.company_id or payment.currency_id != line.currency_id
                        or payment.currency_id.compare_amounts(payment.amount, line.amount)):
                    raise UserError(_('El cheque, rol y pago deben coincidir con su medio documental.'))

    def action_post(self):
        for payment in self:
            existing = payment.state in ('paid','reconciled') and payment.move_id.state == 'posted'
            payment._check_value_payment_method(strict=not existing)
        return super().action_post()

    @api.depends('state','move_id.state','arg_treasury_document_id.reverted_at','move_id.reversal_move_ids.state',
                 'arg_value_line_id.value_reversal_move_id.state','arg_value_instrument_id.rejection_move_id.state')
    def _compute_arg_payment_effect(self):
        super()._compute_arg_payment_effect()
        for payment in self.filtered('arg_value_instrument_id'):
            line = payment._arg_value_line()
            if line and line._arg_value_inverse():
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
