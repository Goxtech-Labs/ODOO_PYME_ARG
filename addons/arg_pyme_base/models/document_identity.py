import re
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError, UserError

DOCUMENT_TYPES = [
    ('PRE', 'Presupuesto', 'arg.pyme.quotation'), ('PED', 'Pedido de cliente', 'sale.order'),
    ('REM', 'Remito de salida', 'stock.picking'), ('FAC', 'Factura de venta', 'account.move'),
    ('NCV', 'Nota de crédito venta', 'account.move'), ('DCL', 'Devolución de cliente', 'stock.picking'),
    ('PPC', 'Pedido a proveedor', 'purchase.order'), ('ENT', 'Entrada de mercadería', 'stock.picking'),
    ('FRC', 'Factura recibida', 'account.move'), ('NCP', 'Nota de crédito proveedor', 'account.move'),
    ('DCP', 'Devolución a proveedor', 'stock.picking'), ('TRA', 'Transferencia interna', 'stock.picking'),
    ('INV', 'Conteo de inventario', 'arg.pyme.inventory.count'), ('AJU', 'Ajuste de inventario', 'arg.pyme.inventory.adjustment'),
    ('SAL', 'Salida interna', 'stock.picking'), ('REC', 'Recibo de cobranza', 'arg.pyme.treasury.document'),
    ('OPA', 'Orden de pago', 'arg.pyme.treasury.document'),
]

class DocumentType(models.Model):
    _name = 'arg.pyme.document.type'
    _description = 'Tipo documental ARG'
    _order = 'company_id, code'
    _check_company_auto = True

    name = fields.Char(required=True, string='Documento')
    code = fields.Char(required=True, string='Código corto', size=4)
    document_model = fields.Char(required=True, string='Modelo operativo')
    company_id = fields.Many2one('res.company', required=True, default=lambda s: s.env.company, index=True)
    sequence_id = fields.Many2one('ir.sequence', required=True, check_company=True, ondelete='restrict', copy=False)
    active = fields.Boolean(default=True)
    _sequence_unique = models.Constraint('UNIQUE(sequence_id)', 'Cada tipo documental necesita su propia secuencia.')
    _company_code_unique = models.Constraint('UNIQUE(company_id, code)', 'El código ya existe en esta compañía.')

    @api.constrains('code', 'sequence_id', 'company_id')
    def _check_definition(self):
        for rec in self:
            if not re.fullmatch(r'[A-Z]{2,4}', rec.code or ''):
                raise ValidationError(_('El código debe tener de dos a cuatro letras mayúsculas.'))
            seq = rec.sequence_id
            if seq.company_id != rec.company_id or seq.prefix or seq.suffix or seq.use_date_range:
                raise ValidationError(_('La secuencia debe ser propia de la compañía, sin prefijo, sufijo ni reinicio por fecha.'))

    def write(self, values):
        if {'code', 'company_id', 'document_model', 'sequence_id'} & values.keys():
            if self.env['arg.pyme.document.identity'].sudo().search_count([('document_type_id', 'in', self.ids)]):
                raise UserError(_('No se puede cambiar la identidad de un tipo que ya tiene documentos.'))
        return super().write(values)

    @api.model
    def _ensure_companies(self, companies):
        # Only a trusted installation/company lifecycle calls this allocator setup.
        for company in companies:
            for code, name, model in DOCUMENT_TYPES:
                types = self.sudo().with_company(company).with_context(active_test=False)
                if types.search_count([('company_id', '=', company.id), ('code', '=', code)]):
                    continue
                seq = self.env['ir.sequence'].sudo().create({
                    'name': name + ' ARG · ' + company.name, 'code': 'arg.' + code.lower(),
                    'company_id': company.id, 'padding': 0, 'number_increment': 1,
                    'prefix': '', 'suffix': '', 'use_date_range': False,
                })
                types.create({'code': code, 'name': name, 'document_model': model,
                              'company_id': company.id, 'sequence_id': seq.id})

class DocumentIdentity(models.Model):
    _name = 'arg.pyme.document.identity'
    _description = 'Identidad documental ARG'
    _rec_name = 'code'
    _order = 'id desc'
    _check_company_auto = True

    company_id = fields.Many2one('res.company', required=True, index=True, ondelete='restrict')
    document_type_id = fields.Many2one('arg.pyme.document.type', required=True, check_company=True, ondelete='restrict')
    number = fields.Integer(required=True, readonly=True)
    code = fields.Char(required=True, readonly=True, index=True)
    document_model = fields.Char(required=True, readonly=True)
    document_res_id = fields.Integer(required=True, readonly=True)
    _number_unique = models.Constraint('UNIQUE(company_id, document_type_id, number)', 'El número documental ya fue asignado.')
    _origin_unique = models.Constraint('UNIQUE(document_model, document_res_id, document_type_id)', 'El documento ya tiene identidad.')
    _positive_number = models.Constraint('CHECK(number > 0 AND document_res_id > 0)', 'La referencia debe ser positiva.')

    @api.model_create_multi
    def create(self, values_list):
        if not self.env.su:
            raise AccessError(_('La numeración sólo se asigna desde un documento operativo.'))
        return super().create(values_list)

    def write(self, values):
        raise UserError(_('La identidad asignada es inmutable.'))

    def unlink(self):
        raise UserError(_('Las identidades se conservan incluso si un documento se anula.'))

    @api.model
    def _allocate_for(self, document, code):
        document.ensure_one()
        document.check_access('write')
        if not getattr(document, '_arg_document_enabled', False):
            raise ValidationError(_('El modelo no pertenece al registro documental ARG.'))
        company = document.company_id
        if company not in self.env.companies:
            raise AccessError(_('La compañía no está habilitada para este usuario.'))
        doc_type = self.env['arg.pyme.document.type'].search([
            ('company_id', '=', company.id), ('code', '=', code), ('document_model', '=', document._name)], limit=1)
        if not doc_type:
            raise ValidationError(_('Falta configurar el tipo documental para esta compañía.'))
        # An effective row update makes concurrent REPEATABLE READ requests retry with a new snapshot.
        document.flush_recordset()
        from odoo.tools import SQL
        if not document._log_access:
            raise ValidationError(_('El registro documental necesita auditoría nativa.'))
        self.env.cr.execute(SQL('UPDATE %s SET write_date = clock_timestamp(), write_uid = %s WHERE id = %s', SQL.identifier(document._table), self.env.uid, document.id))
        document.invalidate_recordset(['write_date', 'write_uid'])
        identities = self.sudo()
        identity = identities.search([('document_model', '=', document._name),
                                      ('document_res_id', '=', document.id), ('document_type_id', '=', doc_type.id)], limit=1)
        if identity:
            return identity
        number = int(doc_type.sequence_id.sudo().next_by_id())
        return identities.create({'company_id': company.id, 'document_type_id': doc_type.id,
                                  'number': number, 'code': '%s-%06d' % (code, number),
                                  'document_model': document._name, 'document_res_id': document.id})

    def action_open_document(self):
        self.ensure_one()
        if self.document_model != self.document_type_id.document_model or self.document_model not in self.env:
            raise AccessError(_('Referencia operativa no disponible.'))
        record = self.env[self.document_model].browse(self.document_res_id).exists()
        if not record or not getattr(record, '_arg_document_enabled', False):
            raise AccessError(_('Documento no disponible.'))
        record.check_access('read')
        return {'type': 'ir.actions.act_window', 'res_model': record._name, 'res_id': record.id, 'view_mode': 'form'}


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    def write(self, values):
        protected = {'prefix', 'suffix', 'company_id', 'use_date_range', 'number_increment',
                     'number_next', 'number_next_actual', 'padding', 'implementation', 'code'}
        if protected & values.keys() and self.env['arg.pyme.document.type'].sudo().with_context(active_test=False).search_count([('sequence_id', 'in', self.ids)]):
            raise UserError(_('Una secuencia documental ARG no puede reiniciarse ni cambiar su formato.'))
        return super().write(values)
