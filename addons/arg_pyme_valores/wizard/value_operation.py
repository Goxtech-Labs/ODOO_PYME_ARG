import uuid
from odoo import fields, models, _


class ValueOperationWizard(models.TransientModel):
    _name = 'arg.pyme.value.operation.wizard'
    _description = 'Operación de cheque ARG'
    instrument_id = fields.Many2one('arg.pyme.value.instrument', required=True, readonly=True)
    company_id = fields.Many2one(related='instrument_id.company_id')
    date = fields.Date(string='Fecha', required=True, default=fields.Date.context_today)
    operation = fields.Selection([('deposited', 'Registrar depósito'), ('settled', 'Registrar acreditación completa'),
                                  ('rejected', 'Registrar rechazo y revertir su cobro')], required=True, string='Operación')
    journal_id = fields.Many2one('account.journal', string='Banco de depósito')
    reference = fields.Char(string='Constancia / motivo', required=True)
    request_key = fields.Char(default=lambda s: str(uuid.uuid4()), required=True, readonly=True)

    def action_confirm(self):
        self.ensure_one()
        return self.instrument_id._arg_operation_value(self.operation, self.date, self.reference, self.journal_id, self.request_key)
