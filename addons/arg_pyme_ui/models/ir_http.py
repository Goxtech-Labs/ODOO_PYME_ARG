from odoo import models

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super().session_info()
        user = self.env.user
        if user._is_internal():
            result['support_url'] = '/arg/soporte'
            result['arg_pyme'] = {'theme': user.arg_theme, 'density': user.arg_density,
                'root_menu_id': self.env.ref('arg_pyme_base.menu_arg_root').id,
                'config_menu_id': self.env.ref('arg_pyme_base.menu_arg_config').id,
                'areas': [{'id': self.env.ref('arg_pyme_base.menu_arg_' + key).id, 'name': label}
                          for key, label in [('ventas','Ventas'),('compras','Compras'),('stock','Stock'),
                                              ('administracion','Administración'),('informes','Informes')]]}
        return result
