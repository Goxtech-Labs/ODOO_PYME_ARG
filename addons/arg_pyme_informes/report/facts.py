from odoo.addons.arg_pyme_base.tools.quantity import quantity_rounding
import math
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

# No optional model is inherited or declared as a dependency/comodel.
SOURCES = {
 'sales': ('Facturación de ventas neta', 'account.move.line', 'Línea de FAC/NCV publicada', 'Fecha contable', True),
 'purchases': ('Facturación de compras neta', 'account.move.line', 'Línea de FRC/NCP publicada', 'Fecha contable', True),
 'sale_orders': ('Pedidos de clientes confirmados', 'sale.order.line', 'Línea de pedido confirmado', 'Fecha del pedido', True),
 'purchase_orders': ('Pedidos al proveedor confirmados', 'purchase.order.line', 'Línea de pedido confirmado', 'Fecha de aprobación', True),
 'cash': ('Caja y banco publicados', 'account.move.line', 'Apunte de liquidez', 'Fecha contable', True),
 'customer_debt': ('Deuda actual de clientes por vencimiento', 'account.move.line', 'Apunte/cuota, residual actual', 'Vencimiento; fecha contable si falta', True),
 'supplier_debt': ('Deuda actual a proveedores por vencimiento', 'account.move.line', 'Apunte/cuota, residual actual', 'Vencimiento; fecha contable si falta', True),
 'applications': ('Aplicaciones contables vigentes', 'account.partial.reconcile', 'Conciliación parcial vigente, una vez', 'Fecha efectiva max_date', True),
 'movements': ('Movimientos físicos terminados', 'stock.move.line', 'Línea física por lote/ubicaciones', 'Fecha efectiva', False),
 'stock_now': ('Existencias actuales', 'stock.quant', 'Quant: producto/ubicación/lote/propietario/paquete', 'Ahora; sin filtro por período', False),
 'stock_at': ('Existencias a una fecha', 'stock.move.line', 'Movimiento terminado por extremo interno', 'Hasta fin del día de corte', False),
}
MAX_ROWS = 5000


class ReportEngine(models.AbstractModel):
    _name = 'arg.pyme.report.engine'
    _description = 'Consultas por hechos y dimensiones ARG'

    @api.model
    def _authorize(self):
        if self.env.user.share or not (self.env.user.has_group('arg_pyme_base.group_informes') or self.env.user.has_group('arg_pyme_base.group_admin')):
            raise AccessError(_('Se requiere Consulta Informes ARG.'))

    @api.model
    def _available(self):
        self._authorize()
        return [(key, meta[0]) for key, meta in SOURCES.items() if meta[1] in self.env and self.env[meta[1]].has_access('read')]

    def _read(self, record, names):
        if not record:
            return {}
        record.ensure_one()
        return record.read(names)[0]  # Enforce field access as well as ACL/record rules.

    def _label(self, record):
        return self._read(record, ['display_name']).get('display_name') or ''

    def _origin(self, record):
        if not record:
            return {'name':'', 'url':''}
        names = ['display_name'] + (['arg_number'] if 'arg_number' in record._fields else [])
        data = self._read(record, names)
        return {'name':data.get('arg_number') or data['display_name'], 'url':'/odoo/%s/%s' % (record._name, record.id)}

    def _progress(self, record, cache):
        key = (record._name, record.id)
        if key not in cache:
            if not hasattr(record, '_arg_get_completion_axes'):
                cache[key] = ''
            else:
                try:
                    record._arg_check_document_access()
                    axes = record._arg_get_completion_axes()
                    labels = {'pending':_('Pendiente'), 'partial':_('Parcial'), 'complete':_('Completo'), 'unknown':_('No determinado'), 'na':_('No corresponde')}
                    cache[key] = ' · '.join(str(axis.get('label', axis.get('name', ''))) + ': ' + labels.get(axis.get('state'), str(axis.get('state', ''))) + (' · '+_('Cerrado con faltante') if axis.get('closed_shortfall') else '') for axis in axes)
                except AccessError:
                    cache[key] = _('No determinado: sin acceso a los ejes del documento')
        return cache[key]

    def _base_row(self, doc, date, partner=None, product=None, unit=None, location=None, original=None, state='', progress=''):
        source = self._origin(doc)
        return {'day':str(date or ''), 'document':source['name'], 'source_url':source['url'],
                'original':self._origin(original)['name'] if original else '',
                'original_url':self._origin(original)['url'] if original else '',
                'partner':self._label(partner), 'product':self._label(product), 'unit':self._label(unit),
                'unit_id':unit.id if unit else False, 'unit_rounding':quantity_rounding(self.env) if unit else None, 'location':self._label(location), 'state':state,
                'progress':progress, 'description':'', 'quantity':None, 'reserved':None, 'available':None, 'flow':'',
                'document_key':(doc._name,doc.id), 'partner_key':partner.id if partner else False,
                'product_key':product.id if product else False, 'location_key':location.id if location else False,
                'net':None, 'tax':None, 'total':None}

    def _timezone(self, wizard):
        value = wizard.env.context.get('tz') or wizard.env.user.tz or 'UTC'
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError, TypeError):
            raise ValidationError(_('Zona horaria no válida. Revise las preferencias.'))
        return value

    def _utc_bounds(self, wizard):
        zone = ZoneInfo(self._timezone(wizard))
        def utc(day):
            return datetime.combine(day, time.min, tzinfo=zone).astimezone(ZoneInfo('UTC')).replace(tzinfo=None)
        return utc(wizard.date_from), utc(wizard.date_to + timedelta(days=1))

    def _domain(self, wizard):
        source = wizard.source
        domain = [('company_id', '=', wizard.company_id.id)]
        date_field = 'date'
        datetime_date = False
        partner_field = 'partner_id'
        product_field = 'product_id'
        if source in ('sales', 'purchases'):
            types = ['out_invoice','out_refund'] if source == 'sales' else ['in_invoice','in_refund']
            domain += [('parent_state','=','posted'), ('move_id.move_type','in',types), ('display_type','=','product')]
        elif source in ('sale_orders','purchase_orders'):
            domain += [('order_id.state','in',['sale'] if source == 'sale_orders' else ['purchase','done']), ('display_type','=',False)]
            date_field = 'order_id.date_order' if source == 'sale_orders' else 'order_id.date_approve'
            partner_field = 'order_id.partner_id'
            datetime_date = True
        elif source == 'cash':
            domain += [('parent_state','=','posted'), ('account_type','=','asset_cash')]
        elif source in ('customer_debt','supplier_debt'):
            domain += [('parent_state','=','posted'), ('account_type','=', 'asset_receivable' if source == 'customer_debt' else 'liability_payable')]
            domain += ['|', '&', ('date_maturity','>=',wizard.date_from), ('date_maturity','<=',wizard.date_to),
                       '&', ('date_maturity','=',False), '&', ('date','>=',wizard.date_from), ('date','<=',wizard.date_to)]
            date_field = False
        elif source == 'applications':
            if wizard.currency_id != wizard.company_id.currency_id:
                raise ValidationError(_('Aplicaciones se expresa en moneda de compañía; elija esa moneda.'))
            date_field = 'max_date'
            product_field = False
            partner_field = 'debit_move_id.partner_id'
            if wizard.partner_id:
                domain += ['|', ('debit_move_id.partner_id','=',wizard.partner_id.id), ('credit_move_id.partner_id','=',wizard.partner_id.id)]
                partner_field = False
        elif source == 'stock_now':
            domain += [('location_id.usage','=','internal')]
            date_field = False
            partner_field = 'owner_id'
        elif source in ('movements','stock_at'):
            domain += [('state','=','done')]
            partner_field = 'picking_partner_id'
            datetime_date = True
            if source == 'stock_at':
                # Opening stock is reconstructed from all completed history, not from current quants.
                domain += [('product_id.is_storable','=',True), '|', '&', ('location_id.usage','=','internal'), ('location_id.company_id','=',wizard.company_id.id), '&', ('location_dest_id.usage','=','internal'), ('location_dest_id.company_id','=',wizard.company_id.id)]
            if wizard.location_query:
                domain += ['|', ('location_id.complete_name','ilike',wizard.location_query), ('location_dest_id.complete_name','ilike',wizard.location_query)]
        if date_field:
            start, stop = self._utc_bounds(wizard) if datetime_date else (wizard.date_from, wizard.date_to)
            if source != 'stock_at':
                domain.append((date_field, '>=', start))
            domain.append((date_field, '<' if datetime_date else '<=', stop))
        if SOURCES[source][4] and source != 'applications':
            domain.append(('currency_id','=',wizard.currency_id.id))
        if wizard.partner_id and partner_field:
            domain.append((partner_field,'=',wizard.partner_id.id))
        if wizard.product_query:
            if not product_field:
                raise ValidationError(_('Este hecho no tiene dimensión producto; quite ese filtro.'))
            domain.append((product_field+'.display_name','ilike',wizard.product_query))
        if wizard.location_query and source == 'stock_now':
            domain.append(('location_id.complete_name','ilike',wizard.location_query))
        elif wizard.location_query and source not in ('movements','stock_at'):
            raise ValidationError(_('El filtro ubicación sólo se aplica a existencias y movimientos.'))
        if source == 'stock_at' and wizard.partner_id:
            raise ValidationError(_('Stock histórico reconstruye ubicaciones completas: quite el filtro tercero.'))
        return domain

    def _collect(self, wizard):
        source = wizard.source
        model = self.env[SOURCES[source][1]].with_company(wizard.company_id).with_context(allowed_company_ids=wizard.company_id.ids)
        domain = self._domain(wizard)
        records = model.search(domain, order='id', limit=MAX_ROWS+1)
        if len(records) > MAX_ROWS:
            raise UserError(_('El corte supera 5000 registros fuente. Reduzca el período o agregue filtros; no se exporta un resultado truncado.'))
        rows = []
        cache = {}
        matched_locations = None
        if source == 'stock_at' and wizard.location_query:
            locations = records.location_id | records.location_dest_id
            matched_locations = set(self.env['stock.location'].search([('id','in',locations.ids), ('complete_name','ilike',wizard.location_query)]).ids)
        for rec in records:
            if source in ('sales','purchases'):
                self._read(rec,['move_id','date','partner_id','product_id','product_uom_id','quantity','price_subtotal','price_total','name'])
                doc = rec.move_id
                self._read(doc,['move_type','state','reversed_entry_id'])
                sign = -1 if doc.move_type in ('out_refund','in_refund') else 1
                row = self._base_row(doc, rec.date, rec.partner_id, rec.product_id, rec.product_uom_id,
                    original=doc.reversed_entry_id, state=doc.state, progress=self._progress(doc,cache))
                row.update(quantity=sign*rec.quantity if rec.product_uom_id else None, net=sign*rec.price_subtotal,
                           tax=sign*(rec.price_total-rec.price_subtotal), total=sign*rec.price_total, description=rec.name)
            elif source in ('sale_orders','purchase_orders'):
                purchase = source == 'purchase_orders'
                unit_field = 'uom_id' if purchase else 'product_uom_id'
                qty_field = 'product_qty' if purchase else 'product_uom_qty'
                self._read(rec,['order_id','product_id',unit_field,qty_field,'price_subtotal','price_total','name'])
                doc = rec.order_id
                date_field = 'date_approve' if purchase else 'date_order'
                self._read(doc,[date_field,'partner_id','state'])
                date = fields.Datetime.context_timestamp(wizard.with_context(tz=self._timezone(wizard)), doc[date_field]).date() if doc[date_field] else False
                row = self._base_row(doc,date,doc.partner_id,rec.product_id,rec[unit_field],state=doc.state,progress=self._progress(doc,cache))
                row.update(quantity=rec[qty_field] if rec[unit_field] else None, net=rec.price_subtotal, tax=rec.price_total-rec.price_subtotal,
                           total=rec.price_total, description=rec.name)
            elif source in ('cash','customer_debt','supplier_debt'):
                names = ['move_id','date','partner_id','amount_currency','name']
                if source != 'cash': names += ['date_maturity','amount_residual_currency']
                self._read(rec,names)
                sign = -1 if source == 'supplier_debt' else 1
                amount = rec.amount_currency if source == 'cash' else sign*rec.amount_residual_currency
                if source != 'cash' and wizard.currency_id.is_zero(amount):
                    continue
                date = rec.date if source == 'cash' else rec.date_maturity or rec.date
                row = self._base_row(rec.move_id,date,rec.partner_id,state='posted',progress=self._progress(rec.move_id,cache))
                row.update(total=amount,description=rec.name)
            elif source == 'applications':
                self._read(rec,['debit_move_id','credit_move_id','amount','max_date'])
                debit, credit = rec.debit_move_id, rec.credit_move_id
                self._read(debit,['move_id','partner_id','parent_state']); self._read(credit,['move_id','partner_id','parent_state'])
                if debit.parent_state != 'posted' or credit.parent_state != 'posted':
                    continue
                row = self._base_row(debit.move_id,rec.max_date,debit.partner_id,original=credit.move_id,state='Vigente')
                row.update(total=rec.amount,description=_('Conciliación #%s · no acredita dinero por sí sola') % rec.id)
            elif source == 'stock_now':
                self._read(rec,['product_id','location_id','lot_id','owner_id','package_id','quantity','reserved_quantity'])
                self._read(rec.product_id,['uom_id'])
                row = self._base_row(rec,False,rec.owner_id,rec.product_id,rec.product_id.uom_id,rec.location_id,state='Actual')
                row.update(quantity=rec.quantity,reserved=rec.reserved_quantity,available=rec.quantity-rec.reserved_quantity,flow=_('Existencia actual'),
                    description=' · '.join(filter(None,[self._label(rec.lot_id),self._label(rec.package_id)])))
            else:
                self._read(rec,['move_id','date','picking_partner_id','product_id','uom_id','quantity','quantity_product_uom','location_id','location_dest_id','lot_id'])
                self._read(rec.product_id,['uom_id'])
                self._read(rec.move_id,['picking_id','origin_returned_move_id'])
                self._read(rec.location_id,['usage','complete_name','company_id']); self._read(rec.location_dest_id,['usage','complete_name','company_id'])
                original = rec.move_id.origin_returned_move_id
                if original: self._read(original,['picking_id'])
                doc = rec.move_id.picking_id or rec.move_id
                original = (original.picking_id or original) if original else None
                date = fields.Datetime.context_timestamp(wizard.with_context(tz=self._timezone(wizard)),rec.date).date()
                if source == 'stock_at':
                    # Two endpoints for internal transfer: no fabricated external inflow/outflow.
                    for location, sign in [(rec.location_id,-1),(rec.location_dest_id,1)]:
                        if location.usage != 'internal' or location.company_id != wizard.company_id or (matched_locations is not None and location.id not in matched_locations):
                            continue
                        row = self._base_row(doc,date,product=rec.product_id,unit=rec.product_id.uom_id,location=location,original=original,state='done')
                        row.update(quantity=sign*rec.quantity_product_uom,description=self._label(rec.lot_id),flow=_('Existencia reconstruida')); rows.append(row)
                    continue
                # Delivery +; customer return -. Receipt +; supplier return -. Other moves keep explicit from/to.
                if rec.location_dest_id.usage == 'customer': sign, flow = 1, _('Entregas a clientes netas')
                elif rec.location_id.usage == 'customer': sign, flow = -1, _('Entregas a clientes netas')
                elif rec.location_id.usage == 'supplier': sign, flow = 1, _('Recepciones de proveedores netas')
                elif rec.location_dest_id.usage == 'supplier': sign, flow = -1, _('Recepciones de proveedores netas')
                elif rec.location_id.usage == rec.location_dest_id.usage == 'internal': sign, flow = 1, _('Transferencias internas')
                else: sign, flow = 1, _('Otros movimientos físicos')
                row = self._base_row(doc,date,rec.picking_partner_id,rec.product_id,rec.product_id.uom_id,rec.location_id,original=original,state='done')
                row.update(quantity=sign*rec.quantity_product_uom,flow=flow,description=self._label(rec.location_id)+' → '+self._label(rec.location_dest_id)+' · '+self._label(rec.lot_id))
            rows.append(row)
        for row in rows:
            for key in ['quantity','reserved','available','net','tax','total']:
                if row[key] is not None and not math.isfinite(row[key]):
                    raise ValidationError(_('La fuente contiene un importe o cantidad no finita; revise el origen.'))
        return rows
