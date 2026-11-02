import csv
import io
import re
from odoo import api, models, _
from odoo.exceptions import ValidationError


def safe_cell(value):
    if value is None:return ''
    if isinstance(value,str):
        # Spreadsheet applications may skip leading whitespace/BOM/control characters before formulas.
        probe = value.lstrip(' \t\r\n\v\f\ufeff')
        if probe.startswith(('=','+','-','@')) or any(ord(c)<32 for c in value):
            return "'"+value
    return value


def report_cell(row, key):
    value = row.get('export_values', {}).get(key)
    if isinstance(value, str) and re.fullmatch(r'-?[0-9]+(?:\.[0-9]+)?', value):
        # Trusted formatted numeric output, including negatives, remains a spreadsheet number.
        return value
    return safe_cell(row.get(key))


def csv_bytes(data):
    stream=io.StringIO(newline='');writer=csv.writer(stream,quoting=csv.QUOTE_ALL)
    writer.writerow(['Informe',safe_cell(data['title'])]);writer.writerow(['Compañía',safe_cell(data['company'])])
    for label,key in [('Moneda','currency'),('Desde','from'),('Hasta','to'),('Zona horaria','timezone'),('Generado','generated_at'),('Grano','grain'),('Fuente','source_model'),('Criterio fecha','date_basis'),('Tercero','partner'),('Producto','product_filter'),('Ubicación','location_filter'),('Agrupación','group_by'),('Criterio','note')]:
        writer.writerow([label,safe_cell(data[key])])
    writer.writerow([]);writer.writerow([safe_cell(label) for key,label in data['columns']])
    for row in data['rows']:writer.writerow([report_cell(row,key) for key,label in data['columns']])
    writer.writerow([]);writer.writerow(['Totales del corte separados por unidad y hecho físico','Unidad','Cantidad','Reservado','Disponible','Neto','Impuesto por línea','Importe'])
    for row in data['totals']:writer.writerow([safe_cell(row['flow']),safe_cell(row['unit'])]+[report_cell(row,k) for k in ['quantity','reserved','available','net','tax','total']])
    return ('\ufeff'+stream.getvalue()).encode('utf-8')


class ReportPdf(models.AbstractModel):
    _name = 'report.arg_pyme_informes.report_document'
    _description = 'Informe ARG en PDF'

    @api.model
    def _get_report_values(self,docids,data=None):
        if not isinstance(docids,list) or len(docids)!=1 or type(docids[0]) is not int or docids[0]<=0:
            raise ValidationError(_('Seleccione una consulta válida.'))
        query=self.env['arg.pyme.report.query'].browse(docids).exists()
        query.ensure_one();query.check_access('read')
        snapshot=self.env['arg.pyme.report.engine']._snapshot(query)
        if snapshot['result_count']>2000:
            raise ValidationError(_('El PDF admite hasta2000filas; use CSV o reduzca el corte.'))
        return {'docs':query,'doc_model':query._name,'doc_ids':query.ids,'report':snapshot}
