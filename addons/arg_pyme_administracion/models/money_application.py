import math
from odoo import api, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _arg_payment_cash_fraction(self, payment, counterpart, invoice_amount):
        """Return this invoice partial's cash amount, or None when native accounting does not prove allocation."""
        self.ensure_one()
        move = counterpart.move_id
        if not payment.has_access('read') or not move.has_access('read') or not move.line_ids.has_access('read'):
            return None
        wrapper = payment.arg_treasury_document_id
        if wrapper and not wrapper.has_access('read'):
            return None
        if (payment.move_id != move or payment.state not in ('paid', 'reconciled') or move.state != 'posted'
                or (wrapper and wrapper.reverted_at)):
            return None
        liquidity = move.line_ids.filtered(lambda l: l.account_id in payment._get_valid_liquidity_accounts()
                                          and l.account_type not in ('asset_receivable', 'liability_payable'))
        counterparts = move.line_ids.filtered(lambda l: l.account_type in ('asset_receivable', 'liability_payable'))
        other = move.line_ids - liquidity - counterparts
        if (not liquidity or len(counterparts) != 1 or counterparts != counterpart
                or any(l.currency_id != payment.currency_id for l in move.line_ids)):
            return None
        liquid = sum(liquidity.mapped('amount_currency'));base = counterpart.amount_currency
        extra = sum(other.mapped('amount_currency'));cur = payment.currency_id
        if (not all(math.isfinite(x) for x in (liquid, base, extra)) or cur.is_zero(base)
                or liquid * base >= 0 or not cur.is_zero(liquid + base + extra)):
            return None
        if not other:
            return invoice_amount if cur.compare_amounts(abs(liquid), abs(base)) == 0 else None

        # Native EPD is attributed per invoice before any generic payment-level proration.
        partials = counterpart.matched_debit_ids | counterpart.matched_credit_ids
        invoices = (partials.debit_move_id | partials.credit_move_id).move_id
        if not partials.has_access('read') or not invoices.has_access('read'):
            return None
        candidates = invoices.filtered(lambda inv: inv.move_type in ('out_invoice','in_invoice') and inv.invoice_payment_term_id.early_discount)
        epd = []
        epd_accounts = self.env['account.account']
        for invoice in candidates:
            terms, account = invoice._get_payment_term_epd_info()
            epd_accounts |= account
            actual, _exchange = invoice._get_reconciled_invoices_partials()
            actual = [(part, abs(amount)) for part, amount, other_line in actual if other_line == counterpart]
            # The nominal invoice total is not evidence that this payment actually settled that total.
            if (len(terms) == 1 and len(actual) == 1 and actual[0][0].has_access('read')
                    and invoice.currency_id.compare_amounts(actual[0][1], abs(invoice.amount_total)) == 0
                    and invoice._is_early_payment_discount_applied(move, actual[0][1], terms, account)):
                epd.append((invoice, terms))
        epd_shaped = bool(candidates and other.filtered(lambda l: l.account_id in epd_accounts or l.tax_repartition_line_id))
        if epd_shaped:
            if len(epd) != 1:
                return None
            discounted, term = epd[0]
            discount = abs(term.amount_currency - term.discount_amount_currency)
            if (discounted.currency_id != cur or cur.compare_amounts(abs(extra), discount)
                    or any(l.account_id not in epd_accounts and not l.tax_repartition_line_id for l in other)):
                return None
            if self == discounted:
                if self.currency_id.compare_amounts(invoice_amount, abs(self.amount_total)):
                    return None
                return abs(term.discount_amount_currency)
            return invoice_amount
        # A standard single generic writeoff, in payment currency; company balances may round differently.
        if len(other) != 1:
            return None
        fraction = abs(liquid / base)
        if not math.isfinite(fraction) or fraction < 0 or fraction > 1:
            return None
        return invoice_amount * fraction

    def _arg_plain_cash_partial(self, counterpart, invoice_amount):
        """One actual cash account and one debt account; complex/manual splits require review."""
        move = counterpart.move_id
        if not move.line_ids.has_access('read'):
            return None
        liquidity = move.line_ids.filtered(lambda l: l.account_type == 'asset_cash')
        debt = move.line_ids.filtered(lambda l: l.account_type in ('asset_receivable', 'liability_payable'))
        if not liquidity:
            return 0.0
        if (move.state != 'posted' or len(liquidity) != 1 or len(debt) != 1 or debt != counterpart
                or len(move.line_ids) != 2 or liquidity.currency_id != counterpart.currency_id):
            return None
        if counterpart.currency_id.compare_amounts(liquidity.amount_currency, -counterpart.amount_currency):
            return None
        if move.statement_line_id:
            statement = move.statement_line_id
            statement.check_access('read')
            if (statement.move_id != move or statement.journal_id.default_account_id != liquidity.account_id
                    or statement.company_id != self.company_id):
                return None
        return invoice_amount

    def _arg_cash_detail(self):
        self.ensure_one();self.check_access('read')
        result = {'known': 0.0, 'unknown': False, 'evidence': [], 'reason': ''}
        if self.state != 'posted':
            return result
        if not self.env['account.move.line'].has_access('read') or not self.env['account.partial.reconcile'].has_access('read'):
            result.update(unknown=True, reason=_('La consulta de aplicaciones requiere permisos contables.'))
            return result
        partials, _exchange_ids = self._get_reconciled_invoices_partials()
        seen = set();explained = 0.0
        for partial, amount, counterpart in partials:
            if partial.id in seen:
                continue
            seen.add(partial.id)
            if not partial.has_access('read') or not counterpart.has_access('read') or not counterpart.move_id.has_access('read'):
                result.update(unknown=True, reason=_('Hay aplicaciones no disponibles con estos permisos.'))
                continue
            amount = abs(amount);explained += amount;other = counterpart.move_id
            value = 0.0
            if other.move_type == 'entry':
                if other.reversal_move_ids.filtered(lambda m: m.state == 'posted') or other.state != 'posted':
                    value = None
                elif counterpart.payment_id:
                    value = self._arg_payment_cash_fraction(counterpart.payment_id, counterpart, amount)
                else:
                    value = self._arg_plain_cash_partial(counterpart, amount)
            if value is None:
                result.update(unknown=True, reason=_('Una aplicación requiere revisar el desglose de dinero, descuentos o ajustes.'))
            else:
                result['known'] += value
            result['evidence'].append({'partial_id': partial.id, 'counterpart_move_id': other.id,
                                      'invoice_amount': amount, 'cash_amount': value})
        settled = max(0, abs(self.amount_total) - abs(self.amount_residual))
        if self.currency_id.compare_amounts(explained, settled):
            result.update(unknown=True, reason=_('Las aplicaciones visibles no explican todo el saldo cancelado.'))
        result['known'] = self.currency_id.round(result['known'])
        return result

    def _arg_money_axis(self, label):
        rows = [];has_unknown = False
        for invoice in self.filtered(lambda m: m.state == 'posted' and m.move_type in ('out_invoice', 'in_invoice')):
            detail = invoice._arg_cash_detail();has_unknown |= detail['unknown']
            rows.append({'label': getattr(invoice, 'arg_number', False) or invoice.name, 'unit': invoice.currency_id.name,
                         'rounding': invoice.currency_id.rounding, 'target': abs(invoice.amount_total), 'done': detail['known'],
                         'unknown': detail['unknown'], 'explanation': detail['reason']})
        axis = self.env['arg.pyme.document.mixin']._arg_axis(label, rows)
        if has_unknown:
            axis['state'] = 'unknown'
            for line in axis['lines']:
                if line.get('unknown'):
                    line['pending'] = None
        return axis

    @api.depends('state', 'amount_total', 'amount_residual', 'line_ids.matched_debit_ids', 'line_ids.matched_credit_ids',
                 'line_ids.matched_debit_ids.debit_move_id.move_id.state', 'line_ids.matched_credit_ids.credit_move_id.move_id.state')
    def _compute_arg_completion_axes(self):
        parent = getattr(super(), '_compute_arg_completion_axes', None)
        if parent:
            parent()

    def _arg_get_completion_axes(self):
        parent = getattr(super(), '_arg_get_completion_axes', None)
        axes = parent() if parent else []
        if self.state == 'posted' and self.move_type in ('out_invoice', 'in_invoice'):
            axes += [self._arg_money_axis(_('Dinero cobrado aplicado') if self.move_type == 'out_invoice' else _('Dinero pagado aplicado'))]
        return axes

    def _arg_document_relations(self):
        parent = getattr(super(), '_arg_document_relations', None)
        relations = parent() if parent else []
        if self.move_type not in ('out_invoice', 'in_invoice', 'out_refund', 'in_refund'):
            return relations
        if not self.env['account.move.line'].has_access('read') or not self.env['account.partial.reconcile'].has_access('read'):
            return relations
        partials, _exchange_ids = self._get_reconciled_invoices_partials()
        visible = self.env['account.move.line']
        for partial, amount, counterpart in partials:
            if partial.has_access('read') and counterpart.has_access('read'):
                visible |= counterpart
        return relations + [{'label': 'Asientos de aplicaciones vigentes', 'records': visible.move_id},
                            {'label': 'Recibos / órdenes de aplicaciones vigentes', 'records': visible.move_id.arg_treasury_document_id}]
