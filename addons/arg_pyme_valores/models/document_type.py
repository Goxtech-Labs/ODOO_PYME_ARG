from odoo import api, models, _
from odoo.exceptions import ValidationError


VALUE_TYPES = [
    ('CHQ', 'Cheque', 'arg.pyme.value.instrument'),
    ('PAG', 'Pagaré', 'arg.pyme.value.instrument'),
]


class DocumentType(models.Model):
    _inherit = 'arg.pyme.document.type'

    @api.model
    def _ensure_companies(self, companies):
        result = super()._ensure_companies(companies)
        # Installation/company lifecycle only. Business records are never sudoed.
        for company in companies:
            for code, name, model in VALUE_TYPES:
                types = self.sudo().with_company(company).with_context(active_test=False)
                existing = types.search([('company_id', '=', company.id), ('code', '=', code)])
                if existing:
                    if existing.document_model != model:
                        raise ValidationError(_('El código %s ya pertenece a otro documento en esta compañía.', code))
                    continue
                sequence = self.env['ir.sequence'].sudo().create({
                    'name': name + ' ARG · ' + company.name,
                    'code': 'arg.' + code.lower(), 'company_id': company.id,
                    'padding': 0, 'number_increment': 1, 'prefix': '', 'suffix': '',
                    'use_date_range': False,
                })
                types.create({'name': name, 'code': code, 'document_model': model,
                              'company_id': company.id, 'sequence_id': sequence.id})
        return result
