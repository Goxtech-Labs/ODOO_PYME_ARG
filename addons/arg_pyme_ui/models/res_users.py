from odoo import api, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    def _arg_set_default_home(self):
        operator = self.env.ref('arg_pyme_base.group_operator')
        home = self.env.ref('arg_pyme_ui.action_arg_home', raise_if_not_found=False)
        if home:
            for user in self:
                if not user.share and operator in user.all_group_ids and not user.action_id:
                    user.action_id = home.id

    @api.model_create_multi
    def create(self, values_list):
        users = super().create(values_list)
        users._arg_set_default_home()
        return users

    def write(self, values):
        result = super().write(values)
        if 'group_ids' in values:
            self._arg_set_default_home()
        return result
