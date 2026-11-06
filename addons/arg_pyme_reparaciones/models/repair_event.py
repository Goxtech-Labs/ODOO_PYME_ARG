import uuid
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError


_REPAIR_ENGINE = object()


def repair_engine(record):
    # Defaults of the calling action must not enter an internal evidence factory.
    context = {key: value for key, value in record.env.context.items()
               if not key.startswith('default_') and key != 'accrual_entry_date'}
    return record.with_context(context, _arg_repair_engine=_REPAIR_ENGINE)


class RepairEvent(models.Model):
    _name = 'arg.pyme.repair.event'
    _description = 'Hecho de recepción / diagnóstico ARG'
    _order = 'id desc'
    _check_company_auto = True

    case_id = fields.Many2one('arg.pyme.repair.case', required=True, ondelete='restrict', index=True, check_company=True)
    company_id = fields.Many2one(related='case_id.company_id', store=True, index=True)
    kind = fields.Selection([('receive', 'Recepción'), ('diagnose', 'Diagnóstico registrado'),
                             ('cancel', 'Borrador cancelado'), ('return', 'Devolución sin reparación'),
                             ('authorize', 'Trabajo autorizado'), ('start', 'Trabajo iniciado'),
                             ('order', 'Pedido vinculado'),
                             ('ready', 'Trabajo listo'), ('resume', 'Trabajo retomado'),
                             ('deliver', 'Equipo reparado entregado'), ('work_correction', 'Trabajo corregido'),
                             ('receipt_correction', 'Datos de recepción corregidos'),
                             ('diagnosis_correction', 'Diagnóstico rectificado'), ('followup', 'Nueva visita preparada')],
                            required=True)
    request_key = fields.Char(required=True, default=lambda self: uuid.uuid4().hex, copy=False, index=True)
    order_id = fields.Many2one('sale.order', check_company=True, ondelete='restrict', readonly=True,
                               string='Pedido vinculado')
    related_case_id = fields.Many2one('arg.pyme.repair.case', check_company=True, ondelete='restrict',
                                      readonly=True, string='Seguimiento preparado')
    effective_date = fields.Date(required=True, string='Fecha del hecho')
    recorded_at = fields.Datetime(required=True, default=fields.Datetime.now, string='Registrado el')
    actor_id = fields.Many2one('res.users', required=True, default=lambda self: self.env.user,
                               ondelete='restrict', string='Registrado por')
    evidence = fields.Json(required=True, string='Constancia')
    _request_unique = models.Constraint('UNIQUE(case_id, request_key)', 'Esta operación ya fue registrada en el parte.')

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('_arg_repair_engine') is not _REPAIR_ENGINE:
            raise AccessError(_('El historial se crea desde las acciones del parte.'))
        return super().create(vals_list)

    def write(self, values):
        raise UserError(_('El historial del parte se conserva sin modificaciones.'))

    def unlink(self):
        raise UserError(_('El historial del parte no se elimina.'))
