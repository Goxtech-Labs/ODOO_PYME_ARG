from odoo import api, fields, models


class CashMoveLine(models.Model):
    _inherit = 'account.move.line'
    arg_cash_amount = fields.Monetary(string='Movimiento en moneda del apunte', currency_field='currency_id',
        compute='_compute_arg_cash_presentation', compute_sudo=False, aggregator=False, groups='arg_pyme_base.group_administracion')
    arg_cash_company_amount = fields.Monetary(string='Movimiento en moneda compañía', currency_field='company_currency_id',
        compute='_compute_arg_cash_presentation', compute_sudo=False, aggregator=False, groups='arg_pyme_base.group_administracion')

    @api.depends('amount_currency', 'balance')
    def _compute_arg_cash_presentation(self):
        for line in self:
            line.arg_cash_amount = line.amount_currency
            line.arg_cash_company_amount = line.balance


class RegisteredPayment(models.Model):
    _inherit = 'account.payment'
    arg_registered_amount = fields.Monetary(string='Importe registrado', currency_field='currency_id',
        compute='_compute_arg_registered_amount', compute_sudo=False, aggregator=False, groups='arg_pyme_base.group_administracion')

    arg_payment_effect = fields.Selection([('registered','Registrado'),('reverted','Revertido'),('review','Revisar asiento')],
        string='Efecto registrado', compute='_compute_arg_payment_effect', compute_sudo=False, groups='arg_pyme_base.group_administracion')

    @api.depends('state', 'move_id.state', 'arg_treasury_document_id.reverted_at', 'move_id.reversal_move_ids.state')
    def _compute_arg_payment_effect(self):
        for pay in self:
            if pay.arg_treasury_document_id.reverted_at:
                pay.arg_payment_effect = 'reverted'
            elif pay.state not in ('paid','reconciled') or pay.move_id.state != 'posted' or pay.move_id.reversal_move_ids.filtered(lambda m:m.state == 'posted'):
                pay.arg_payment_effect = 'review'
            else:
                pay.arg_payment_effect = 'registered'

    @api.depends('amount', 'payment_type')
    def _compute_arg_registered_amount(self):
        for pay in self:
            pay.arg_registered_amount = pay.amount * (1 if pay.payment_type == 'inbound' else -1)
