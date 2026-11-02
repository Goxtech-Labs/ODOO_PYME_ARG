from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
from ..report.export import csv_bytes


class Export(http.Controller):
    @http.route('/arg/informes/<int:query_id>/csv',type='http',auth='user',methods=['GET'])
    def csv(self,query_id,**kwargs):
        query=request.env['arg.pyme.report.query'].browse(query_id).exists()
        if not query:raise NotFound()
        query.check_access('read')
        data=request.env['arg.pyme.report.engine']._snapshot(query)
        return request.make_response(csv_bytes(data),headers=[('Content-Type','text/csv; charset=utf-8'),
            ('Content-Disposition','attachment; filename="informe-arg.csv"'),('Cache-Control','no-store'),('X-Content-Type-Options','nosniff')])
