import uuid
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

_QUANT_ENGINE = object()
_INVENTORY_ENGINE = object()


class Product(models.Model):
    _inherit = 'product.product'
    arg_stock_revision = fields.Char(readonly=True, copy=False, default=lambda self: uuid.uuid4().hex, groups='base.group_user')

    @api.model_create_multi
    def create(self, vals_list):
        if any('arg_stock_revision' in values for values in vals_list) or self.env.context.get('default_arg_stock_revision'):
            raise AccessError(_('La revisión técnica de stock se administra automáticamente.'))
        return super().create(vals_list)

    def write(self, values):
        if 'arg_stock_revision' in values:
            raise AccessError(_('La revisión técnica de stock no se edita.'))
        return super().write(values)

    def _arg_lock_stock(self, touch=False):
        self.check_access('read')
        result = {}
        for product in self.sorted('id'):
            product.flush_recordset(['arg_stock_revision'])
            if touch:
                self.env.cr.execute('UPDATE product_product SET arg_stock_revision=%s WHERE id=%s RETURNING arg_stock_revision',
                                    [uuid.uuid4().hex, product.id])
            else:
                # Effective row update participates in native repeatable-read conflict/retry handling, including new quants.
                self.env.cr.execute('UPDATE product_product SET arg_stock_revision=arg_stock_revision WHERE id=%s RETURNING arg_stock_revision', [product.id])
            result[product.id] = self.env.cr.fetchone()[0]
            product.invalidate_recordset(['arg_stock_revision'])
        return result


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.su and self.env.context.get('_arg_quant_engine') is not _QUANT_ENGINE:
            if any(values.get('quantity') or values.get('reserved_quantity') for values in vals_list) or self.env.context.get('default_quantity') or self.env.context.get('default_reserved_quantity'):
                raise AccessError(_('Las existencias cambian mediante movimientos nativos, no mediante cantidades directas.'))
        products = self.env['product.product'].browse(list({values.get('product_id') or self.env.context.get('default_product_id') for values in vals_list} - {False, None}))
        products._arg_lock_stock(touch=True)
        return super().create(vals_list)

    def write(self, values):
        physical = {'quantity', 'reserved_quantity', 'product_id', 'location_id', 'lot_id', 'package_id', 'owner_id'}
        if physical & values.keys() and not self.env.su and self.env.context.get('_arg_quant_engine') is not _QUANT_ENGINE:
            raise AccessError(_('Use movimientos o ajustes nativos; no edite existencias directamente.'))
        if (physical | {'lot_id', 'package_id', 'owner_id'}) & values.keys():
            self.product_id._arg_lock_stock(touch=True)
        return super().write(values)

    def unlink(self):
        self.product_id._arg_lock_stock(touch=True)
        return super().unlink()

    @api.model
    def _update_available_quantity(self, *args, **kwargs):
        return super(StockQuant, self.with_context(_arg_quant_engine=_QUANT_ENGINE))._update_available_quantity(*args, **kwargs)

    def action_apply_inventory(self, date=None):
        if not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Aplicar diferencias requiere responsable ARG.'))
        return super().action_apply_inventory(date=date)

    def _get_inventory_move_values(self, *args, **kwargs):
        values = super()._get_inventory_move_values(*args, **kwargs)
        context = self.env.context.get('_arg_inventory_engine')
        if isinstance(context, tuple) and len(context) == 2 and context[0] is _INVENTORY_ENGINE:
            values['arg_inventory_adjustment_id'] = context[1]
        return values


class StockMatrix(models.AbstractModel):
    _name = 'arg.pyme.stock.matrix'
    _description = 'Consulta de existencias ARG'

    @api.model
    def _authorize(self):
        if self.env.user.share or not (self.env.user.has_group('arg_pyme_base.group_stock') or self.env.user.has_group('arg_pyme_base.group_admin')):
            raise AccessError(_('Se requiere acceso Stock ARG.'))

    @api.model
    def options(self):
        self._authorize()
        warehouses = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=200)
        locations = self.env['stock.location'].search([('company_id', '=', self.env.company.id), ('usage', '=', 'internal')], limit=500)
        return {'company': self.env.company.display_name,
                'warehouses': [{'id': row.id, 'name': row.display_name} for row in warehouses],
                'locations': [{'id': row.id, 'name': row.complete_name} for row in locations]}

    @api.model
    def page(self, warehouse_id, location_id=False, query='', offset=0):
        self._authorize()
        if type(warehouse_id) is not int or type(offset) is not int or offset < 0:
            raise ValidationError(_('Elija un depósito y una página válidos.'))
        warehouse = self.env['stock.warehouse'].browse(warehouse_id).exists()
        warehouse.check_access('read')
        if not warehouse or warehouse.company_id != self.env.company:
            raise AccessError(_('El depósito debe pertenecer a la compañía activa.'))
        context = {'allowed_company_ids': [self.env.company.id], 'warehouse_id': warehouse.id}
        if location_id:
            if type(location_id) is not int:
                raise ValidationError(_('Ubicación no válida.'))
            location = self.env['stock.location'].browse(location_id).exists()
            location.check_access('read')
            if not location or location.company_id != self.env.company or location.usage != 'internal' or not location.parent_path.startswith(warehouse.view_location_id.parent_path):
                raise AccessError(_('La ubicación debe pertenecer al depósito elegido.'))
            context['location'] = location.id
        product_model = self.env['product.product'].with_context({
            'lang': self.env.context.get('lang'), 'tz': self.env.context.get('tz'), **context})
        domain = [('is_storable', '=', True), ('company_id', 'in', [False, self.env.company.id])]
        query = str(query or '').strip()[:120]
        if query:
            domain += ['|', ('name', 'ilike', query), ('default_code', 'ilike', query)]
        products = product_model.search(domain, limit=30, offset=offset, order='default_code,id')
        quant_domain = list(products._get_domain_locations()[0]) + [('product_id', 'in', products.ids), ('company_id', '=', self.env.company.id)]
        grouped = self.env['stock.quant']._read_group(quant_domain, ['product_id'], ['reserved_quantity:sum'])
        reserved = {product.id: quantity for product, quantity in grouped}
        return {'company': self.env.company.display_name, 'warehouse': warehouse.display_name,
                'as_of': str(fields.Datetime.now()), 'count': product_model.search_count(domain), 'offset': offset,
                'rows': [{'id': product.id, 'code': product.default_code or '', 'name': product.display_name,
                          'unit': product.uom_id.display_name, 'physical': product.qty_available,
                          'reserved': reserved.get(product.id, 0), 'available': product.free_qty,
                          'incoming': product.incoming_qty, 'outgoing': product.outgoing_qty, 'forecast': product.virtual_available,
                          'other_unavailable': product.qty_available - reserved.get(product.id, 0) - product.free_qty}
                         for product in products]}
