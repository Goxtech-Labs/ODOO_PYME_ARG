import hashlib
import json
import uuid
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError, UserError


_VALUE_ENGINE = object()


def value_engine(env):
    return env.context.get('_arg_value_engine') is _VALUE_ENGINE


class ValueEvent(models.Model):
    _name = 'arg.pyme.value.event'
    _description = 'Evidencia de un valor ARG'
    _order = 'id desc'
    _check_company_auto = True

    instrument_id = fields.Many2one('arg.pyme.value.instrument', required=True, ondelete='restrict', index=True)
    company_id = fields.Many2one(related='instrument_id.company_id', store=True)
    actor_id = fields.Many2one('res.users', required=True, readonly=True, ondelete='restrict')
    recorded_at = fields.Datetime(required=True, readonly=True)
    kind = fields.Selection([
        ('draft_created', 'Borrador creado'), ('draft_changed', 'Borrador modificado'),
        ('draft_canceled', 'Borrador cancelado'),
        ('received', 'Recibido por REC'), ('deposited', 'Depósito registrado'),
        ('settled', 'Acreditación registrada'), ('rejected', 'Rechazo con reversión'),
        ('receipt_reversed', 'Recepción revertida'),
    ], required=True, readonly=True)
    request_key = fields.Char(required=True, readonly=True)
    fingerprint = fields.Char(required=True, readonly=True)
    payload = fields.Json(readonly=True)
    _event_key_unique = models.Constraint('UNIQUE(instrument_id, request_key)', 'La operación de este valor ya está registrada.')

    @api.model_create_multi
    def create(self, vals_list):
        if not value_engine(self.env):
            raise AccessError(_('La evidencia del valor sólo se genera desde su operación autorizada.'))
        prepared = []
        for vals in vals_list:
            vals = dict(vals)
            if {'company_id', 'actor_id', 'recorded_at', 'fingerprint'} & vals.keys():
                raise AccessError(_('Autor, fecha, compañía y huella de evidencia se asignan en servidor.'))
            instrument = self.env['arg.pyme.value.instrument'].browse(vals.get('instrument_id')).exists()
            if not instrument:
                raise ValidationError(_('Falta el valor al que pertenece esta evidencia.'))
            instrument._arg_value_check()
            if vals.get('kind') not in self._fields['kind'].get_values(self.env):
                raise ValidationError(_('Tipo de evidencia no disponible.'))
            try:
                vals['request_key'] = str(uuid.UUID(vals.get('request_key', '')))
                canonical = json.dumps({'kind': vals['kind'], 'payload': vals.get('payload') or {}},
                                       sort_keys=True, separators=(',', ':'), allow_nan=False)
            except (ValueError, TypeError, AttributeError):
                raise ValidationError(_('La referencia o contenido de evidencia no es válido.'))
            vals.update(actor_id=self.env.uid, recorded_at=fields.Datetime.now(),
                        fingerprint=hashlib.sha256(canonical.encode()).hexdigest())
            prepared.append(vals)
        clean = {k: v for k, v in self.env.context.items() if not k.startswith('default_')}
        return super(ValueEvent, self.with_context(clean)).create(prepared)

    def write(self, vals):
        raise UserError(_('La evidencia de valores es inmutable.'))

    def unlink(self):
        raise UserError(_('La evidencia de valores se conserva.'))
