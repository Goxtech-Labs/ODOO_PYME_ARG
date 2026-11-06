"""Transaction-bound state for replenishment; never an RPC authorization flag."""
import hashlib
import json
import uuid

from odoo import _
from odoo.exceptions import AccessError, ValidationError


_CONTEXT_KEY = '_arg_replenishment_run'
_REFERENCE_MODELS = frozenset({
    'res.company', 'res.users', 'res.partner', 'res.currency',
    'product.product', 'product.template', 'product.supplierinfo', 'uom.uom',
    'stock.warehouse', 'stock.location', 'stock.route', 'stock.rule',
    'stock.warehouse.orderpoint', 'stock.picking', 'stock.move', 'stock.move.line',
    'purchase.order', 'purchase.order.line', 'mrp.bom', 'mrp.bom.line',
    'mrp.production', 'mrp.workorder', 'mrp.workcenter',
})


def canonical_json(value):
    try:
        return json.dumps(value, sort_keys=True, separators=(',', ':'),
                          ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError, OverflowError, RecursionError) as error:
        raise ValidationError(_('Los datos de reposición no son válidos.')) from error


def json_hash(value):
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def operation_key(value):
    if not isinstance(value, str):
        raise ValidationError(_('La confirmación necesita una clave de operación válida.'))
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError) as error:
        raise ValidationError(_('La confirmación necesita una clave de operación válida.')) from error
    if str(parsed) != value or parsed.int == 0:
        raise ValidationError(_('La confirmación necesita una clave de operación válida.'))
    return value


def check_references(env, references):
    """Validate the CURRENT recipient, including field permissions, before any output.

    The manifest contains both ends of every relation and every field whose
    historical data is returned. It must be populated by the server adapters.
    Never read a hidden business record with sudo to make a receipt readable.
    """
    if env.su:
        raise AccessError(_('Valide el resultado con los permisos actuales del solicitante.'))
    if not isinstance(references, list) or not references:
        raise AccessError(_('El resultado de reposición no está disponible con sus permisos actuales.'))
    for reference in references:
        if not isinstance(reference, dict) or set(reference) != {'model', 'id', 'fields'}:
            raise AccessError(_('El resultado de reposición no está disponible con sus permisos actuales.'))
        model, identifier, names = (reference[name] for name in ('model', 'id', 'fields'))
        if (not isinstance(model, str) or model not in _REFERENCE_MODELS or model not in env.registry
                or type(identifier) is not int or identifier <= 0
                or not isinstance(names, list) or not names
                or any(not isinstance(name, str) for name in names)):
            raise AccessError(_('El resultado de reposición no está disponible con sus permisos actuales.'))
        record = env[model].browse(identifier)
        try:
            record.check_access('read')
            if not record.exists():
                raise AccessError(_('Referencia no disponible.'))
            for name in names:
                if name not in record._fields:
                    raise AccessError(_('Dimensión no disponible.'))
                record.check_field_access(record._fields[name], 'read')
            if model != 'res.users' and 'company_id' in record._fields:
                record.check_field_access(record._fields['company_id'], 'read')
                if record.company_id and record.company_id != env.company:
                    raise AccessError(_('Compañía no disponible.'))
        except AccessError as error:
            raise AccessError(_('El resultado de reposición no está disponible con sus permisos actuales.')) from error


class _ReplenishmentRun:
    """Hashable private context object, tied to one cursor and original actor.

    Persistent data uses JSON snapshots. Native adapters share this object only
    while that transaction is running; JSON sent by a client cannot construct it.
    Finalization belongs to the orchestrator, AFTER native postconditions pass.
    """

    def __init__(self, env, key, payload, proposal):
        if env.su:
            raise AccessError(_('Inicie la reposición con los permisos del solicitante.'))
        self.cursor = env.cr
        self.database = env.cr.dbname
        self.actor_id = env.uid
        self.company_id = env.company.id
        self.operation_key = operation_key(key)
        self.payload_json = canonical_json(payload)
        self.proposal_json = canonical_json(proposal)
        self.payload_hash = hashlib.sha256(self.payload_json.encode()).hexdigest()
        self.proposal_hash = hashlib.sha256(self.proposal_json.encode()).hexdigest()
        self._references = {}
        self._events = []
        self._evidence_json = None

    def reference(self, record, names):
        if self._evidence_json is not None:
            raise AccessError(_('La evidencia de reposición ya está cerrada.'))
        record.ensure_one()
        if record._name not in _REFERENCE_MODELS or type(record.id) is not int or record.id <= 0:
            raise ValidationError(_('La referencia de reposición no es persistente o no está admitida.'))
        names = list(names)
        reference = {'model': record._name, 'id': record.id, 'fields': names}
        actor_env = record.with_user(self.actor_id).sudo(False).with_context({
            'allowed_company_ids': [self.company_id],
        }).env
        check_references(actor_env, [reference])
        self._references.setdefault((record._name, record.id), set()).update(names)

    def event(self, value):
        if self._evidence_json is not None:
            raise AccessError(_('La evidencia de reposición ya está cerrada.'))
        self._events.append(json.loads(canonical_json(value)))

    def finish(self, summary):
        if self._evidence_json is not None or not self._events or not self._references:
            raise ValidationError(_('La reposición necesita resultados nativos verificados.'))
        self._evidence_json = canonical_json({
            'summary': summary,
            'events': self._events,
            'references': [
                {'model': model, 'id': identifier, 'fields': sorted(names)}
                for (model, identifier), names in sorted(self._references.items())
            ],
        })

    def material(self):
        if self._evidence_json is None:
            raise AccessError(_('La reposición todavía no tiene un resultado verificado.'))
        return {
            'company_id': self.company_id,
            'actor_id': self.actor_id,
            'operation_key': self.operation_key,
            'payload_hash': self.payload_hash,
            'proposal_hash': self.proposal_hash,
            'payload': json.loads(self.payload_json),
            'proposal': json.loads(self.proposal_json),
            'evidence': json.loads(self._evidence_json),
        }


def current_run(env, required=False):
    value = env.context.get(_CONTEXT_KEY)
    if value is None and not required:
        return None
    if (not isinstance(value, _ReplenishmentRun) or value.cursor is not env.cr
            or value.database != env.cr.dbname or value.company_id != env.company.id):
        raise AccessError(_('El contexto de reposición no es válido para esta transacción.'))
    return value
