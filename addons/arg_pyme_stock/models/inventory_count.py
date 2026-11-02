import hashlib
import json
import math
from odoo import api, fields, models, Command, _
from odoo.exceptions import AccessError, UserError, ValidationError
from .stock_quant import _INVENTORY_ENGINE
from .stock_picking import _manager


class InventoryCount(models.Model):
    _name = 'arg.pyme.inventory.count'
    _inherit = ['arg.pyme.document.mixin']
    _description = 'Conteo de inventario ARG'
    _rec_name = 'arg_number'
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    location_id = fields.Many2one('stock.location', required=True, check_company=True, string='Ubicación')
    date = fields.Date(required=True, default=fields.Date.context_today, string='Fecha')
    reason = fields.Char(required=True, default='Inventario físico', string='Motivo')
    state = fields.Selection([('draft', 'Borrador'), ('counting', 'En conteo'), ('counted', 'Contado'),
                              ('applied', 'Aplicado'), ('cancel', 'Cancelado')], default='draft', readonly=True)
    line_ids = fields.One2many('arg.pyme.inventory.count.line', 'count_id', string='Detalle')
    adjustment_id = fields.Many2one('arg.pyme.inventory.adjustment', readonly=True, copy=False, check_company=True)
    captured_at = fields.Datetime(readonly=True, copy=False)
    applied_by = fields.Many2one('res.users', readonly=True, copy=False)

    def _arg_document_code(self):
        return 'INV'

    @api.model_create_multi
    def create(self, vals_list):
        protected = ('state', 'adjustment_id', 'captured_at', 'applied_by')
        for values in vals_list:
            if any(values.get(k) or self.env.context.get('default_' + k) for k in protected if k != 'state') or values.get('state', self.env.context.get('default_state', 'draft')) != 'draft':
                raise AccessError(_('El conteo comienza en borrador y conserva su evidencia.'))
            values['state'] = 'draft'
        return super().create(vals_list)

    def _arg_lock(self):
        self.ensure_one()
        self._arg_check_document_access()
        self.check_access('write')
        self.flush_recordset(['write_date'])
        self.env.cr.execute('UPDATE arg_pyme_inventory_count SET write_date=clock_timestamp() WHERE id=%s', [self.id])
        self.invalidate_recordset(['write_date'])

    def write(self, values):
        if {'state', 'adjustment_id', 'captured_at', 'applied_by'} & values.keys():
            raise AccessError(_('Use las acciones de conteo y aplicación.'))
        for count in self:
            count._arg_lock()
            if count.state != 'draft' and {'company_id', 'location_id', 'date', 'reason'} & values.keys():
                raise UserError(_('El conteo iniciado conserva ubicación, fecha y motivo.'))
        return super().write(values)

    def _arg_validate_scope(self):
        if self.location_id.usage != 'internal' or self.location_id.company_id != self.company_id:
            raise UserError(_('El conteo usa una ubicación interna propia de la compañía.'))
        if not self.line_ids or len(self.line_ids) > 500:
            raise UserError(_('Agregue productos; opere hasta quinientas líneas por aplicación. Puede separar conteos por ubicación.'))
        seen = set()
        for line in self.line_ids:
            line.product_id.check_access('read')
            if not line.product_id.is_storable or (line.product_id.company_id and line.product_id.company_id != self.company_id):
                raise UserError(_('Elija productos almacenables de la compañía o compartidos.'))
            if line.product_id.tracking in ('lot', 'serial') and not line.lot_id:
                raise UserError(_('Complete lote o serie para el producto trazable.'))
            if line.lot_id and (line.lot_id.product_id != line.product_id or (line.lot_id.company_id and line.lot_id.company_id != self.company_id)):
                raise UserError(_('El lote/serie debe corresponder al producto y compañía.'))
            key = (line.product_id.id, line.lot_id.id, line.package_id.id, line.owner_id.id)
            if key in seen:
                raise UserError(_('Una combinación de producto, lote, paquete y propietario se cuenta una sola vez.'))
            seen.add(key)

    def action_load_location(self):
        self._arg_lock()
        if self.state != 'draft':
            raise UserError(_('Cargue productos antes de tomar referencia.'))
        if self.line_ids:
            raise UserError(_('La carga de ubicación se usa en un conteo vacío; conserve o retire sus líneas borrador.'))
        quants = self.env['stock.quant'].search([('company_id', '=', self.company_id.id), ('location_id', '=', self.location_id.id)], limit=501)
        if len(quants) > 500:
            raise UserError(_('La ubicación supera la página de carga. Prepare un subconjunto o divida por ubicación.'))
        seen = set()
        values = []
        for quant in quants:
            key = (quant.product_id.id, quant.lot_id.id, quant.package_id.id, quant.owner_id.id)
            if key in seen:
                continue
            seen.add(key)
            values.append(Command.create({'product_id': key[0], 'lot_id': key[1], 'package_id': key[2], 'owner_id': key[3]}))
        self.write({'line_ids': values})
        return True

    def _arg_lock_unit_definitions(self):
        # Freeze the units used by the count against concurrent master-data changes, without changing their values.
        templates = self.line_ids.product_id.product_tmpl_id
        templates.check_access('read')
        for template in templates.sorted('id'):
            self.env.cr.execute('UPDATE product_template SET id=id WHERE id=%s', [template.id])
        units = self.line_ids.product_id.uom_id
        units.check_access('read')
        for unit in units.sorted('id'):
            self.env.cr.execute('UPDATE uom_uom SET id=id WHERE id=%s', [unit.id])

    def action_start(self):
        self._arg_lock()
        if self.state != 'draft':
            raise UserError(_('La referencia se toma desde borrador.'))
        self._arg_validate_scope()
        self._arg_lock_unit_definitions()
        revisions = self.line_ids.product_id._arg_lock_stock()
        for line in self.line_ids:
            quants, fingerprint = line._arg_quants()
            if len(quants) > 1 or quants.filtered('inventory_quantity_set'):
                raise UserError(_('Resuelva primero quants duplicados o un conteo nativo pendiente para este producto y ubicación.'))
            super(InventoryLine, line).write({'theoretical_quantity': sum(quants.mapped('quantity')),
                                              'baseline_revision': revisions[line.product_id.id], 'baseline_fingerprint': fingerprint,
                                              'scope_snapshot': {'name': line.product_id.display_name, 'unit': line.product_id.uom_id.display_name, 'lot': line.lot_id.name or ''}})
        super(InventoryCount, self).write({'state': 'counting', 'captured_at': fields.Datetime.now()})
        return True

    def action_mark_counted(self):
        self._arg_lock()
        if self.state != 'counting' or not self.line_ids or not all(line.counted for line in self.line_ids):
            raise UserError(_('Registre cada cantidad y marque Contado; cero explícito es distinto de una línea sin contar.'))
        for line in self.line_ids:
            qty = line.counted_quantity
            rounding = line.product_id.uom_id.rounding
            if not math.isfinite(qty) or qty < 0 or not math.isclose(qty / rounding, round(qty / rounding), rel_tol=0, abs_tol=1e-7):
                raise ValidationError(_('Revise cantidades contadas no negativas y su precisión.'))
            if line.product_id.tracking == 'serial' and qty not in (0, 1):
                raise UserError(_('Cada serie se cuenta como cero o una unidad.'))
        super(InventoryCount, self).write({'state': 'counted'})
        return True

    def action_cancel(self):
        _manager(self.env)
        self._arg_lock()
        if self.state == 'applied':
            raise UserError(_('El conteo aplicado se conserva; prepare otro conteo para corregir.'))
        super(InventoryCount, self).write({'state': 'cancel'})
        return True

    def action_apply(self):
        _manager(self.env)
        self._arg_lock()
        if self.adjustment_id:
            return self.adjustment_id._arg_action_open()
        if self.state != 'counted':
            raise UserError(_('Complete y cierre el conteo antes de aplicar diferencias.'))
        self._arg_validate_scope()
        self._arg_lock_unit_definitions()
        revisions = self.line_ids.product_id._arg_lock_stock()
        snapshots = []
        targets = []
        # Validate every baseline before any native movement; own adjustments may then advance revisions.
        for line in self.line_ids:
            quants, fingerprint = line._arg_quants()
            if revisions[line.product_id.id] != line.baseline_revision or fingerprint != line.baseline_fingerprint:
                raise UserError(_('Cambió el stock o la reserva desde la referencia. Conserve este conteo y prepare uno actualizado.'))
            snapshots.append({'product': line.product_id.display_name, 'lot': line.lot_id.name or '',
                              'unit': line.product_id.uom_id.display_name, 'theoretical': line.theoretical_quantity,
                              'counted': line.counted_quantity, 'difference': line.counted_quantity - line.theoretical_quantity})
            targets.append((line, quants))
        adjustment = self.env['arg.pyme.inventory.adjustment'].with_company(self.company_id).with_context(_arg_inventory_engine=(_INVENTORY_ENGINE, None)).create({
            'count_id': self.id, 'snapshot': snapshots, 'reason': self.reason, 'user_id': self.env.uid})
        for line, quant in targets:
            if line.product_id.uom_id.compare(line.counted_quantity, line.theoretical_quantity) == 0:
                continue
            if not quant:
                quant = self.env['stock.quant'].with_company(self.company_id).with_context(inventory_mode=True).create({
                    'product_id': line.product_id.id, 'location_id': self.location_id.id, 'lot_id': line.lot_id.id,
                    'package_id': line.package_id.id, 'owner_id': line.owner_id.id, 'inventory_quantity': line.counted_quantity})
            else:
                quant.with_context(inventory_mode=True).write({'inventory_quantity': line.counted_quantity})
            result = quant.with_context(inventory_mode=True, _arg_inventory_engine=(_INVENTORY_ENGINE, adjustment.id)).action_apply_inventory()
            if isinstance(result, dict):
                raise UserError(_('El motor nativo solicita resolver un conflicto de inventario. No se aplicó este documento.'))
        super(InventoryCount, self).write({'state': 'applied', 'adjustment_id': adjustment.id, 'applied_by': self.env.uid})
        return adjustment._arg_action_open()

    def _arg_get_completion_axes(self):
        return [self._arg_axis('Conteo', [{'label': line.product_id.display_name, 'unit': 'línea', 'rounding': 1,
                                         'target': 1, 'done': 1 if line.counted else 0} for line in self.line_ids]),
                self._arg_axis('Aplicación', [{'label': 'Documento', 'unit': 'documento', 'rounding': 1,
                                               'target': 1, 'done': 1 if self.state == 'applied' else 0,
                                               'closed': 1 if self.state == 'cancel' else 0}])]

    def _arg_document_relations(self):
        return [{'label': 'Ajuste aplicado', 'records': self.adjustment_id}]

    def _arg_report_payload(self):
        return {'title': 'Conteo de inventario ARG', 'company': self.company_id.name, 'date': str(self.date),
                'state_label': dict(self._fields['state']._description_selection(self.env)).get(self.state),
                'partner_name': self.location_id.display_name, 'partner_address': '', 'external_reference': self.arg_reference,
                'currency': '', 'lines': [{'description': (line.scope_snapshot or {}).get('name', line.product_id.display_name) + (' · ' + line.lot_id.name if line.lot_id else ''),
                                         'quantity': line.counted_quantity if line.counted else 'Sin contar', 'unit': (line.scope_snapshot or {}).get('unit') or line.product_id.uom_id.display_name,
                                         'unit_price': '', 'total': ''} for line in self.line_ids],
                'totals': [], 'notes': self.reason}


class InventoryLine(models.Model):
    _name = 'arg.pyme.inventory.count.line'
    _description = 'Detalle de conteo ARG'
    count_id = fields.Many2one('arg.pyme.inventory.count', required=True, ondelete='cascade')
    company_id = fields.Many2one(related='count_id.company_id', store=True)
    product_id = fields.Many2one('product.product', required=True, check_company=True, string='Producto')
    lot_id = fields.Many2one('stock.lot', check_company=True, string='Lote/serie')
    package_id = fields.Many2one('stock.package', check_company=True, string='Paquete')
    owner_id = fields.Many2one('res.partner', check_company=True, string='Propietario')
    theoretical_quantity = fields.Float(readonly=True, digits='Product Unit', string='Referencia')
    counted_quantity = fields.Float(digits='Product Unit', string='Cantidad contada')
    counted = fields.Boolean(string='Contado')
    baseline_revision = fields.Char(readonly=True)
    baseline_fingerprint = fields.Char(readonly=True)
    scope_snapshot = fields.Json(readonly=True, copy=False)

    def _arg_quants(self):
        self.ensure_one()
        quants = self.env['stock.quant'].search([('company_id', '=', self.company_id.id), ('location_id', '=', self.count_id.location_id.id),
                                                ('product_id', '=', self.product_id.id), ('lot_id', '=', self.lot_id.id),
                                                ('package_id', '=', self.package_id.id), ('owner_id', '=', self.owner_id.id)], order='id')
        data = {'quants': quants.read(['quantity', 'reserved_quantity', 'inventory_quantity', 'inventory_quantity_set', 'write_date']),
                'product': [self.product_id.id, self.product_id.uom_id.id, self.product_id.uom_id.rounding, self.product_id.tracking, self.product_id.is_storable]}
        return quants, hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if any(values.get(k) or self.env.context.get('default_' + k) for k in ('theoretical_quantity', 'baseline_revision', 'baseline_fingerprint', 'scope_snapshot')):
                raise AccessError(_('La referencia del stock se captura automáticamente.'))
            count = self.env['arg.pyme.inventory.count'].browse(values['count_id'])
            count._arg_lock()
            if count.state != 'draft':
                raise UserError(_('Defina el alcance del conteo antes de tomar referencia.'))
        return super().create(vals_list)

    def write(self, values):
        if {'count_id', 'company_id', 'theoretical_quantity', 'baseline_revision', 'baseline_fingerprint', 'scope_snapshot'} & values.keys():
            raise AccessError(_('La referencia y el origen de conteo se conservan.'))
        for count in self.count_id.sorted('id'):
            count._arg_lock()
            if count.state not in ('draft', 'counting') or (count.state != 'draft' and {'product_id', 'lot_id', 'package_id', 'owner_id'} & values.keys()):
                raise UserError(_('Conserve el alcance del conteo iniciado y los valores del conteo cerrado.'))
        return super().write(values)

    def unlink(self):
        for count in self.count_id:
            count._arg_lock()
            if count.state != 'draft':
                raise UserError(_('Conserve el alcance del conteo iniciado.'))
        return super().unlink()


class InventoryAdjustment(models.Model):
    _name = 'arg.pyme.inventory.adjustment'
    _inherit = ['arg.pyme.document.mixin']
    _description = 'Ajuste de inventario ARG'
    _rec_name = 'arg_number'
    count_id = fields.Many2one('arg.pyme.inventory.count', required=True, ondelete='restrict', check_company=True)
    company_id = fields.Many2one(related='count_id.company_id', store=True)
    snapshot = fields.Json(required=True, readonly=True)
    reason = fields.Char(required=True, readonly=True)
    user_id = fields.Many2one('res.users', required=True, readonly=True)
    move_ids = fields.One2many('stock.move', 'arg_inventory_adjustment_id', readonly=True)
    _count_unique = models.Constraint('UNIQUE(count_id)', 'El conteo ya tiene un ajuste aplicado.')

    def _arg_document_code(self):
        return 'AJU'

    @api.model_create_multi
    def create(self, vals_list):
        context = self.env.context.get('_arg_inventory_engine')
        if not isinstance(context, tuple) or context[0] is not _INVENTORY_ENGINE:
            raise AccessError(_('El ajuste se crea únicamente al aplicar un conteo autorizado.'))
        return super().create(vals_list)

    def write(self, values):
        raise AccessError(_('El ajuste aplicado se conserva. Prepare una corrección vinculada.'))

    def _arg_action_open(self):
        self._arg_check_document_access()
        return {'type': 'ir.actions.act_window', 'res_model': self._name, 'res_id': self.id, 'view_mode': 'form',
                'views': [(self.env.ref('arg_pyme_stock.inventory_adjustment_form').id, 'form')]}

    def _arg_document_relations(self):
        return [{'label': 'Conteo origen', 'records': self.count_id}, {'label': 'Movimientos nativos', 'records': self.move_ids}]

    def _arg_report_payload(self):
        return {'title': 'Ajuste de inventario ARG', 'company': self.company_id.name, 'date': str(self.create_date),
                'state_label': 'Aplicado', 'partner_name': self.count_id.location_id.display_name, 'partner_address': '',
                'external_reference': self.count_id.arg_number, 'currency': '',
                'lines': [{'description': row['product'] + (' · ' + row['lot'] if row['lot'] else ''), 'quantity': row['difference'],
                           'unit': row['unit'], 'unit_price': '', 'total': ''} for row in self.snapshot],
                'totals': [], 'notes': self.reason + ' · ' + self.user_id.display_name}
