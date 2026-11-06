import hashlib
import math
import re
import uuid
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import SQL
from .value_event import _VALUE_ENGINE, value_engine


class ValueInstrument(models.Model):
    _name = 'arg.pyme.value.instrument'
    _inherit = ['arg.pyme.document.mixin']
    _description = 'Cheque / pagaré ARG'
    _rec_name = 'arg_number'
    _order = 'id desc'
    _check_company_auto = True

    date = fields.Date(string='Fecha de registro', required=True, default=fields.Date.context_today)
    partner_id = fields.Many2one('res.partner', string='Tercero', required=True, check_company=True, ondelete='restrict')
    instrument_kind = fields.Selection([('cheque', 'Cheque'), ('promissory', 'Pagaré')], required=True, default='cheque', string='Documento')
    ownership = fields.Selection([('third_party', 'De terceros'), ('own', 'Propio')], required=True, default='third_party', string='Origen')
    support = fields.Selection([('paper', 'Papel'), ('electronic', 'Electrónico / ECHEQ')], required=True, default='paper', string='Soporte')
    cheque_type = fields.Selection([('common', 'Común'), ('deferred', 'De pago diferido')], default='deferred', string='Clase de cheque')
    currency_id = fields.Many2one('res.currency', required=True, string='Moneda', default=lambda s: s.env.company.arg_default_currency_id or s.env.company.currency_id)
    amount = fields.Monetary(string='Importe nominal', required=True, aggregator=False)
    company_id = fields.Many2one('res.company', required=True, default=lambda s: s.env.company, index=True)
    bank_account_id = fields.Many2one('res.partner.bank', string='Cuenta libradora registrada', check_company=True, ondelete='restrict')
    bank_name = fields.Char(string='Banco')
    bank_identifier = fields.Char(string='Código bancario', help='Identificador conocido del banco. Al elegir una cuenta registrada se propone su BIC, si está informado; no se inventa un código ausente.')
    issuer_id = fields.Many2one('res.partner', string='Librador / firmante', check_company=True, ondelete='restrict')
    issuer_identifier = fields.Char(string='CUIT / identificación del firmante')
    beneficiary_id = fields.Many2one('res.partner', string='Beneficiario', check_company=True, ondelete='restrict')
    issuer_account = fields.Char(string='Cuenta libradora')
    instrument_number = fields.Char(string='Número del título')
    electronic_identifier = fields.Char(string='Identificador externo')
    issued_on = fields.Date(string='Fecha de emisión')
    payable_on = fields.Date(string='Fecha de pago / vencimiento')
    note = fields.Text(string='Observaciones')
    state = fields.Selection([('draft', 'Borrador'), ('portfolio', 'En cartera'), ('deposited', 'Depositado, pendiente de acreditación'),
                              ('settled', 'Acreditado'), ('rejected', 'Rechazado'), ('returned', 'Recepción revertida'),
                              ('reserved', 'Reservado para OPA'), ('transferred', 'Entregado a tercero'), ('transferred_closed', 'Entrega con cierre informado'),
                              ('own_issued', 'Propio entregado, pendiente de débito'), ('own_debited', 'Propio debitado'),
                              ('own_returned', 'Propio devuelto'), ('disputed', 'Devuelto, en revisión'),
                              ('canceled', 'Borrador cancelado')], required=True, default='draft', readonly=True, copy=False, index=True)
    event_ids = fields.One2many('arg.pyme.value.event', 'instrument_id', string='Historial', readonly=True, copy=False)
    identity_key = fields.Char(readonly=True, copy=False, index=True)
    _external_identity_unique = models.Constraint('UNIQUE(company_id, identity_key)', 'Este instrumento ya fue registrado en la compañía.')
    _nominal_positive = models.Constraint('CHECK(amount > 0)', 'El importe nominal debe ser positivo.')

    @api.model
    def _currency_for_company(self, company_id):
        company = self.env['res.company'].browse(company_id)
        if company not in self.env.companies:
            raise AccessError(_('Compañía no habilitada.'))
        return (company.arg_default_currency_id or company.currency_id).id

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        if 'currency_id' in fields_list and 'default_currency_id' not in self.env.context:
            company_id = result.get('company_id') or self.env.context.get('default_company_id') or self.env.company.id
            result['currency_id'] = self._currency_for_company(company_id)
        return result

    def _arg_document_code(self):
        self.ensure_one()
        return 'CHQ' if self.instrument_kind == 'cheque' else 'PAG'

    def _arg_value_check(self):
        self.ensure_one()
        self._arg_check_document_access()
        if not self.env.user.has_group('arg_pyme_base.group_administracion'):
            raise AccessError(_('La operación requiere Administración ARG.'))
        self.check_access('write')

    def _arg_value_lock(self):
        self._arg_value_check()
        # The actual row update also makes concurrent REPEATABLE READ edits retry.
        self.flush_recordset()
        self.env.cr.execute(SQL('UPDATE %s SET write_date=clock_timestamp(), write_uid=%s WHERE id=%s',
                                SQL.identifier(self._table), self.env.uid, self.id))
        self.invalidate_recordset()

    @api.model
    def _value_identity(self, vals):
        """Deduplicate only actual identifiers, never a guessed issuer or number."""
        norm = lambda x: re.sub(r'\s+', '', str(x or '')).upper()
        external = norm(vals.get('electronic_identifier'))
        if vals.get('support') == 'electronic' and external:
            raw = ['electronic', vals.get('instrument_kind'), external]
        elif (vals.get('support') == 'paper' and vals.get('instrument_kind') == 'promissory'
              and norm(vals.get('issuer_identifier')) and norm(vals.get('instrument_number')) and vals.get('issued_on')):
            # A promissory note need not have a bank account. Use the actual signer
            # identifier, title number and issue date, never a duplicate-able partner ID.
            signer = re.sub(r'[.\-]', '', norm(vals['issuer_identifier']))
            if re.fullmatch(r'AR\d{11}', signer):
                signer = signer[2:]
            raw = ['paper', 'promissory', signer,
                   norm(vals['instrument_number']), str(fields.Date.to_date(vals['issued_on']))]
        elif (vals.get('support') == 'paper' and vals.get('instrument_kind') == 'cheque' and norm(vals.get('bank_identifier'))
              and norm(vals.get('issuer_account')) and norm(vals.get('instrument_number'))):
            raw = ['paper', 'cheque', norm(vals['bank_identifier']),
                   norm(vals['issuer_account']), norm(vals['instrument_number'])]
        else:
            return False
        import json
        return hashlib.sha256(json.dumps(raw, separators=(',', ':')).encode()).hexdigest()

    @api.model
    def _value_business_fields(self):
        return {'instrument_kind', 'ownership', 'support', 'bank_account_id', 'bank_name', 'bank_identifier', 'issuer_id', 'issuer_account',
                'issuer_identifier', 'issued_on', 'instrument_number', 'electronic_identifier'}

    @api.model
    def _bank_snapshot(self, account_id):
        if not account_id:
            return {}
        account = self.env['res.partner.bank'].browse(account_id).exists()
        if not account:
            raise ValidationError(_('La cuenta bancaria indicada no está disponible.'))
        account.check_access('read')
        return {'bank_name': account.bank_name, 'bank_identifier': account.bank_bic,
                'issuer_account': account.account_number, 'issuer_id': account.partner_id.id}

    @api.onchange('bank_account_id')
    def _onchange_bank_account(self):
        for record in self:
            if record.bank_account_id:
                record.update(record._bank_snapshot(record.bank_account_id.id))
                record._onchange_issuer_identifier()

    @api.onchange('issuer_id')
    def _onchange_issuer_identifier(self):
        for record in self:
            record.issuer_identifier = record.issuer_id.vat or False

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        for vals in vals_list:
            vals = dict(vals)
            if vals.get('company_id') and 'currency_id' not in vals and 'default_currency_id' not in self.env.context:
                vals['currency_id'] = self._currency_for_company(vals['company_id'])
            if {'state', 'event_ids', 'identity_key'} & vals.keys() or any(
                    'default_' + k in self.env.context for k in ('state', 'event_ids', 'identity_key')):
                raise AccessError(_('El estado y el historial se generan desde las acciones del valor.'))
            fields_to_get = list(self._value_business_fields() - vals.keys())
            defaults = self.default_get(fields_to_get)
            account = vals.get('bank_account_id') or defaults.get('bank_account_id')
            if account:
                for key, value in self._bank_snapshot(account).items():
                    if key not in vals and key not in defaults:
                        vals[key] = value
            issuer = vals['issuer_id'] if 'issuer_id' in vals else defaults.get('issuer_id')
            if issuer and 'issuer_identifier' not in vals and 'issuer_identifier' not in defaults:
                partner = self.env['res.partner'].browse(issuer)
                partner.check_access('read')
                vals['issuer_identifier'] = partner.vat or False
            vals['identity_key'] = self._value_identity({**defaults, **vals})
            prepared.append(vals)
        records = super().create(prepared)
        records._validate_value()
        for record in records:
            record._record_draft_event('draft_created', {'nominal': record.amount, 'currency_id': record.currency_id.id})
        return records

    def write(self, vals):
        if {'event_ids', 'identity_key'} & vals.keys():
            raise AccessError(_('El historial y la identidad externa no se editan manualmente.'))
        if 'state' in vals and not value_engine(self.env):
            raise AccessError(_('Use la acción correspondiente para cambiar el estado.'))
        for record in self.sorted('id'):
            record._arg_value_lock()
            if record.state != 'draft' and not value_engine(self.env):
                raise UserError(_('Este registro conserva sus datos; no se edita un valor cancelado.'))
            if 'instrument_kind' in vals and vals['instrument_kind'] != record.instrument_kind:
                raise UserError(_('Cheque y pagaré conservan su identidad. Cree el tipo de documento correspondiente.'))
        # Preserve per-record identity when a multi-record edit changes issuer metadata.
        for record in self:
            update = dict(vals)
            if vals.get('bank_account_id'):
                for key, value in self._bank_snapshot(vals['bank_account_id']).items():
                    update.setdefault(key, value)
            if 'issuer_id' in update and 'issuer_identifier' not in update:
                partner = self.env['res.partner'].browse(update['issuer_id']) if update['issuer_id'] else self.env['res.partner']
                if partner:
                    partner.check_access('read')
                update['issuer_identifier'] = partner.vat if partner else False
            if self._value_business_fields() & update.keys():
                current = {key: (record[key].id if record._fields[key].type == 'many2one' else record[key])
                           for key in self._value_business_fields()}
                update['identity_key'] = self._value_identity({**current, **update})
            super(ValueInstrument, record).write(update)
            record._validate_value()
            if not value_engine(self.env):
                record._record_draft_event('draft_changed', {'fields': sorted(vals)})
        return True

    def unlink(self):
        raise UserError(_('Conserve la identidad y cancele el borrador si no se utilizará.'))

    def copy(self, default=None):
        raise UserError(_('No duplique un título existente. Cree un registro con su propia identificación.'))

    @api.constrains('amount', 'currency_id', 'partner_id', 'issuer_id', 'beneficiary_id', 'company_id',
                    'instrument_kind', 'cheque_type', 'support', 'issued_on', 'payable_on')
    def _validate_value(self):
        for record in self:
            record._arg_value_check()
            if not math.isfinite(record.amount) or record.currency_id.compare_amounts(record.amount, 0) <= 0:
                raise ValidationError(_('Complete un importe nominal positivo en la moneda del título.'))
            for partner in record.partner_id | record.issuer_id | record.beneficiary_id:
                if partner.company_id and partner.company_id != record.company_id:
                    raise ValidationError(_('El tercero pertenece a otra compañía.'))
            if record.instrument_kind == 'cheque' and not record.cheque_type:
                raise ValidationError(_('Seleccione si el cheque es común o de pago diferido.'))
            if record.issued_on and record.payable_on and record.payable_on < record.issued_on:
                raise ValidationError(_('La fecha de pago no puede preceder a la fecha de emisión.'))

    def _record_draft_event(self, kind, payload):
        self._arg_value_check()
        return self.env['arg.pyme.value.event'].with_context(_arg_value_engine=_VALUE_ENGINE).create({
            'instrument_id': self.id, 'kind': kind, 'request_key': str(uuid.uuid4()), 'payload': payload,
        })

    def action_cancel_draft(self):
        self._arg_value_lock()
        if self.state == 'canceled':
            return self._value_action()
        if self.state != 'draft':
            raise UserError(_('La cancelación de borrador no revierte operaciones confirmadas.'))
        self.with_context(_arg_value_engine=_VALUE_ENGINE).write({'state': 'canceled'})
        self._record_draft_event('draft_canceled', {})
        return self._value_action()

    def _value_action(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window', 'name': self.arg_number or _('Valor ARG'),
                'res_model': self._name, 'res_id': self.id, 'view_mode': 'form',
                'views': [(self.env.ref('arg_pyme_valores.value_form').id, 'form')]}

    def _arg_report_payload(self):
        self.ensure_one()
        return {'title': _('Cheque ARG') if self.instrument_kind == 'cheque' else _('Pagaré ARG'),
                'company': self.company_id.name, 'date': str(self.date),
                'partner_name': self.partner_id.name, 'partner_address': self.partner_id.contact_address or '',
                'state_label': dict(self._fields['state']._description_selection(self.env)).get(self.state),
                'external_reference': self.instrument_number or self.electronic_identifier or '',
                'currency': self.currency_id.name,
                'lines': [{'description': _('Importe nominal del título'), 'quantity': 1, 'unit': '',
                           'unit_price': self.amount, 'total': self.amount}],
                'totals': [{'label': _('Nominal'), 'amount': self.amount}],
                'notes': _('Registro de borrador. No acredita recepción, emisión bancaria, cobro ni validez jurídica del título.')}
