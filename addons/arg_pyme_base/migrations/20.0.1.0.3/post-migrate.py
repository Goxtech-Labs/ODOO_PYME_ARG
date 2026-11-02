from odoo import api, SUPERUSER_ID, _
from odoo.exceptions import UserError


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    types = env['arg.pyme.document.type'].with_context(active_test=False).search([
        ('code', '=', 'AJU'), ('document_model', '=', 'stock.move')])
    if env['arg.pyme.document.identity'].search_count([('document_type_id', 'in', types.ids)]):
        raise UserError(_('AJU conserva identidades del modelo anterior. Prepare una migración explícita de sus referencias antes de cambiar el registro; no se renumeraron documentos.'))
    types.write({'document_model': 'arg.pyme.inventory.adjustment'})
