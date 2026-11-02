import uuid
from odoo import fields, models, _
from odoo.exceptions import UserError


class ApplyWizard(models.TransientModel):
    _name = 'arg.pyme.treasury.apply.wizard'
    _description = 'Aplicar saldo financiero ARG'
    document_id = fields.Many2one('arg.pyme.treasury.document', required=True, readonly=True)
    company_id = fields.Many2one(related='document_id.company_id')
    partner_id = fields.Many2one(related='document_id.partner_id')
    commercial_partner_id = fields.Many2one(related='document_id.partner_id.commercial_partner_id')
    kind = fields.Selection(related='document_id.kind')
    move_id = fields.Many2one('account.move', string='Factura', required=True)
    request_key = fields.Char(default=lambda s: str(uuid.uuid4()), required=True, readonly=True)

    def action_apply(self):
        self.ensure_one()
        return self.document_id._arg_apply(self.move_id, self.request_key)


class ReverseWizard(models.TransientModel):
    _name = 'arg.pyme.treasury.reverse.wizard'
    _description = 'Revertir recibo / pago ARG'
    document_id = fields.Many2one('arg.pyme.treasury.document', required=True, readonly=True)
    date = fields.Date(string='Fecha', default=fields.Date.context_today, required=True)
    reason = fields.Text(string='Motivo', required=True)
    request_key = fields.Char(default=lambda s: str(uuid.uuid4()), required=True, readonly=True)

    def action_reverse(self):
        self.ensure_one()
        return self.document_id._arg_reverse(self.date, self.reason, self.request_key)


class UnapplyWizard(models.TransientModel):
    _name = 'arg.pyme.treasury.unapply.wizard'
    _description = 'Desaplicar documento financiero ARG'
    document_id = fields.Many2one('arg.pyme.treasury.document', required=True, readonly=True)
    target_ids = fields.Json(required=True, readonly=True)
    reason = fields.Text(string='Motivo', required=True)
    request_key = fields.Char(default=lambda s: str(uuid.uuid4()), required=True, readonly=True)

    def action_unapply(self):
        self.ensure_one()
        return self.document_id._arg_unapply(self.target_ids, self.reason, self.request_key)
