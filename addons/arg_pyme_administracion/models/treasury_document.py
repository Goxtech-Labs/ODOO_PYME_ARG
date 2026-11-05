import math
import uuid
import hashlib
import json
from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import SQL

_TREASURY_ENGINE = object()


def engine(env):
    return env.context.get('_arg_treasury_engine') is _TREASURY_ENGINE


def check_manager(env):
    if not env.user.has_group('arg_pyme_administracion.group_finance_manager'):
        raise AccessError(_('La operación requiere Responsable Administración ARG.'))


class TreasuryDocument(models.Model):
    _name = 'arg.pyme.treasury.document'
    _inherit = ['arg.pyme.document.mixin']
    _description = 'Recibo / orden de pago ARG'
    _rec_name = 'arg_number'
    _order = 'id desc'
    _check_company_auto = True

    kind = fields.Selection([('REC', 'Recibo de cobranza'), ('OPA', 'Orden de pago')], required=True, default='REC', string='Tipo documental')
    company_id = fields.Many2one('res.company', required=True, default=lambda s: s.env.company, index=True)
    partner_id = fields.Many2one('res.partner', string='Tercero', required=True, check_company=True, ondelete='restrict')
    commercial_partner_id = fields.Many2one(related='partner_id.commercial_partner_id', readonly=True)
    date = fields.Date(string='Fecha', required=True, default=fields.Date.context_today)
    currency_id = fields.Many2one('res.currency', string='Moneda', required=True,
                                  default=lambda s: s.env.company.arg_default_currency_id or s.env.company.currency_id)
    note = fields.Text(string='Observaciones')
    debt_move_ids = fields.Many2many('account.move', 'arg_treasury_debt_rel', 'document_id', 'move_id', string='Facturas a aplicar', check_company=True)
    line_ids = fields.One2many('arg.pyme.treasury.line', 'document_id', string='Medios')
    payment_ids = fields.One2many('account.payment', 'arg_treasury_document_id', readonly=True, string='Pagos nativos')
    reversal_move_ids = fields.Many2many('account.move', 'arg_treasury_reversal_rel', 'document_id', 'move_id', readonly=True, copy=False, string='Asientos inversos', check_company=True)
    event_ids = fields.One2many('arg.pyme.treasury.audit.event', 'document_id', readonly=True, string='Historial')
    confirmed_at = fields.Datetime(readonly=True, copy=False)
    canceled_at = fields.Datetime(readonly=True, copy=False)
    reverted_at = fields.Datetime(readonly=True, copy=False)
    snapshot = fields.Json(readonly=True, copy=False)
    state = fields.Selection([('draft', 'Borrador'), ('confirmed', 'Confirmado'), ('exception', 'Revisar efectos contables'),
                              ('canceled', 'Cancelado'), ('reverted', 'Revertido')], string='Estado', compute='_compute_status', compute_sudo=False)
    total = fields.Monetary(compute='_compute_amounts', compute_sudo=False, aggregator=False)
    free_amount = fields.Monetary(string='Libre por aplicar', compute='_compute_amounts', compute_sudo=False, aggregator=False)
    applied_amount = fields.Monetary(string='Aplicado', compute='_compute_amounts', compute_sudo=False, aggregator=False)
    partial_ids = fields.Many2many('account.partial.reconcile', compute='_compute_partials', compute_sudo=False, string='Aplicaciones vigentes')

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        if 'line_ids' in fields_list and 'line_ids' not in values:
            company = self.env['res.company'].browse(values.get('company_id') or self.env.company.id)
            if company not in self.env.companies:
                raise AccessError(_('Compañía no habilitada.'))
            method = company.arg_receipt_method_id if values.get('kind', 'REC') == 'REC' else company.arg_payment_method_id
            if method:
                values['line_ids'] = [Command.create({'method_id': method.id, 'amount': 0})]
        return values

    def _arg_document_code(self):
        return self.kind

    def _arg_check(self, manager=False):
        self.ensure_one()
        self._arg_check_document_access()
        if not self.env.user.has_group('arg_pyme_base.group_administracion'):
            raise AccessError(_('La operación requiere Administración ARG.'))
        if manager:
            check_manager(self.env)
            self.check_access('write')

    def _arg_lock(self):
        self._arg_check(manager=True)
        self.flush_recordset()
        self.env.cr.execute(SQL('UPDATE arg_pyme_treasury_document SET write_date=clock_timestamp(), write_uid=%s WHERE id=%s', self.env.uid, self.id))
        self.invalidate_recordset()

    def _arg_lock_draft(self):
        # Preparing is an operator action; serialize child CRUD against confirmation without granting manager rights.
        for doc in self.sorted('id'):
            doc._arg_check()
            doc.check_access('write')
            doc.flush_recordset(['confirmed_at', 'canceled_at', 'write_date', 'write_uid'])
            self.env.cr.execute(SQL('UPDATE arg_pyme_treasury_document SET write_date=clock_timestamp(), write_uid=%s WHERE id=%s', self.env.uid, doc.id))
            doc.invalidate_recordset(['confirmed_at', 'canceled_at', 'state', 'line_ids'])
            if doc.confirmed_at or doc.canceled_at:
                raise UserError(_('El documento ya no admite cambios en sus medios.'))

    @api.depends('confirmed_at', 'canceled_at', 'reverted_at', 'payment_ids.state', 'payment_ids.move_id.state')
    def _compute_status(self):
        for doc in self:
            if doc.reverted_at:
                doc.state = 'reverted'
            elif doc.canceled_at:
                doc.state = 'canceled'
            elif not doc.confirmed_at:
                doc.state = 'draft'
            elif (not doc.payment_ids or any(not doc._arg_payment_expected(p) for p in doc.payment_ids)):
                doc.state = 'exception'
            else:
                doc.state = 'confirmed'

    def _arg_counterparts(self):
        self.ensure_one()
        return self._arg_effect_payments().move_id.line_ids.filtered(lambda l: l.account_type in ('asset_receivable', 'liability_payable'))

    @api.depends('line_ids.amount', 'confirmed_at', 'reverted_at', 'payment_ids.state',
                 'payment_ids.move_id.line_ids.amount_residual_currency', 'payment_ids.move_id.state')
    def _compute_amounts(self):
        for doc in self:
            doc.total = sum(doc.line_ids.mapped('amount'))
            if not doc.confirmed_at or doc.reverted_at:
                doc.free_amount = doc.applied_amount = 0
            else:
                # Generated payments use the wrapper currency and no writeoff. Their actual native residual is authoritative.
                free = sum(abs(l.amount_residual_currency) for l in doc._arg_counterparts())
                doc.free_amount = free
                doc.applied_amount = max(0, doc._arg_effect_nominal() - free)

    @api.depends('payment_ids.move_id.line_ids.matched_debit_ids', 'payment_ids.move_id.line_ids.matched_credit_ids')
    def _compute_partials(self):
        for doc in self:
            lines = doc._arg_counterparts()
            doc.partial_ids = lines.matched_debit_ids | lines.matched_credit_ids

    @api.model_create_multi
    def create(self, vals_list):
        protected = self._arg_protected_fields()
        for values in vals_list:
            if protected.intersection(values) or any(self.env.context.get('default_'+k) for k in protected):
                raise AccessError(_('Los efectos y la evidencia se generan desde las acciones del documento.'))
        records = super().create(vals_list)
        records._arg_validate_header()
        return records

    @api.model
    def _arg_protected_fields(self):
        return {'state', 'confirmed_at', 'canceled_at', 'reverted_at', 'snapshot', 'payment_ids', 'reversal_move_ids',
                'event_ids', 'partial_ids', 'total', 'free_amount', 'applied_amount', 'commercial_partner_id'}

    def write(self, values):
        if not engine(self.env):
            if self._arg_protected_fields().intersection(values):
                raise AccessError(_('Los efectos y la evidencia no se editan manualmente.'))
            if any(d.confirmed_at or d.canceled_at for d in self):
                raise UserError(_('El documento conserva sus datos. Use desaplicar o revertir, según corresponda.'))
            if 'kind' in values and any(d.kind != values['kind'] for d in self):
                raise UserError(_('El tipo documental no cambia después de numerarse.'))
        result = super().write(values)
        self._arg_validate_header()
        return result

    def _arg_validate_header(self):
        for doc in self:
            if doc.company_id not in self.env.companies:
                raise AccessError(_('Compañía no habilitada.'))
            if doc.partner_id.company_id and doc.partner_id.company_id != doc.company_id:
                raise ValidationError(_('El tercero pertenece a otra compañía.'))
            expected = 'out_invoice' if doc.kind == 'REC' else 'in_invoice'
            for move in (doc.debt_move_ids if not doc.confirmed_at else self.env['account.move']):
                move.check_access('read')
                if (move.company_id != doc.company_id or move.partner_id.commercial_partner_id != doc.partner_id.commercial_partner_id
                        or move.move_type != expected or move.state != 'posted'):
                    raise ValidationError(_('Seleccione facturas publicadas del mismo tercero, compañía y sentido.'))

    def _arg_debt_lines(self, moves=None):
        self.ensure_one()
        moves = moves if moves is not None else self.debt_move_ids
        account_type = 'asset_receivable' if self.kind == 'REC' else 'liability_payable'
        return moves.line_ids.filtered(lambda l: l.parent_state == 'posted' and l.account_type == account_type
                                      and not l.reconciled and (not l.currency_id.is_zero(l.amount_residual_currency)
                                                               or not l.company_currency_id.is_zero(l.amount_residual)))

    def _arg_check_configuration(self):
        self._arg_validate_header()
        if not self.line_ids or len(self.line_ids) > 100:
            raise UserError(_('Agregue entre uno y cien medios de cobro o pago.'))
        fx = self.company_id.currency_id._arg_require_conversion(self.currency_id, self.company_id, self.date)
        for line in self.line_ids:
            if not math.isfinite(line.amount) or self.currency_id.compare_amounts(line.amount, 0) <= 0:
                raise UserError(_('Cada medio necesita un importe positivo.'))
            self._arg_check_line_configuration(line)
        for move in self.debt_move_ids:
            self.company_id.currency_id._arg_require_conversion(move.currency_id, self.company_id, self.date)
        return fx

    def _arg_check_line_configuration(self, line):
        method = line.method_id
        method.check_access('read')
        direction = 'inbound' if self.kind == 'REC' else 'outbound'
        if (not method or method.journal_id.company_id != self.company_id or method.journal_id.type not in ('bank', 'cash')
                or method.payment_method_id.payment_type != direction or method.code != 'manual'):
            raise UserError(_('Seleccione un medio manual de caja o banco de esta compañía y del sentido correspondiente.'))
        if not method.payment_account_id:
            raise UserError(_('Configure la cuenta transitoria del medio antes de confirmar.'))
        if method.journal_id.currency_id and method.journal_id.currency_id != self.currency_id:
            raise UserError(_('La moneda del medio no coincide con la del documento.'))

    def action_confirm(self):
        self.ensure_one()
        self._arg_lock()
        if self.confirmed_at:
            return self._arg_action()
        if self.canceled_at:
            raise UserError(_('El documento está cancelado.'))
        self._arg_prepare_confirmation()
        fx = self._arg_check_configuration()
        if self.debt_move_ids and not self._arg_debt_lines():
            raise UserError(_('Las facturas seleccionadas ya no tienen deuda. Revise las aplicaciones o quite el origen para un anticipo.'))
        company_doc = self.with_company(self.company_id)
        clean = {k: v for k, v in company_doc.env.context.items() if not k.startswith('default_')}
        doc = company_doc.with_context(clean, _arg_treasury_engine=_TREASURY_ENGINE,
                tracking_disable=True, mail_notrack=True, skip_sale_auto_invoice_send=True)
        doc._arg_event('confirm_prepare', {'amount': doc.total, 'currency': doc.currency_id.name, 'fx': fx})
        for line in doc.line_ids.sorted('id'):
            payments = doc._arg_create_line_payment(line)
            doc._arg_validate_line_payment(line, payments)
            line.write({'payment_id': payments.id})
            doc._arg_finalize_line_payment(line, payments)
        snapshot = {'company': doc.company_id.name, 'partner': {'name': doc.partner_id.name, 'address': doc.partner_id.contact_address or ''},
                    'date': str(doc.date), 'currency': doc.currency_id.name, 'fx': fx,
                    'lines': [doc._arg_line_snapshot(l) for l in doc.line_ids]}
        doc.write({'confirmed_at': fields.Datetime.now(), 'snapshot': snapshot})
        doc._arg_event('confirm', {'payment_ids': doc.payment_ids.ids, 'move_ids': doc.payment_ids.move_id.ids, 'snapshot': snapshot})
        return self._arg_action()

    def _arg_create_line_payment(self, line):
        debt = self._arg_debt_lines()
        if debt:
            # The native register handles existing debt, including multiple installments and partial payment.
            context = {k: v for k, v in self.env.context.items() if not k.startswith('default_')}
            wizard = self.env['account.payment.register'].with_context(context, active_model='account.move.line', active_ids=debt.ids).create({
                'line_ids': [Command.set(debt.ids)], 'payment_date': self.date, 'amount': line.amount,
                'currency_id': self.currency_id.id, 'journal_id': line.method_id.journal_id.id,
                'payment_method_line_id': line.method_id.id, 'group_payment': True,
                'payment_difference_handling': 'open', 'installments_mode': 'full',
                'communication': self.arg_number, 'arg_treasury_document_id': self.id})
            if not wizard.can_edit_wizard or len(wizard._get_batches()) != 1:
                raise UserError(_('Estas facturas usan cuentas o condiciones diferentes. Registre documentos separados.'))
            payments = wizard._create_payments()
        else:
            # The register requires eligible debt; advances deliberately use native account.payment directly.
            payments = self.env['account.payment'].create({
                'company_id': self.company_id.id, 'partner_id': self.partner_id.commercial_partner_id.id,
                'partner_type': 'customer' if self.kind == 'REC' else 'supplier',
                'payment_type': 'inbound' if self.kind == 'REC' else 'outbound',
                'date': self.date, 'currency_id': self.currency_id.id, 'amount': line.amount,
                'journal_id': line.method_id.journal_id.id, 'payment_method_line_id': line.method_id.id,
                'memo': self.arg_number, 'arg_treasury_document_id': self.id})
            payments.action_post()
        return payments

    def _arg_validate_line_payment(self, line, payments):
        if (len(payments) != 1 or payments.move_id.state != 'posted' or payments.state not in ('paid', 'reconciled')
                or payments.company_id != self.company_id or payments.currency_id != self.currency_id
                or payments.partner_id.commercial_partner_id != self.partner_id.commercial_partner_id
                or payments.currency_id.compare_amounts(payments.amount, line.amount)):
            raise UserError(_('El pago nativo no produjo el efecto esperado. Revise la configuración; no se confirmó este documento.'))
        counterpart = payments.move_id.line_ids.filtered(lambda l: l.account_type == ('asset_receivable' if self.kind == 'REC' else 'liability_payable'))
        liquidity = payments.move_id.line_ids.filtered(lambda l: l.account_id == line.method_id.payment_account_id)
        if (len(counterpart) != 1 or len(liquidity) != 1 or len(payments.move_id.line_ids) != 2
                or counterpart.currency_id != self.currency_id or liquidity.currency_id != self.currency_id
                or self.currency_id.compare_amounts(abs(counterpart.amount_currency), line.amount)
                or self.currency_id.compare_amounts(abs(liquidity.amount_currency), line.amount)):
            raise UserError(_('El medio debe generar un asiento simple de dinero y contrapartida por el importe indicado. Revise su configuración.'))

    def _arg_prepare_confirmation(self):
        """Optional media reserve/check their identities before posting any line."""
        return None

    def _arg_finalize_line_payment(self, line, payment):
        return None

    def _arg_line_snapshot(self, line):
        return {'method': line.method_id.name, 'journal': line.method_id.journal_id.name,
                'amount': line.amount, 'payment_id': line.payment_id.id, 'move_id': line.payment_id.move_id.id}

    def _arg_effect_payments(self):
        self.ensure_one()
        return self.payment_ids

    def _arg_effect_nominal(self):
        self.ensure_one()
        return sum(self.line_ids.mapped('amount'))

    def _arg_payment_expected(self, payment):
        return payment.state in ('paid', 'reconciled') and payment.move_id.state == 'posted'

    def _arg_before_reverse(self):
        return None

    def _arg_after_reverse(self, inverses, date, reason):
        return None

    def _arg_event(self, kind, payload, **values):
        self.ensure_one()
        self._arg_check(manager=True)
        return self.env['arg.pyme.treasury.audit.event'].with_context(_arg_treasury_engine=_TREASURY_ENGINE).create({
            'document_id': self.id, 'company_id': self.company_id.id, 'kind': kind,
            'request_key': str(uuid.uuid4()), 'actor_id': self.env.uid, 'event_date': fields.Datetime.now(),
            'currency_id': self.currency_id.id, 'payload': payload, **values})

    def _arg_operation(self, key, kind, payload):
        self.ensure_one()
        try:
            key = str(uuid.UUID(key))
        except (ValueError, TypeError, AttributeError):
            raise ValidationError(_('Referencia de operación inválida.'))
        fingerprint = hashlib.sha256(json.dumps({'kind': kind, 'payload': payload}, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        event = self.env['arg.pyme.treasury.audit.event'].search([('document_id', '=', self.id), ('request_key', '=', key)], limit=1)
        if event:
            if event.request_hash != fingerprint or event.kind != kind:
                raise UserError(_('La referencia ya se usó con otra operación.'))
            return False
        return self._arg_event(kind, payload, request_key=key, request_hash=fingerprint)

    def action_apply(self):
        self._arg_check(manager=True)
        if self.state != 'confirmed':
            raise UserError(_('Confirme el documento antes de aplicar su saldo.'))
        return {'type': 'ir.actions.act_window', 'name': _('Aplicar saldo disponible'),
                'res_model': 'arg.pyme.treasury.apply.wizard', 'views': [(False, 'form')], 'target': 'new',
                'context': {'default_document_id': self.id}}

    def _arg_apply(self, move, key):
        self._arg_lock()
        move.ensure_one();move.check_access('read')
        payload = {'move_id': move.id}
        if not self._arg_operation(key, 'apply_request', payload):
            return self._arg_action()
        if self.state != 'confirmed':
            raise UserError(_('El documento no está confirmado.'))
        expected = 'out_invoice' if self.kind == 'REC' else 'in_invoice'
        if (move.state != 'posted' or move.move_type != expected or move.company_id != self.company_id
                or move.partner_id.commercial_partner_id != self.partner_id.commercial_partner_id):
            raise UserError(_('Seleccione una factura publicada del mismo tercero y compañía.'))
        day = max(self.date, move.date)
        self.company_id.currency_id._arg_require_conversion(move.currency_id, self.company_id, day)
        self.company_id.currency_id._arg_require_conversion(self.currency_id, self.company_id, day)
        credits = self._arg_counterparts().filtered(lambda l: not l.reconciled)
        debt = self._arg_debt_lines(move).sorted(lambda l: (l.date_maturity or l.date, l.id))
        if not credits or not debt:
            raise UserError(_('No queda saldo disponible o deuda en esta factura.'))
        applied = False
        for due in debt:
            for credit in credits:
                if (credit.account_id == due.account_id and not credit.reconciled and not due.reconciled
                        and credit.amount_residual * due.amount_residual <= 0):
                    (credit | due).with_company(self.company_id).with_context(_arg_treasury_engine=_TREASURY_ENGINE).reconcile()
                    applied = True
        if not applied:
            raise UserError(_('El anticipo y la deuda no usan la misma cuenta conciliable. Revise las cuentas del tercero.'))
        return self._arg_action()

    def action_unapply(self):
        self._arg_check(manager=True)
        if self.state != 'confirmed' or not self.partial_ids:
            raise UserError(_('No hay aplicaciones vigentes para desaplicar.'))
        return {'type': 'ir.actions.act_window', 'name': _('Desaplicar documento'),
                'res_model': 'arg.pyme.treasury.unapply.wizard', 'views': [(False, 'form')], 'target': 'new',
                'context': {'default_document_id': self.id, 'default_target_ids': self.partial_ids.ids}}

    def _arg_unapply(self, ids, reason, key):
        self._arg_lock()
        if (not isinstance(ids, list) or not ids or len(ids) > 500 or any(type(i) is not int or i <= 0 for i in ids)
                or not (reason or '').strip()):
            raise ValidationError(_('Seleccione aplicaciones válidas y complete el motivo.'))
        ids = sorted(set(ids))
        if not self._arg_operation(key, 'unapply_request', {'partial_ids': ids, 'reason': reason}):
            return self._arg_action()
        if self.state != 'confirmed' or not set(ids).issubset(self.partial_ids.ids):
            raise UserError(_('Las aplicaciones cambiaron. Actualice el documento antes de preparar otra desaplicación.'))
        self.env['account.partial.reconcile'].browse(ids).with_context(_arg_treasury_engine=_TREASURY_ENGINE).unlink()
        return self._arg_action()

    def action_cancel_draft(self):
        self._arg_lock()
        if self.confirmed_at:
            raise UserError(_('Use Revertir para un documento confirmado.'))
        if not self.canceled_at:
            self.with_context(_arg_treasury_engine=_TREASURY_ENGINE).write({'canceled_at': fields.Datetime.now()})
            self._arg_event('cancel', {})
        return self._arg_action()

    def action_reverse(self):
        self._arg_check(manager=True)
        if self.state not in ('confirmed', 'exception'):
            raise UserError(_('Sólo se revierte un documento con efectos confirmados.'))
        return {'type': 'ir.actions.act_window', 'name': _('Revertir documento'), 'res_model': 'arg.pyme.treasury.reverse.wizard',
                'views': [(False, 'form')], 'target': 'new', 'context': {'default_document_id': self.id}}

    def _arg_reverse(self, date, reason, key):
        self._arg_lock()
        date = fields.Date.to_date(date)
        if not date or not (reason or '').strip():
            raise UserError(_('Complete fecha y motivo de reversión.'))
        if not self._arg_operation(key, 'reverse_request', {'date': str(date), 'reason': reason}):
            return self._arg_action()
        if self.reverted_at:
            return self._arg_action()
        if not self.confirmed_at:
            raise UserError(_('El documento aún no tiene efectos para revertir.'))
        self._arg_before_reverse()
        moves = self._arg_effect_payments().move_id
        if not moves or any(m.state != 'posted' for m in moves):
            raise UserError(_('Hay efectos contables fuera de estado. Revise los pagos nativos antes de revertir.'))
        for payment in self._arg_effect_payments():
            liquidity, _, _ = payment._seek_for_lines()
            if liquidity.matched_debit_ids or liquidity.matched_credit_ids:
                raise UserError(_('El pago tiene conciliación de caja/banco. Revise y desaplique esa conciliación antes de revertir.'))
        doc = self.with_company(self.company_id).with_context(_arg_treasury_engine=_TREASURY_ENGINE)
        doc._arg_event('reverse_prepare', {'date': str(date), 'reason': reason, 'move_ids': moves.ids})
        # Native reverse posts inverse entries and reconciles against originals; it does not erase the ledger.
        inverses = moves.with_company(self.company_id).with_context(_arg_treasury_engine=_TREASURY_ENGINE, tracking_disable=True)._reverse_moves([
            {'date': date, 'ref': self.arg_number + ' · ' + reason, 'arg_treasury_document_id': self.id} for move in moves], cancel=True)
        doc.write({'reverted_at': fields.Datetime.now(), 'reversal_move_ids': [Command.set(inverses.ids)]})
        doc._arg_after_reverse(inverses, date, reason)
        doc._arg_event('reverse', {'date': str(date), 'reason': reason, 'move_ids': inverses.ids})
        return self._arg_action()

    def _arg_action(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window', 'name': self.arg_number, 'res_model': self._name,
                'res_id': self.id, 'views': [(self.env.ref('arg_pyme_administracion.treasury_form').id, 'form')], 'target': 'current'}

    @api.model
    def _arg_action_new_from_debt(self, move):
        move.ensure_one();move.check_access('read')
        if not self.env.user.has_group('arg_pyme_base.group_administracion') or move.company_id not in self.env.companies:
            raise AccessError(_('La operación requiere Administración ARG en la compañía del comprobante.'))
        if move.state != 'posted':
            raise UserError(_('Publique primero la factura.'))
        if move.move_type not in ('out_invoice', 'in_invoice') or move.currency_id.is_zero(move.amount_residual):
            action = self.env.ref('arg_pyme_administracion.action_customer_account' if move.is_sale_document() else 'arg_pyme_administracion.action_supplier_account').read()[0]
            action['domain'] = [('move_id', '=', move.id)]
            action['context'] = {}
            return action
        kind = 'REC' if move.move_type == 'out_invoice' else 'OPA'
        method = move.company_id.arg_receipt_method_id if kind == 'REC' else move.company_id.arg_payment_method_id
        return {'type': 'ir.actions.act_window', 'name': _('Preparar cobro / pago'), 'res_model': self._name,
                'views': [(self.env.ref('arg_pyme_administracion.treasury_form').id, 'form')], 'target': 'current',
                'context': {'default_kind': kind, 'default_company_id': move.company_id.id, 'default_partner_id': move.partner_id.id,
                            'default_currency_id': move.currency_id.id, 'default_debt_move_ids': [Command.set(move.ids)],
                            'default_line_ids': [Command.create({'method_id': method.id, 'amount': abs(move.amount_residual)})]}}

    @api.depends('state', 'line_ids.amount', 'payment_ids.move_id.line_ids.amount_residual_currency', 'payment_ids.state')
    def _compute_arg_completion_axes(self):
        super()._compute_arg_completion_axes()

    def _arg_get_completion_axes(self):
        if not self.confirmed_at or self.reverted_at:
            return []
        return [self._arg_axis('Aplicación a deuda', [{'label': self.arg_number, 'unit': self.currency_id.name,
                'rounding': self.currency_id.rounding, 'target': self.total, 'done': self.applied_amount}])]

    def _arg_document_relations(self):
        invoices = self.partial_ids.debit_move_id.move_id | self.partial_ids.credit_move_id.move_id
        return [{'label': 'Facturas seleccionadas al preparar', 'records': self.debt_move_ids},
                {'label': 'Documentos de aplicaciones vigentes', 'records': invoices - self.payment_ids.move_id},
                {'label': 'Pagos nativos', 'records': self.payment_ids}, {'label': 'Asientos inversos', 'records': self.reversal_move_ids}]

    def _arg_report_payload(self):
        snap = self.snapshot or {};partner = snap.get('partner') or {'name': self.partner_id.name, 'address': self.partner_id.contact_address or ''}
        return {'title': _('Recibo de cobranza ARG') if self.kind == 'REC' else _('Orden de pago ARG'),
                'date': str(self.date), 'state_label': dict(self._fields['state']._description_selection(self.env)).get(self.state),
                'company': snap.get('company') or self.company_id.name, 'partner_name': partner['name'], 'partner_address': partner['address'],
                'external_reference': self.arg_reference or '', 'currency': self.currency_id.name,
                'lines': [{'description': l['method'] + ' · ' + l['journal'], 'quantity': 1, 'unit': '', 'unit_price': l['amount'], 'total': l['amount']}
                          for l in (snap.get('lines') or [{'method': l.method_id.name or '', 'journal': l.method_id.journal_id.name or '', 'amount': l.amount} for l in self.line_ids])],
                'totals': [{'label': _('Total'), 'amount': self.total}, {'label': _('Aplicado'), 'amount': self.applied_amount},
                           {'label': _('Libre por aplicar'), 'amount': self.free_amount}], 'notes': self.note or ''}


class TreasuryLine(models.Model):
    _name = 'arg.pyme.treasury.line'
    _description = 'Medio de recibo / pago ARG'
    _check_company_auto = True
    _order = 'id'

    document_id = fields.Many2one('arg.pyme.treasury.document', required=True, ondelete='cascade', index=True)
    company_id = fields.Many2one(related='document_id.company_id', store=True)
    currency_id = fields.Many2one(related='document_id.currency_id')
    method_id = fields.Many2one('account.payment.method.line', string='Medio', check_company=True, ondelete='restrict')
    amount = fields.Monetary(string='Importe')
    payment_id = fields.Many2one('account.payment', readonly=True, copy=False, ondelete='restrict', check_company=True)
    _payment_unique = models.Constraint('UNIQUE(payment_id)', 'El pago ya pertenece a otro medio documental.')

    def _arg_check_draft(self):
        self.document_id._arg_lock_draft()

    @api.model_create_multi
    def create(self, vals_list):
        derived = {'company_id', 'currency_id'}
        if any(derived.intersection(v) for v in vals_list) or any(self.env.context.get('default_'+k) for k in derived):
            raise AccessError(_('La compañía y moneda del medio se reciben del documento.'))
        if not engine(self.env):
            if any(v.get('payment_id') for v in vals_list) or self.env.context.get('default_payment_id'):
                raise AccessError(_('El pago se asigna al confirmar.'))
            ids = [v.get('document_id') or self.env.context.get('default_document_id') for v in vals_list]
            self.env['arg.pyme.treasury.document'].browse([i for i in ids if i])._arg_lock_draft()
        return super().create(vals_list)

    def write(self, vals):
        if {'company_id', 'currency_id'}.intersection(vals):
            raise AccessError(_('La compañía y moneda del medio se reciben del documento.'))
        if not engine(self.env):
            docs = self.document_id
            if vals.get('document_id'):
                docs |= self.env['arg.pyme.treasury.document'].browse(vals['document_id'])
            docs._arg_lock_draft()
            if 'payment_id' in vals:
                raise AccessError(_('El pago no se reasigna manualmente.'))
        return super().write(vals)

    def unlink(self):
        self._arg_check_draft()
        return super().unlink()

    @api.constrains('amount')
    def _check_amount(self):
        if any(not math.isfinite(l.amount) or l.amount < 0 for l in self):
            raise ValidationError(_('El importe debe ser finito y no negativo.'))


class TreasuryCompany(models.Model):
    _inherit = 'res.company'
    arg_receipt_method_id = fields.Many2one('account.payment.method.line', string='Medio de cobro predeterminado ARG', check_company=True)
    arg_payment_method_id = fields.Many2one('account.payment.method.line', string='Medio de pago predeterminado ARG', check_company=True)

    @api.constrains('arg_receipt_method_id', 'arg_payment_method_id')
    def _check_arg_methods(self):
        for company in self:
            for method, direction in [(company.arg_receipt_method_id, 'inbound'), (company.arg_payment_method_id, 'outbound')]:
                if method and (method.journal_id.company_id != company or method.payment_method_id.payment_type != direction or method.code != 'manual'):
                    raise ValidationError(_('El medio predeterminado debe ser manual, de esta compañía y del sentido correspondiente.'))
