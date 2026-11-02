import hashlib
import json
import math
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.float_utils import float_compare


_PURCHASE_LIFECYCLE = object()
_BILL_GENERATION = object()


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'arg.pyme.document.mixin']

    arg_purchase_snapshot = fields.Json(readonly=True, copy=False, groups='base.group_user')
    arg_allow_zero_price = fields.Boolean(string='Aceptar precios cero expresamente')
    arg_bill_operation_ids = fields.One2many('arg.pyme.purchase.bill.operation', 'order_id', readonly=True)

    def _arg_document_code(self):
        return 'PPC'

    def _arg_require_manager(self):
        if not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Confirmar o revertir compras requiere responsable ARG.'))

    def _arg_lock(self):
        self.check_access('write')
        for order in self.sorted('id'):
            order._arg_check_document_access()
            order.flush_recordset(['write_date', 'write_uid'])
            self.env.cr.execute('UPDATE purchase_order SET write_date=clock_timestamp(),write_uid=%s WHERE id=%s',
                                [self.env.uid, order.id])
            order.invalidate_recordset(['write_date', 'write_uid'])

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        for raw in vals_list:
            values = dict(raw)
            values.setdefault('state', 'draft')
            if (values.get('arg_purchase_snapshot') or values.get('arg_bill_operation_ids')
                    or self.env.context.get('default_arg_purchase_snapshot') or self.env.context.get('default_arg_bill_operation_ids')):
                raise AccessError(_('La evidencia de compras se administra desde sus acciones.'))
            if values.get('state', 'draft') not in ('draft', 'sent'):
                raise AccessError(_('El pedido se crea en borrador.'))
            company = self.env['res.company'].browse(values.get('company_id') or self.env.company.id)
            if company not in self.env.companies:
                raise AccessError(_('Compañía no habilitada.'))
            if values.get('partner_id'):
                known = self.env['res.partner'].browse(values['partner_id']).with_company(company)._arg_document_defaults('purchase')
                values.setdefault('currency_id', known['currency_id'])
                values.setdefault('payment_term_id', known['payment_term_id'])
                if known['conditions_note']:
                    values.setdefault('note', known['conditions_note'])
            prepared.append(values)
        return super().create(prepared)

    def write(self, values):
        if {'arg_purchase_snapshot', 'arg_bill_operation_ids'} & values.keys():
            raise AccessError(_('La evidencia acordada no se modifica manualmente.'))
        if {'state', 'locked'} & values.keys() and self.env.context.get('_arg_purchase_lifecycle') is not _PURCHASE_LIFECYCLE:
            raise AccessError(_('Use las acciones de confirmar, aprobar, cancelar o desbloquear el pedido.'))
        commercial = {'partner_id', 'currency_id', 'company_id', 'date_order', 'payment_term_id',
                      'fiscal_position_id', 'document_tax_mode', 'note', 'arg_allow_zero_price'}
        if commercial & values.keys():
            self._arg_lock()
            if any(order.state not in ('draft', 'sent') for order in self):
                raise UserError(_('Las condiciones confirmadas se conservan. Cancele y vuelva a borrador si corresponde.'))
        return super().write(values)

    def _arg_tax_definition(self):
        taxes = self.order_line.tax_ids
        taxes |= taxes.flatten_taxes_hierarchy()
        names = ['name', 'amount', 'amount_type', 'price_include', 'sequence', 'include_base_amount',
                 'is_base_affected', 'children_tax_ids', 'company_id', 'tax_exigibility', 'write_date']
        rows = taxes.with_context(lang='en_US').sorted('id').read([n for n in names if n in taxes._fields])
        repartitions = taxes.invoice_repartition_line_ids | taxes.refund_repartition_line_ids
        details = repartitions.sorted('id').read(['factor_percent', 'repartition_type', 'account_id', 'tag_ids', 'write_date'])
        return json.loads(json.dumps({'taxes': rows, 'repartitions': details}, default=str))

    def _arg_validate_terms(self):
        for order in self:
            if not order.partner_id or not order.currency_id or not order.order_line.filtered(lambda line: not line.display_type):
                raise UserError(_('Complete proveedor, moneda y al menos un producto.'))
            order.company_id.currency_id._arg_require_conversion(order.currency_id, order.company_id,
                                                                fields.Date.to_date(order.date_order))
            for line in order.order_line.filtered(lambda item: not item.display_type):
                if not line.product_id or line.product_id.type not in ('consu', 'service') or line.uom_id != line.product_id.uom_id:
                    raise UserError(_('Complete productos o servicios con su unidad base.'))
                if not all(math.isfinite(v) for v in (line.product_qty, line.price_unit, line.discount)):
                    raise ValidationError(_('Revise cantidades, precios y descuentos finitos.'))
                if (float_compare(line.product_qty, 0, precision_rounding=line.uom_id.rounding) <= 0
                        or not math.isclose(line.product_qty / line.uom_id.rounding, round(line.product_qty / line.uom_id.rounding), rel_tol=0, abs_tol=1e-7)
                        or line.price_unit < 0 or not 0 <= line.discount <= 100):
                    raise ValidationError(_('Revise cantidades positivas, precios no negativos y descuento entre cero y cien.'))
                if not line.price_unit and not order.arg_allow_zero_price:
                    raise UserError(_('Acepte expresamente los precios cero o corrija el detalle.'))
                if any(tax.company_id != order.company_id for tax in line.tax_ids):
                    raise UserError(_('Los impuestos deben corresponder a la compañía del pedido.'))

    def _arg_freeze(self):
        for order in self:
            if order.arg_purchase_snapshot:
                if order.arg_purchase_snapshot['tax_definition'] != order._arg_tax_definition():
                    raise UserError(_('Cambió una definición impositiva acordada. Revise el pedido antes de continuar.'))
                continue
            partner = order.partner_id.with_context(lang='es_AR')
            snapshot = {
                'company': {'id': order.company_id.id, 'name': order.company_id.name},
                'partner': {'id': partner.id, 'name': partner.name or '', 'vat': partner.vat or '',
                            'address': partner.contact_address or ''},
                'date': str(order.date_order), 'currency_id': order.currency_id.id, 'currency': order.currency_id.name,
                'rate': self.env['res.currency']._get_conversion_rate(order.company_id.currency_id, order.currency_id,
                                                                   order.company_id, fields.Date.to_date(order.date_order)),
                'rate_evidence': order.company_id.currency_id._arg_require_conversion(order.currency_id, order.company_id,
                                                                                     fields.Date.to_date(order.date_order)),
                'payment_term': order.payment_term_id.display_name or '', 'notes': str(order.note or ''),
                'totals': {'untaxed': order.amount_untaxed, 'tax': order.amount_tax, 'total': order.amount_total},
                'tax_definition': order._arg_tax_definition(),
                'lines': {str(line.id): {'name': line.name, 'product_id': line.product_id.id, 'quantity': line.product_qty,
                                        'unit': line.uom_id.display_name, 'price': line.price_unit, 'discount': line.discount,
                                        'tax_ids': line.tax_ids.ids, 'total': line.price_total}
                          for line in order.order_line if not line.display_type},
            }
            super(PurchaseOrder, order).write({'arg_purchase_snapshot': snapshot})

    def button_confirm(self):
        self._arg_require_manager()
        self._arg_lock()
        self._arg_validate_terms()
        self._arg_freeze()
        return super(PurchaseOrder, self.with_context(_arg_purchase_lifecycle=_PURCHASE_LIFECYCLE)).button_confirm()

    def button_approve(self, force=False):
        self._arg_require_manager()
        self._arg_lock()
        if any(order.state not in ('draft', 'sent', 'to approve') for order in self):
            raise UserError(_('Sólo se aprueba un pedido borrador o pendiente de aprobación.'))
        self._arg_validate_terms()
        self._arg_freeze()
        return super(PurchaseOrder, self.with_context(_arg_purchase_lifecycle=_PURCHASE_LIFECYCLE)).button_approve(force=force)

    def button_cancel(self):
        self._arg_require_manager()
        self._arg_lock()
        return super(PurchaseOrder, self.with_context(_arg_purchase_lifecycle=_PURCHASE_LIFECYCLE)).button_cancel()

    def button_draft(self):
        self._arg_require_manager()
        self._arg_lock()
        if any(order.state not in ('cancel', 'to approve') or order.invoice_ids.filtered(lambda move: move.state != 'cancel') for order in self):
            raise UserError(_('Sólo se vuelve a borrador desde cancelado o por aprobar y sin facturas activas.'))
        result = super(PurchaseOrder, self.with_context(_arg_purchase_lifecycle=_PURCHASE_LIFECYCLE)).button_draft()
        super(PurchaseOrder, self).write({'arg_purchase_snapshot': False})
        return result

    def button_lock(self):
        self._arg_require_manager()
        return super(PurchaseOrder, self.with_context(_arg_purchase_lifecycle=_PURCHASE_LIFECYCLE)).button_lock()

    def button_unlock(self):
        self._arg_require_manager()
        return super(PurchaseOrder, self.with_context(_arg_purchase_lifecycle=_PURCHASE_LIFECYCLE)).button_unlock()

    def _mark_rfqs_as_sent(self):
        return super(PurchaseOrder, self.with_context(_arg_purchase_lifecycle=_PURCHASE_LIFECYCLE))._mark_rfqs_as_sent()

    def action_arg_prepare_bill(self):
        self._arg_check_document_access()
        self.check_access('write')
        wizard = self.env['arg.pyme.purchase.bill.wizard'].create({'order_id': self.id})
        return {'type': 'ir.actions.act_window', 'res_model': wizard._name, 'res_id': wizard.id,
                'view_mode': 'form', 'target': 'new', 'views': [(self.env.ref('arg_pyme_compras.purchase_bill_form').id, 'form')]}

    def action_create_invoice(self, attachment_ids=False):
        if self.env.context.get('_arg_purchase_bill') is not _BILL_GENERATION:
            if attachment_ids:
                raise UserError(_('Registre el archivo desde la factura recibida; prepare el documento desde el pedido.'))
            return self.action_arg_prepare_bill()
        return super().action_create_invoice(attachment_ids=attachment_ids)

    def _arg_prepare_bill(self, key, quantities):
        self.ensure_one()
        self._arg_lock()
        if not isinstance(key, str) or not 16 <= len(key) <= 80 or not isinstance(quantities, list) or not quantities or len(quantities) > 500:
            raise ValidationError(_('Revise la operación y las cantidades seleccionadas.'))
        selected = []
        seen = set()
        for raw in quantities:
            if not isinstance(raw, dict):
                raise ValidationError(_('Detalle de factura no válido.'))
            line_id, qty = raw.get('line_id'), raw.get('quantity')
            if type(line_id) is not int or type(qty) not in (int, float) or not math.isfinite(qty) or qty < 0 or line_id in seen:
                raise ValidationError(_('Detalle de factura no válido.'))
            seen.add(line_id)
            line = self.order_line.filtered(lambda item: item.id == line_id and not item.display_type)
            if not line:
                raise AccessError(_('La línea debe pertenecer al pedido.'))
            if qty:
                if not math.isclose(qty / line.uom_id.rounding, round(qty / line.uom_id.rounding), rel_tol=0, abs_tol=1e-7):
                    raise ValidationError(_('La cantidad no respeta la precisión de la unidad.'))
                selected.append((line, float(qty)))
        if not selected:
            raise UserError(_('Seleccione al menos una cantidad positiva.'))
        signature = _digest([(line.id, qty) for line, qty in sorted(selected, key=lambda pair: pair[0].id)])
        events = self.env['arg.pyme.purchase.bill.operation']
        prior = events.search([('order_id', '=', self.id), ('operation_key', '=', key)], limit=1)
        if prior:
            if prior.payload_hash != signature:
                raise ValidationError(_('La clave ya corresponde a otras cantidades.'))
            prior.move_id.check_access('read')
            return prior.move_id
        if self.state != 'purchase':
            raise UserError(_('Confirme o apruebe primero el pedido.'))
        self._arg_freeze()
        drafts = self.invoice_ids.filtered(lambda move: move.state == 'draft')
        if drafts:
            raise UserError(_('Ya hay una factura borrador vinculada. Resuélvala antes de preparar otra.'))
        values = self.with_context(default_move_type='in_invoice')._prepare_invoice()
        values.update(move_type='in_invoice', state='draft')
        values['invoice_line_ids'] = []
        for line, qty in selected:
            if float_compare(qty, line.qty_to_invoice, precision_rounding=line.uom_id.rounding) > 0:
                raise UserError(_('La cantidad supera el pendiente facturable según la política del producto.'))
            row = line._prepare_account_move_line()
            row['quantity'] = qty
            values['invoice_line_ids'].append((0, 0, row))
        values['arg_purchase_header_snapshot'] = self.arg_purchase_snapshot
        move = self.env['account.move'].with_company(self.company_id).with_context(_arg_purchase_bill=_BILL_GENERATION).create(values)
        events.sudo().create({'order_id': self.id, 'move_id': move.id, 'operation_key': key,
                             'payload_hash': signature, 'user_id': self.env.uid})
        return move.with_context(_arg_purchase_bill=None)

    @api.depends('write_date', 'state', 'order_line.product_qty', 'order_line.invoice_lines.quantity',
                 'order_line.invoice_lines.move_id.state', 'invoice_ids.amount_residual', 'invoice_ids.amount_total')
    def _compute_arg_completion_axes(self):
        super()._compute_arg_completion_axes()

    def _arg_get_completion_axes(self):
        rows = []
        for line in self.order_line.filtered(lambda item: not item.display_type):
            posted = line.invoice_lines.filtered(lambda item: item.move_id.state == 'posted')
            quantity = sum(item.product_uom_id._compute_quantity(item.quantity, line.uom_id)
                           * (1 if item.move_id.move_type == 'in_invoice' else -1) for item in posted)
            rows.append({'label': line.name, 'unit': line.uom_id.display_name, 'rounding': line.uom_id.rounding,
                         'target': line.product_qty, 'done': quantity,
                         'closed': max(0, line.product_qty - quantity) if self.state == 'cancel' else 0})
        result = [self._arg_axis('Facturación recibida publicada', rows)]
        bills = self.invoice_ids.filtered(lambda move: move.state == 'posted' and move.move_type == 'in_invoice')
        scope_reason = self._arg_invoice_scope_reason(bills, 'purchase_line_id')
        if scope_reason:
            result.append(self._arg_unknown_axis('Cancelación de deuda facturada', scope_reason))
        for currency in bills.currency_id if not scope_reason else self.env['res.currency']:
            subset = bills.filtered(lambda move: move.currency_id == currency)
            result.append(self._arg_axis('Cancelación de deuda facturada · ' + currency.name, [
                {'label': bill.arg_number or bill.name, 'unit': currency.name, 'rounding': currency.rounding,
                 'target': abs(bill.amount_total), 'done': max(0, abs(bill.amount_total) - abs(bill.amount_residual))} for bill in subset]))
        if getattr(self.env['account.move'], '_arg_money_axis', None):
            result.append(self._arg_unknown_axis('Dinero pagado sobre lo facturado', scope_reason) if scope_reason else bills._arg_money_axis('Dinero pagado sobre lo facturado'))
        return super()._arg_get_completion_axes() + result

    def _arg_document_relations(self):
        return super()._arg_document_relations() + [{'label': 'Facturas y notas recibidas', 'records': self.invoice_ids}]

    def _arg_document_line_relations(self):
        result = super()._arg_document_line_relations()
        for line in self.order_line:
            for invoice_line in line.invoice_lines:
                result.append({'source_document': self, 'source_line': line, 'target_document': invoice_line.move_id,
                               'target_line': invoice_line, 'quantity': invoice_line.quantity,
                               'unit': invoice_line.product_uom_id.display_name})
        return result

    def _arg_report_payload(self):
        snap = self.arg_purchase_snapshot or {}
        partner = snap.get('partner') or {'name': self.partner_id.name or '', 'address': self.partner_id.contact_address or ''}
        rows = ([{'description': line['name'], 'quantity': line['quantity'], 'unit': line['unit'],
                  'unit_price': line['price'], 'total': line['total']} for line in snap['lines'].values()]
                if snap else [{'description': line.name, 'quantity': line.product_qty, 'unit': line.uom_id.display_name,
                               'unit_price': line.price_unit, 'total': line.price_total} for line in self.order_line if not line.display_type])
        totals = snap.get('totals') or {'untaxed': self.amount_untaxed, 'tax': self.amount_tax, 'total': self.amount_total}
        return {'title': 'Pedido al proveedor ARG', 'company': snap.get('company', {}).get('name') or self.company_id.name,
                'date': snap.get('date') or str(self.date_order), 'state_label': dict(self._fields['state']._description_selection(self.env)).get(self.state),
                'partner_name': partner['name'], 'partner_address': partner['address'], 'external_reference': self.partner_ref or self.arg_reference,
                'currency': snap.get('currency') or self.currency_id.name,
                'lines': rows, 'totals': [{'label': 'Neto', 'amount': totals['untaxed']}, {'label': 'Impuestos', 'amount': totals['tax']},
                                        {'label': 'Total', 'amount': totals['total']}], 'notes': snap.get('notes') or str(self.note or '')}


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        orders = self.env['purchase.order'].browse(list({v['order_id'] for v in vals_list}))
        orders._arg_lock()
        if any(order.state not in ('draft', 'sent') for order in orders):
            raise UserError(_('No agregue líneas a un pedido confirmado.'))
        return super().create(vals_list)

    def write(self, values):
        if 'order_id' in values:
            raise AccessError(_('La línea conserva su pedido de origen.'))
        if {'product_id', 'product_qty', 'uom_id', 'price_unit', 'discount', 'tax_ids', 'name'} & values.keys():
            self.order_id._arg_lock()
            if any(line.order_id.state not in ('draft', 'sent') for line in self):
                raise UserError(_('Las líneas confirmadas conservan sus condiciones.'))
        return super().write(values)

    def unlink(self):
        self.order_id._arg_lock()
        if any(line.order_id.state not in ('draft', 'sent') for line in self):
            raise UserError(_('Conserve las líneas confirmadas y sus vínculos.'))
        return super().unlink()

    @api.depends('product_qty', 'uom_id', 'company_id', 'order_id.partner_id', 'order_id.currency_id', 'order_id.date_order')
    def _compute_price_unit_and_date_planned_and_name(self):
        for company in self.company_id:
            lines = self.filtered(lambda line: line.company_id == company).with_company(company)
            lines._arg_require_supplier_rates()
            super(PurchaseOrderLine, lines)._compute_price_unit_and_date_planned_and_name()
        without_company = self.filtered(lambda line: not line.company_id)
        if without_company:
            super(PurchaseOrderLine, without_company)._compute_price_unit_and_date_planned_and_name()

    def _arg_require_supplier_rates(self):
        for line in self:
            if not line.product_id or line.invoice_lines or not line.company_id or self.env.context.get('skip_uom_conversion') or line.technical_price_unit != line.price_unit:
                continue
            seller = line.with_company(line.company_id)._get_seller_info()
            if not seller and line.price_unit and line.uom_id == line._origin.uom_id and line.partner_id == line._origin.partner_id and not line.product_id._has_vendor_pricelist(line.partner_id, line.company_id):
                continue
            currency = seller['currency_id'] if seller else line.product_id.cost_currency_id
            currency._arg_require_conversion(line.currency_id, line.company_id,
                                             fields.Date.to_date(line.date_order) or fields.Date.context_today(line))


class BillOperation(models.Model):
    _name = 'arg.pyme.purchase.bill.operation'
    _description = 'Evidencia de preparación de factura recibida ARG'
    order_id = fields.Many2one('purchase.order', required=True, ondelete='restrict', check_company=True)
    company_id = fields.Many2one(related='order_id.company_id', store=True)
    move_id = fields.Many2one('account.move', required=True, ondelete='restrict', check_company=True)
    operation_key = fields.Char(required=True)
    payload_hash = fields.Char(required=True)
    user_id = fields.Many2one('res.users', required=True)
    _key_unique = models.Constraint('UNIQUE(order_id,operation_key)', 'La operación ya fue registrada.')

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.su:
            raise AccessError(_('La evidencia se crea únicamente desde la preparación validada.'))
        return super().create(vals_list)

    def write(self, values):
        raise AccessError(_('La evidencia de preparación se conserva.'))

    def unlink(self):
        raise AccessError(_('La evidencia de preparación se conserva.'))
