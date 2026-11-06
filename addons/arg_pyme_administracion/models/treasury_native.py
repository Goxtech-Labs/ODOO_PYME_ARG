from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from .treasury_document import engine, _TREASURY_ENGINE, check_manager


class PaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    arg_treasury_document_id = fields.Many2one('arg.pyme.treasury.document', readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        if (any(v.get('arg_treasury_document_id') for v in vals_list) or self.env.context.get('default_arg_treasury_document_id')) and not engine(self.env):
            raise AccessError(_('El origen financiero se asigna desde el documento ARG.'))
        return super().create(vals_list)

    def write(self, vals):
        if 'arg_treasury_document_id' in vals and not engine(self.env):
            raise AccessError(_('El origen financiero no se reasigna.'))
        return super().write(vals)

    def _init_payments(self, to_process, edit_mode=False):
        self.ensure_one()
        if self.arg_treasury_document_id:
            if not engine(self.env):
                raise AccessError(_('Prepare el cobro o pago desde su documento ARG.'))
            self.arg_treasury_document_id._arg_check(manager=True)
            for item in to_process:
                item['create_vals']['arg_treasury_document_id'] = self.arg_treasury_document_id.id
        return super()._init_payments(to_process, edit_mode=edit_mode)


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    arg_treasury_document_id = fields.Many2one('arg.pyme.treasury.document', readonly=True, copy=False,
                                              check_company=True, ondelete='restrict', index=True)

    @api.model_create_multi
    def create(self, vals_list):
        if not engine(self.env):
            moves = self.env['account.move'].browse([v.get('move_id') or self.env.context.get('default_move_id') for v in vals_list
                                                   if v.get('move_id') or self.env.context.get('default_move_id')])
            if moves.arg_treasury_document_id:
                raise AccessError(_('El asiento ARG no se puede asociar a otro pago.'))
        if (any(v.get('arg_treasury_document_id') for v in vals_list) or self.env.context.get('default_arg_treasury_document_id')) and not engine(self.env):
            raise AccessError(_('El vínculo de pago se asigna al confirmar REC/OPA.'))
        return super().create(vals_list)

    def write(self, vals):
        if not engine(self.env):
            if 'arg_treasury_document_id' in vals:
                raise AccessError(_('El pago conserva su documento de origen.'))
            if vals.get('move_id') and self.env['account.move'].browse(vals['move_id']).arg_treasury_document_id:
                raise AccessError(_('El asiento ARG no se puede asociar a otro pago.'))
            owned = self.filtered('arg_treasury_document_id')
            immutable = {'date', 'amount', 'payment_type', 'partner_type', 'currency_id', 'partner_id', 'company_id',
                         'journal_id', 'payment_method_line_id', 'destination_account_id', 'outstanding_account_id', 'move_id', 'memo'}
            if owned and immutable.intersection(vals):
                raise UserError(_('El pago de REC/OPA conserva sus datos y asiento. Use Revertir en el documento ARG.'))
            if owned and 'state' in vals:
                # Native computed paid/reconciled transitions do not alter the monetary effect.
                if any(p.state not in ('paid', 'reconciled') or vals['state'] not in ('paid', 'reconciled') or p.move_id.state != 'posted' for p in owned):
                    raise UserError(_('Use las acciones del documento ARG para cambiar sus efectos.'))
        return super().write(vals)

    def unlink(self):
        if self.filtered('arg_treasury_document_id'):
            raise UserError(_('Los pagos vinculados a REC/OPA se conservan con su evidencia.'))
        return super().unlink()

    def _generate_move_vals(self, *args, **kwargs):
        vals = super()._generate_move_vals(*args, **kwargs)
        if self.arg_treasury_document_id:
            vals['arg_treasury_document_id'] = self.arg_treasury_document_id.id
        return vals

    def _arg_lifecycle(self):
        if self.filtered('arg_treasury_document_id') and not engine(self.env):
            raise UserError(_('Realice la operación desde REC/OPA para conservar sus efectos e historial.'))

    def action_post(self):
        self._arg_lifecycle()
        return super().action_post()

    def action_draft(self):
        self._arg_lifecycle()
        return super().action_draft()

    def action_cancel(self):
        self._arg_lifecycle()
        return super().action_cancel()

    def action_reject(self):
        self._arg_lifecycle()
        return super().action_reject()


class AccountMove(models.Model):
    _inherit = 'account.move'
    arg_treasury_document_id = fields.Many2one('arg.pyme.treasury.document', readonly=True, copy=False,
                                              check_company=True, ondelete='restrict', index=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            origin = vals.get('arg_treasury_document_id') or self.env.context.get('default_arg_treasury_document_id')
            payment_id = vals.get('origin_payment_id') or self.env.context.get('default_origin_payment_id')
            payment = self.env['account.payment'].browse(payment_id) if payment_id else self.env['account.payment']
            if (origin or payment.arg_treasury_document_id) and not engine(self.env):
                raise AccessError(_('Los asientos de REC/OPA se generan desde el pago autorizado.'))
        return super().create(vals_list)

    def write(self, vals):
        if not engine(self.env):
            if 'arg_treasury_document_id' in vals:
                raise AccessError(_('El asiento conserva su documento ARG.'))
            owned = self.filtered('arg_treasury_document_id')
            if owned and {'line_ids', 'state', 'date', 'journal_id', 'company_id', 'partner_id', 'currency_id', 'origin_payment_id', 'reversed_entry_id', 'name', 'ref', 'auto_post', 'posted_before'}.intersection(vals):
                raise UserError(_('El asiento financiero se conserva. Use Revertir en REC/OPA.'))
            if vals.get('origin_payment_id') and self.env['account.payment'].browse(vals['origin_payment_id']).arg_treasury_document_id:
                raise AccessError(_('El origen financiero no se reasigna.'))
        return super().write(vals)

    def unlink(self):
        if self.filtered('arg_treasury_document_id'):
            raise UserError(_('Los asientos de REC/OPA no se eliminan.'))
        return super().unlink()

    def _reverse_moves(self, *args, **kwargs):
        if self.filtered('arg_treasury_document_id') and not engine(self.env):
            raise UserError(_('Use Revertir en REC/OPA para conservar evidencia y aplicaciones.'))
        return super()._reverse_moves(*args, **kwargs)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model_create_multi
    def create(self, vals_list):
        if not engine(self.env):
            ids = [v.get('move_id') or self.env.context.get('default_move_id') for v in vals_list]
            if self.env['account.move'].browse([i for i in ids if i]).arg_treasury_document_id:
                raise AccessError(_('Los apuntes de REC/OPA se generan desde sus operaciones autorizadas.'))
        return super().create(vals_list)

    def write(self, vals):
        if not engine(self.env):
            owned = self.move_id.arg_treasury_document_id
            if vals.get('move_id'):
                owned |= self.env['account.move'].browse(vals['move_id']).arg_treasury_document_id
            if owned and {'move_id', 'company_id', 'partner_id', 'account_id', 'currency_id', 'date', 'date_maturity',
                          'balance', 'debit', 'credit', 'amount_currency', 'amount_residual', 'amount_residual_currency',
                          'tax_ids', 'tax_line_id', 'matched_debit_ids', 'matched_credit_ids', 'parent_state', 'reconciled', 'full_reconcile_id', 'payment_id', 'statement_line_id', 'journal_id', 'account_type', 'company_currency_id'}.intersection(vals):
                raise UserError(_('Los apuntes financieros conservan sus importes y dimensiones. Use las acciones de REC/OPA.'))
        return super().write(vals)

    def unlink(self):
        if self.move_id.arg_treasury_document_id:
            raise UserError(_('Los apuntes financieros se conservan.'))
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
        docs = lines.move_id.arg_treasury_document_id
        if docs:
            for doc in docs.sorted('id'):
                doc._arg_lock()
            clean = {k: v for k, v in self.env.context.items() if not k.startswith('default_')}
            return super(AccountMoveLine, self.with_context(clean, _arg_treasury_engine=_TREASURY_ENGINE))._reconcile_plan(reconciliation_plan)
        return super()._reconcile_plan(reconciliation_plan)
