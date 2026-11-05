from odoo.addons.arg_pyme_base.tools.quantity import quantity_rounding
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from odoo.tools.float_utils import float_compare
from .purchase_order import _BILL_GENERATION


_ACCOUNT_LIFECYCLE = object()


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'arg.pyme.document.mixin']

    arg_purchase_header_snapshot = fields.Json(readonly=True, copy=False, groups='base.group_user')

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        move_type = values.get('move_type', self.env.context.get('default_move_type'))
        if ('invoice_date' in fields_list and move_type in ('in_invoice', 'in_refund')
                and not values.get('invoice_date') and 'default_invoice_date' not in self.env.context):
            values['invoice_date'] = fields.Date.context_today(self)
        return values

    def _arg_document_code(self):
        if self.move_type == 'in_invoice':
            return 'FRC'
        if self.move_type == 'in_refund':
            return 'NCP'
        return super()._arg_document_code()

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            move_type = values.get('move_type', self.env.context.get('default_move_type', 'entry'))
            if move_type in ('in_invoice', 'in_refund'):
                values.setdefault('state', 'draft')
            if values.get('move_type', self.env.context.get('default_move_type')) in ('in_invoice', 'in_refund') and values.get('state', 'draft') != 'draft':
                raise AccessError(_('La factura recibida se crea en borrador.'))
            if ('arg_purchase_header_snapshot' in values or self.env.context.get('default_arg_purchase_header_snapshot')) and self.env.context.get('_arg_purchase_bill') is not _BILL_GENERATION:
                raise AccessError(_('La evidencia del proveedor se recibe desde una preparación autorizada.'))
            if values.get('move_type') == 'in_refund' and values.get('reversed_entry_id'):
                origin = self.browse(values['reversed_entry_id'])
                origin.check_access('read')
                if origin.arg_purchase_header_snapshot:
                    values['arg_purchase_header_snapshot'] = origin.arg_purchase_header_snapshot
        return super().create(vals_list)

    def write(self, values):
        if 'move_type' in values and any(move.move_type != values['move_type'] for move in self):
            raise UserError(_('El comprobante conserva su tipo. Cree una factura o nota vinculada.'))
        if 'state' in values and self.filtered(lambda move: move.move_type in ('in_invoice', 'in_refund')) and self.env.context.get('_arg_purchase_account_lifecycle') is not _ACCOUNT_LIFECYCLE:
            raise AccessError(_('Use las acciones de publicar, cancelar o volver a borrador.'))
        if 'arg_purchase_header_snapshot' in values:
            raise AccessError(_('La evidencia del proveedor no se edita manualmente.'))
        for move in self.filtered('arg_purchase_header_snapshot'):
            if any(name in values and values[name] != move[name].id for name in ('company_id', 'partner_id', 'currency_id')):
                raise UserError(_('El comprobante conserva compañía, proveedor y moneda de origen.'))
        return super().write(values)

    def _arg_check_purchase_posting(self):
        for move in self:
            move._arg_check_document_access()
            if not self.env.user.has_group('arg_pyme_base.group_manager'):
                raise AccessError(_('Publicar una factura o nota recibida requiere responsable ARG y permisos contables nativos.'))
            if not (move.ref or '').strip():
                raise UserError(_('Complete el número original del comprobante del proveedor. El código FRC/NCP es independiente.'))
            move.company_id.currency_id._arg_require_conversion(move.currency_id, move.company_id, move._get_invoice_currency_rate_date())
            orders = move.invoice_line_ids.purchase_line_id.order_id
            orders._arg_lock()
            for order in orders:
                if order.state != 'purchase' or order.company_id != move.company_id or order.currency_id != move.currency_id or order.partner_id.commercial_partner_id != move.partner_id.commercial_partner_id:
                    raise UserError(_('Revise pedido confirmado, compañía, moneda y proveedor de las líneas vinculadas.'))
                order._arg_freeze()
            if not move.arg_purchase_header_snapshot:
                partner = move.partner_id.with_context(lang='es_AR')
                payload = {'company': {'id': move.company_id.id, 'name': move.company_id.name},
                           'partner': {'id': partner.id, 'name': partner.name or '', 'vat': partner.vat or '',
                                       'address': partner.contact_address or ''}, 'notes': ''}
                super(AccountMove, move).write({'arg_purchase_header_snapshot': payload})

    def _arg_check_purchase_quantities(self):
        # Include the whole posting set, not one draft at a time. The PPC lock serializes other requests.
        for source in self.invoice_line_ids.purchase_line_id:
            lines = self.invoice_line_ids.filtered(lambda line: line.purchase_line_id == source)
            for line in lines:
                if line.product_id != source.product_id or line.product_uom_id != source.uom_id:
                    raise UserError(_('La línea vinculada conserva producto y unidad base del pedido.'))
                if line.quantity <= 0:
                    raise UserError(_('Use cantidades positivas y el tipo factura o nota para indicar el sentido de la operación.'))
            other = source.invoice_lines.filtered(lambda line: line.move_id not in self and line.move_id.state == 'posted')
            def quantity(rows):
                return sum(line.product_uom_id._compute_quantity(line.quantity, source.uom_id)
                           * (1 if line.move_id.move_type == 'in_invoice' else -1) for line in rows)
            net = quantity(other) + quantity(lines)
            # Credits may refund a billed quantity even if a later return has already reduced received quantity.
            if float_compare(net, 0, precision_rounding=quantity_rounding(self.env)) < 0:
                raise UserError(_('La nota supera las unidades facturadas netas de esta línea del pedido.'))
            if lines.filtered(lambda line: line.move_id.move_type == 'in_invoice'):
                base = source.product_qty if source.product_id.purchase_method == 'purchase' else source.qty_received
                if float_compare(net, base, precision_rounding=quantity_rounding(self.env)) > 0:
                    raise UserError(_('Las facturas del lote superan la cantidad pendiente según la política del producto.'))

    def _post(self, *args, **kwargs):
        documents = self.filtered(lambda move: move.move_type in ('in_invoice', 'in_refund'))
        documents._arg_check_purchase_posting()
        soft = args[0] if args else kwargs.get('soft', True)
        actual = documents.filtered(lambda move: not soft or move.date <= fields.Date.context_today(move))
        actual._arg_check_purchase_quantities()
        posted = super(AccountMove, self.with_context(_arg_purchase_account_lifecycle=_ACCOUNT_LIFECYCLE))._post(*args, **kwargs)
        return posted.with_context(_arg_purchase_account_lifecycle=None)

    def button_cancel(self):
        if self.filtered(lambda move: move.move_type in ('in_invoice', 'in_refund')) and not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Cancelar un comprobante recibido requiere responsable ARG.'))
        return super(AccountMove, self.with_context(_arg_purchase_account_lifecycle=_ACCOUNT_LIFECYCLE)).button_cancel()

    def button_draft(self):
        if self.filtered(lambda move: move.move_type in ('in_invoice', 'in_refund')) and not self.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Revertir un comprobante recibido requiere responsable ARG.'))
        return super(AccountMove, self.with_context(_arg_purchase_account_lifecycle=_ACCOUNT_LIFECYCLE)).button_draft()

    @api.depends('write_date', 'state', 'amount_total', 'amount_residual', 'currency_id', 'move_type')
    def _compute_arg_completion_axes(self):
        super()._compute_arg_completion_axes()

    def _arg_get_completion_axes(self):
        if self.move_type not in ('in_invoice', 'in_refund') or self.state != 'posted':
            return super()._arg_get_completion_axes()
        return [self._arg_axis('Cancelación de deuda' if self.move_type == 'in_invoice' else 'Aplicación de crédito', [
            {'label': self.arg_number or self.name, 'unit': self.currency_id.name, 'rounding': self.currency_id.rounding,
             'target': abs(self.amount_total), 'done': max(0, abs(self.amount_total) - abs(self.amount_residual))}])]

    def _arg_document_relations(self):
        result = super()._arg_document_relations()
        if self.move_type in ('in_invoice', 'in_refund'):
            result += [{'label': 'Pedidos al proveedor', 'records': self.invoice_line_ids.purchase_line_id.order_id}]
            if self.reversed_entry_id:
                result.append({'label': 'Comprobante corregido', 'records': self.reversed_entry_id})
            if self.reversal_move_ids:
                result.append({'label': 'Notas vinculadas', 'records': self.reversal_move_ids})
        return result

    def _arg_document_line_relations(self):
        result = super()._arg_document_line_relations()
        if self.move_type in ('in_invoice', 'in_refund'):
            for line in self.invoice_line_ids.filtered('purchase_line_id'):
                result.append({'source_document': line.purchase_line_id.order_id, 'source_line': line.purchase_line_id,
                               'target_document': self, 'target_line': line, 'quantity': line.quantity,
                               'unit': line.product_uom_id.display_name})
        return result

    def action_arg_purchase_treasury(self):
        self._arg_check_document_access()
        if 'arg.pyme.treasury.document' not in self.env:
            raise UserError(_('Los pagos y sus aplicaciones se incorporan con Administración ARG. Deuda saldada no equivale a dinero pagado.'))
        return self.env['arg.pyme.treasury.document']._arg_action_new_from_debt(self)

    def _arg_report_payload(self):
        if self.move_type not in ('in_invoice', 'in_refund'):
            return super()._arg_report_payload()
        snap = self.arg_purchase_header_snapshot or {}
        partner = snap.get('partner') or {'name': self.partner_id.name or '', 'address': self.partner_id.contact_address or ''}
        return {'title': 'Factura recibida ARG' if self.move_type == 'in_invoice' else 'Nota de crédito proveedor ARG',
                'company': snap.get('company', {}).get('name') or self.company_id.name,
                'date': str(self.invoice_date or self.date), 'state_label': dict(self._fields['state']._description_selection(self.env)).get(self.state),
                'partner_name': partner['name'], 'partner_address': partner['address'], 'external_reference': self.ref or '',
                'currency': self.currency_id.name,
                'lines': [{'description': line.name, 'quantity': line.quantity, 'unit': line.product_uom_id.display_name,
                           'unit_price': line.price_unit, 'total': line.price_total}
                          for line in self.invoice_line_ids if line.display_type == 'product'],
                'totals': [{'label': 'Neto', 'amount': self.amount_untaxed}, {'label': 'Impuestos', 'amount': self.amount_tax},
                           {'label': 'Total', 'amount': self.amount_total}, {'label': 'Deuda pendiente', 'amount': self.amount_residual}],
                'notes': snap.get('notes') or ''}
