from odoo import api, models, _
from odoo.exceptions import ValidationError


class DocumentType(models.Model):
    _inherit = 'arg.pyme.document.type'

    @api.model
    def _ensure_companies(self, companies):
        result = super()._ensure_companies(companies)
        for company in companies:
            self._ensure_repair_type(company, 'REP', 'Parte de reparación', 'arg.pyme.repair.case')
            self._ensure_repair_type(company, 'PTM', 'Parte de trabajo', 'arg.pyme.repair.intervention')
        return result

    @api.model
    def _ensure_repair_type(self, company, code, name, model):
        # Trusted installation/company setup only; never sudo a repair operation.
        types = self.sudo().with_company(company).with_context(active_test=False)
        existing = types.search([('company_id', '=', company.id), ('code', '=', code)])
        if existing:
            if existing.document_model != model:
                raise ValidationError(_('%s ya identifica otro documento en esta compañía.', code))
            return
        sequence = self.env['ir.sequence'].sudo().create({
            'name': name + ' ARG · ' + company.name,
            'code': 'arg.' + code.lower(), 'company_id': company.id, 'padding': 0,
            'number_increment': 1, 'prefix': '', 'suffix': '', 'use_date_range': False,
        })
        types.create({'name': name, 'code': code,
                      'document_model': model, 'company_id': company.id,
                      'sequence_id': sequence.id})
