"""Private immutable execution receipt; no management ACL on raw evidence.

    Validated service representations will be the user entry point. Native
    documents retain quantities, prices, states and their actual business effects.
"""
from odoo import api, fields, models, _
from odoo.exceptions import AccessError

from ..tools.replenishment import current_run, check_references


class ReplenishmentOperation(models.Model):
    _name = 'arg.pyme.replenishment.operation'
    _description = 'Evidencia técnica de reposición ARG'
    _rec_name = 'operation_key'
    _order = 'id desc'
    _check_company_auto = True

    company_id = fields.Many2one('res.company', required=True, readonly=True, ondelete='restrict')
    actor_id = fields.Many2one('res.users', required=True, readonly=True, ondelete='restrict')
    operation_key = fields.Char(required=True, readonly=True, copy=False)
    payload_hash = fields.Char(required=True, readonly=True, copy=False)
    proposal_hash = fields.Char(required=True, readonly=True, copy=False)
    confirmed_at = fields.Datetime(required=True, readonly=True, default=fields.Datetime.now)
    payload = fields.Json(required=True, readonly=True, copy=False)
    proposal = fields.Json(required=True, readonly=True, copy=False)
    evidence = fields.Json(required=True, readonly=True, copy=False)

    _operation_unique = models.Constraint(
        'UNIQUE(company_id, operation_key)', 'La confirmación de reposición ya fue registrada.')

    @api.model_create_multi
    def create(self, vals_list):
        run = current_run(self.env, required=True)
        if not self.env.su or len(vals_list) != 1 or vals_list[0]:
            raise AccessError(_('La evidencia sólo se crea desde una confirmación validada.'))
        material = run.material()
        actor_model = self.with_user(run.actor_id).sudo(False).with_context({
            'allowed_company_ids': [run.company_id],
        })
        actor_model.env['arg.pyme.stock.matrix']._authorize()
        if not actor_model.env.user.has_group('arg_pyme_base.group_manager'):
            raise AccessError(_('Confirmar reposición requiere responsable ARG.'))
        check_references(actor_model.env, material['evidence']['references'])
        # Do not accept defaults from caller context or ir.default for receipt
        # material. The timestamp is created here, not supplied over RPC.
        material['confirmed_at'] = fields.Datetime.now()
        return super().create([material])

    def write(self, values):
        raise AccessError(_('La evidencia de reposición es inmutable.'))

    def unlink(self):
        raise AccessError(_('La evidencia de reposición se conserva.'))

    def copy(self, default=None):
        raise AccessError(_('Una confirmación de reposición no se duplica.'))

    def copy_data(self, default=None):
        raise AccessError(_('La evidencia no se copia ni se exporta por este método.'))
