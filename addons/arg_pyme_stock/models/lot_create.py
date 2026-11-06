"""Minimal native-lot registration, with shared identity serialization."""
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


def _product_id(raw):
    if isinstance(raw, models.BaseModel):
        if raw._name != 'product.product' or len(raw) != 1:
            raise ValidationError(_('Producto no válido.'))
        raw = raw.id
    if raw is False or raw is None:
        return False
    if type(raw) is not int or raw <= 0:
        raise ValidationError(_('Producto no válido.'))
    return raw


class StockLotIdentity(models.Model):
    _inherit = 'stock.lot'

    @api.model_create_multi
    def create(self, vals_list):
        if vals_list:
            self.check_access('create')
            default = self.default_get(['product_id']).get('product_id') if any('product_id' not in v for v in vals_list) else False
            identifiers = {_product_id(v.get('product_id', default)) for v in vals_list} - {False}
            self.env['product.product'].browse(sorted(identifiers))._arg_lock_stock()
        return super().create(vals_list)

    def write(self, values):
        if self and {'name', 'product_id', 'company_id'} & values.keys():
            self.check_access('write')
            products = self.product_id
            if 'product_id' in values:
                identifier = _product_id(values['product_id'])
                if identifier:
                    products |= self.env['product.product'].browse(identifier)
            products._arg_lock_stock()
        return super().write(values)


class LotCreate(models.TransientModel):
    _name = 'arg.pyme.lot.create'
    _description = 'Alta mínima de serie/lote ARG'

    product_id = fields.Many2one('product.product', string='Producto', required=True,
        domain="[('is_storable','=',True),('tracking','in',['serial','lot'])]", check_company=True)
    name = fields.Char(string='Serie o lote', required=True)
    ref = fields.Char(string='Referencia del fabricante')
    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)
    created_lot_id = fields.Many2one('stock.lot', readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        if any('created_lot_id' in v for v in vals_list) or self.env.context.get('default_created_lot_id'):
            raise AccessError(_('El resultado del alta se administra automáticamente.'))
        return super().create([{**values, 'created_lot_id': False} for values in vals_list])

    def write(self, values):
        if 'created_lot_id' in values:
            raise AccessError(_('El resultado del alta no se edita.'))
        if {'product_id', 'name', 'ref', 'company_id'} & values.keys() and self.filtered('created_lot_id'):
            raise UserError(_('Esta alta ya terminó. Abrí otro asistente para un lote diferente.'))
        return super().write(values)

    def action_create_lot(self):
        self.ensure_one()
        service = self.env['arg.pyme.stock.trace']._scoped()
        wizard = self.with_env(service.env).exists()
        if not wizard:
            raise UserError(_('El asistente venció. Abrí una nueva alta.'))
        wizard.check_access('write')
        if wizard.company_id != service.env.company:
            raise AccessError(_('El alta pertenece a otra compañía.'))
        service.env['stock.lot'].check_access('create')
        wizard.flush_recordset(['created_lot_id', 'write_date'])
        service.env.cr.execute('UPDATE arg_pyme_lot_create SET write_date=clock_timestamp() WHERE id=%s RETURNING id', [wizard.id])
        if not service.env.cr.fetchone():
            raise UserError(_('El asistente venció. Abrí una nueva alta.'))
        wizard.invalidate_recordset()
        if wizard.created_lot_id:
            return service.from_lot(wizard.created_lot_id.id)
        product = service._record('product.product', wizard.product_id.id, active=True)
        if not product.is_storable or product.tracking not in ('serial', 'lot'):
            raise UserError(_('Elegí un producto almacenable con seguimiento de serie o lote configurado.'))
        name = (wizard.name or '').strip(); reference = (wizard.ref or '').strip()
        if not 1 <= len(name) <= 256 or len(reference) > 256:
            raise ValidationError(_('La serie/lote admite de1 a256 caracteres y la referencia hasta256.'))
        lot = service.env['stock.lot'].create({'product_id': product.id, 'name': name,
                                             'ref': reference, 'company_id': service.env.company.id})
        super(LotCreate, wizard).write({'created_lot_id': lot.id})
        return service.from_lot(lot.id)
