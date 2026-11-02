import json
from odoo import api, fields, models, _
from odoo.exceptions import AccessError
from .treasury_document import engine, check_manager, _TREASURY_ENGINE


class AuditEvent(models.Model):
    _name = 'arg.pyme.treasury.audit.event'
    _description = 'Evidencia financiera ARG'
    _order = 'id desc'
    _check_company_auto = True
    document_id = fields.Many2one('arg.pyme.treasury.document', required=True, check_company=True, ondelete='restrict', index=True)
    company_id = fields.Many2one('res.company', required=True, index=True)
    kind = fields.Selection([
        ('confirm_prepare','Preparación de confirmación'), ('confirm','Confirmación'),
        ('apply_prepare','Preparación de aplicación'), ('apply','Aplicación'), ('apply_request','Solicitud de aplicación'),
        ('unapply_request','Solicitud de desaplicación'), ('unapply','Desaplicación'),
        ('reverse_request','Solicitud de reversión'), ('reverse_prepare','Preparación de reversión'),
        ('reverse','Reversión'), ('cancel','Cancelación de borrador')], required=True, string='Operación')
    request_key = fields.Char(required=True, readonly=True)
    request_hash = fields.Char(readonly=True)
    actor_id = fields.Many2one('res.users', required=True, ondelete='restrict', string='Usuario')
    event_date = fields.Datetime(required=True, string='Fecha')
    currency_id = fields.Many2one('res.currency', required=True)
    payload = fields.Json(required=True, readonly=True)
    evidence_text = fields.Text(string='Detalle de evidencia', compute='_compute_evidence_text', compute_sudo=False)
    native_partial_id = fields.Integer(readonly=True, index=True)
    caused_by_id = fields.Many2one('arg.pyme.treasury.audit.event', readonly=True, ondelete='restrict')
    inverse_of_id = fields.Many2one('arg.pyme.treasury.audit.event', readonly=True, ondelete='restrict')
    _request_unique = models.Constraint('UNIQUE(document_id, request_key)', 'La operación ya tiene evidencia.')

    @api.depends('payload')
    def _compute_evidence_text(self):
        for event in self:
            event.evidence_text = json.dumps(event.payload, ensure_ascii=False, indent=2)

    @api.model_create_multi
    def create(self, values_list):
        if not engine(self.env):
            raise AccessError(_('La evidencia se genera desde operaciones financieras autorizadas.'))
        return super().create(values_list)

    def write(self, values):
        raise AccessError(_('La evidencia financiera es inmutable.'))

    def unlink(self):
        raise AccessError(_('La evidencia financiera se conserva.'))


class PartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    @api.model
    def _arg_documents_for_lines(self, lines):
        lines.check_access('read')
        return lines.move_id.arg_treasury_document_id

    def _arg_audit_partial(self, kind):
        for partial in self:
            lines = partial.debit_move_id | partial.credit_move_id
            docs = self._arg_documents_for_lines(lines)
            for doc in docs:
                doc._arg_lock()
                before = self.env['arg.pyme.treasury.audit.event'].search([
                    ('document_id', '=', doc.id), ('native_partial_id', '=', partial.id), ('kind', '=', 'apply')], order='id desc', limit=1)
                payload = {'partial_id': partial.id, 'debit_line_id': partial.debit_move_id.id, 'credit_line_id': partial.credit_move_id.id,
                           'debit_move_id': partial.debit_move_id.move_id.id, 'credit_move_id': partial.credit_move_id.move_id.id,
                           'company_amount': partial.amount, 'debit_currency_id': partial.debit_currency_id.id,
                           'credit_currency_id': partial.credit_currency_id.id, 'debit_amount': partial.debit_amount_currency,
                           'credit_amount': partial.credit_amount_currency, 'max_date': str(partial.max_date)}
                doc._arg_event(kind, payload, native_partial_id=partial.id, inverse_of_id=before.id if kind == 'unapply' else False)

    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
            lines = self.env['account.move.line'].browse([values['debit_move_id'], values['credit_move_id']])
            docs = self._arg_documents_for_lines(lines)
            for doc in docs.sorted('id'):
                doc._arg_lock()
                doc._arg_event('apply_prepare', {'debit_line_id': lines[0].id, 'credit_line_id': lines[1].id,
                      'company_amount': values.get('amount'), 'debit_amount': values.get('debit_amount_currency'),
                      'credit_amount': values.get('credit_amount_currency')})
        partials = super().create(values_list)
        partials._arg_audit_partial('apply')
        return partials

    def write(self, values):
        protected = {'debit_move_id', 'credit_move_id', 'amount', 'debit_amount_currency', 'credit_amount_currency', 'company_id'}
        if protected.intersection(values):
            docs = (self.debit_move_id | self.credit_move_id).move_id.arg_treasury_document_id
            endpoints = [values[k] for k in ('debit_move_id', 'credit_move_id') if values.get(k)]
            if endpoints:
                docs |= self._arg_documents_for_lines(self.env['account.move.line'].browse(endpoints))
            if docs:
                raise AccessError(_('La aplicación financiera conserva sus importes y apuntes. Desaplique y vuelva a aplicar.'))
        return super().write(values)

    def unlink(self):
        docs = (self.debit_move_id | self.credit_move_id).move_id.arg_treasury_document_id
        self._arg_audit_partial('unapply')
        if docs:
            return super(PartialReconcile, self.with_context(_arg_treasury_engine=_TREASURY_ENGINE)).unlink()
        return super().unlink()
