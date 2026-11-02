from odoo import api, models, _
from odoo.exceptions import AccessError, ValidationError

class DocumentReport(models.AbstractModel):
    _name = 'report.arg_pyme_documentos.document_report'
    _description = 'Impresión documental ARG'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = (data or {}).get('arg_model')
        if not isinstance(model,str) or model not in self.env or (not getattr(self.env[model],'_arg_document_enabled',False) or self.env[model]._abstract):
            raise AccessError(_('Modelo documental no disponible.'))
        docids = docids or (data or {}).get('arg_ids')
        if not isinstance(docids,list) or not docids or len(docids) > 100 or any(type(i) is not int or i <= 0 for i in docids):
            raise ValidationError(_('Seleccione de uno a cien documentos.'))
        records = self.env[model].browse(docids).exists()
        if len(records) != len(set(docids)): raise AccessError(_('Documento no disponible.'))
        pages = []
        for record in records:
            record._arg_check_document_access()
            if not record.arg_identity_id: raise ValidationError(_('Documento sin identidad ARG.'))
            payload = dict(record._arg_report_payload())
            # Identity, live state and demo labels cannot be supplied by caller-controlled report data.
            payload.update(number=record.arg_number,demo=record.arg_demo,draft=getattr(record,'state',None)=='draft')
            payload.setdefault('company',record.company_id.name)
            payload.setdefault('axes',record._arg_get_completion_axes())
            pages.append(payload)
        return {'doc_ids':records.ids,'doc_model':model,'docs':records,'pages':pages}
