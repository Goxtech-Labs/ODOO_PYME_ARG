from pathlib import Path
from odoo import api, models
from odoo.tools.binary import BinaryBytes
from odoo.exceptions import AccessError

class Branding(models.AbstractModel):
    _name = 'arg.pyme.ui.branding'
    _description = 'Identidad visual ARG'

    @api.model
    def _apply_identity(self):
        if not self.env.su:
            raise AccessError('La identidad se aplica desde instalación o migración autorizada.')
        bot = self.env.ref('base.partner_root')
        avatar = Path(__file__).parents[1] / 'static/img/goxtechbot.png'
        values = {'name': 'GOXTECHBOT'}
        if avatar.is_file():values['image_1920'] = BinaryBytes(avatar.read_bytes(), filename='goxtechbot.png')
        bot.with_context(tracking_disable=True, mail_notrack=True).write(values)
