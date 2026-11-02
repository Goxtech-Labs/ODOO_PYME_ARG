from odoo import models

class DocumentLinks(models.AbstractModel):
    _inherit = 'arg.pyme.document.mixin'

    def _arg_document_relations(self):
        # Adapters return [{'label': ..., 'records': native_recordset}]. Origin text is not a relation.
        return []

    def _arg_document_line_relations(self):
        # Each adapter supplies actual ORM references, never only origin text or unguarded IDs.
        # source_document, target_document, source_line, target_line, quantity, unit.
        return []

    def arg_document_links(self):
        self._arg_check_document_access()
        groups = []
        for relation in self._arg_document_relations():
            records = relation['records'].exists()
            visible = []
            for record in records:
                if record.has_access('read') and ('company_id' not in record._fields or not record.company_id or record.company_id in self.env.companies):
                    visible.append({'id':record.id,'name':getattr(record,'arg_number',False) or record.display_name})
            if visible:
                groups.append({'label':relation['label'],'model':records._name,'documents':visible})
        line_links = []
        for relation in self._arg_document_line_relations():
            references = [relation[k] for k in ('source_document','target_document','source_line','target_line')]
            if not all(len(r)==1 and r.exists() and r.has_access('read') for r in references):
                continue
            if any('company_id' in r._fields and r.company_id and r.company_id not in self.env.companies for r in references):
                continue
            source, target, source_line, target_line = references
            line_links.append({'source':{'model':source._name,'id':source.id,'name':getattr(source,'arg_number',False) or source.display_name},
                'target':{'model':target._name,'id':target.id,'name':getattr(target,'arg_number',False) or target.display_name},
                'source_line':source_line.display_name,'target_line':target_line.display_name,
                'quantity':relation['quantity'],'unit':relation['unit']})
        return {'number':self.arg_number,'groups':groups,'line_links':line_links}

    def action_arg_links(self):
        self._arg_check_document_access()
        return {'type':'ir.actions.client','name':'Trazabilidad ARG','tag':'arg_pyme.document_links',
                'params':{'model':self._name,'id':self.id}}
