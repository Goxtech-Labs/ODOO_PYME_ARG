from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Presentation only: native residuals and reconciliation remain the sole ledger.
    # Non-stored/non-aggregated fields deliberately avoid adding currencies in grouped lists.
    arg_account_original = fields.Monetary(
        string='Importe original', currency_field='currency_id', compute='_compute_arg_current_account',
        compute_sudo=False, aggregator=False, groups='arg_pyme_base.group_administracion')
    arg_account_residual = fields.Monetary(
        string='Saldo: deuda (+), crédito (−)', currency_field='currency_id', compute='_compute_arg_current_account',
        compute_sudo=False, aggregator=False, groups='arg_pyme_base.group_administracion')
    arg_account_company_residual = fields.Monetary(
        string='Saldo en moneda compañía', currency_field='company_currency_id', compute='_compute_arg_current_account',
        compute_sudo=False, aggregator=False, groups='arg_pyme_base.group_administracion')
    arg_account_document = fields.Char(
        string='Documento', compute='_compute_arg_current_account', compute_sudo=False,
        groups='arg_pyme_base.group_administracion')
    arg_account_origin_type = fields.Char(
        string='Tipo de origen', compute='_compute_arg_current_account', compute_sudo=False,
        groups='arg_pyme_base.group_administracion')
    arg_account_progress = fields.Selection(
        [('unposted', 'Sin publicar'), ('pending', 'Pendiente'), ('partial', 'Parcial'), ('complete', 'Saldado')],
        string='Cancelación de deuda / aplicación de crédito', compute='_compute_arg_current_account',
        compute_sudo=False, groups='arg_pyme_base.group_administracion')

    @api.depends('move_id.name', 'move_id.move_type', 'move_id.origin_payment_id', 'move_id.state',
                 'account_id.account_type', 'amount_currency', 'balance', 'amount_residual_currency',
                 'amount_residual', 'currency_id', 'company_currency_id')
    def _compute_arg_current_account(self):
        names = {'out_invoice': _('Factura de venta'), 'out_refund': _('Nota de crédito de venta'),
                 'in_invoice': _('Factura recibida'), 'in_refund': _('Nota de crédito del proveedor')}
        for line in self:
            direction = -1 if line.account_type == 'liability_payable' else 1
            line.arg_account_original = line.amount_currency * direction
            line.arg_account_residual = line.amount_residual_currency * direction
            line.arg_account_company_residual = line.amount_residual * direction
            line.arg_account_document = getattr(line.move_id, 'arg_number', False) or line.move_id.name or _('Sin número')
            line.arg_account_origin_type = names.get(line.move_id.move_type) or (
                _('Pago / anticipo') if line.move_id.origin_payment_id else _('Apunte contable'))
            if line.move_id.state != 'posted':
                status = 'unposted'
            elif line.currency_id.is_zero(line.amount_residual_currency) and line.company_currency_id.is_zero(line.amount_residual):
                status = 'complete'
            elif (line.currency_id.compare_amounts(abs(line.amount_residual_currency), abs(line.amount_currency)) < 0
                  or line.company_currency_id.compare_amounts(abs(line.amount_residual), abs(line.balance)) < 0):
                status = 'partial'
            else:
                status = 'pending'
            line.arg_account_progress = status

    def action_arg_account_document(self):
        self.ensure_one()
        self.check_access('read')
        if (not self.env.user.has_group('arg_pyme_base.group_administracion')
                or self.company_id not in self.env.companies):
            raise AccessError(_('La consulta requiere Administración ARG en una compañía habilitada.'))
        self.move_id.check_access('read')
        return {'type': 'ir.actions.act_window', 'name': _('Documento de origen'),
                'res_model': 'account.move', 'res_id': self.move_id.id,
                'views': [(False, 'form')], 'target': 'current'}
