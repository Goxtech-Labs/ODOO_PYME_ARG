from odoo import api, models, _
from odoo.exceptions import ValidationError


class DocumentType(models.Model):
    _inherit = 'arg.pyme.document.type'

    @api.model
    def _ensure_companies(self, companies):
        result = super()._ensure_companies(companies)
        for company in companies:
            # Trusted installation/company setup only; never sudo a repair operation.
            types = self.sudo().with_company(company).with_context(active_test=False)
            existing = types.search([('company_id', '=', company.id), ('code', '=', 'REP')])
            if existing:
                if existing.document_model != 'arg.pyme.repair.case':
                    raise ValidationError(_('REP ya identifica otro documento en esta compañía.'))
                continue
            sequence = self.env['ir.sequence'].sudo().create({
                'name': 'Parte de reparación ARG · ' + company.name,
                'code': 'arg.rep', 'company_id': company.id, 'padding': 0,
                'number_increment': 1, 'prefix': '', 'suffix': '', 'use_date_range': False,
            })
            types.create({'name': 'Parte de reparación', 'code': 'REP',
                          'document_model': 'arg.pyme.repair.case', 'company_id': company.id,
                          'sequence_id': sequence.id})
        return result
