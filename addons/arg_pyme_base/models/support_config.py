import re
from urllib.parse import urlsplit
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    arg_support_channel = fields.Selection([('none','Sin configurar'),('email','Correo'),('whatsapp','WhatsApp'),('tickets','Tickets')], default='none', config_parameter='arg_pyme.support.channel', string='Canal principal ARG')
    arg_support_email = fields.Char(config_parameter='arg_pyme.support.email', string='Correo de soporte')
    arg_support_whatsapp = fields.Char(config_parameter='arg_pyme.support.whatsapp', string='WhatsApp (formato internacional)')
    arg_support_tickets = fields.Char(config_parameter='arg_pyme.support.tickets', string='URL de tickets')

    @api.constrains('arg_support_email', 'arg_support_whatsapp', 'arg_support_tickets', 'arg_support_channel')
    def _check_arg_support(self):
        for rec in self:
            if rec.arg_support_email and not re.fullmatch(r'[^\s@?&#]+@[^\s@?&#]+\.[^\s@?&#]+', rec.arg_support_email):
                raise ValidationError(_('Revisá el correo de soporte.'))
            if rec.arg_support_whatsapp and not re.fullmatch(r'\+?[1-9][0-9]{7,14}', rec.arg_support_whatsapp):
                raise ValidationError(_('Usá el número internacional, sólo dígitos y + opcional.'))
            if rec.arg_support_tickets:
                url = urlsplit(rec.arg_support_tickets)
                if url.scheme != 'https' or not url.hostname or url.username or url.password:
                    raise ValidationError(_('El sistema de tickets debe usar HTTPS sin credenciales en la URL.'))
            field = {'email':'arg_support_email','whatsapp':'arg_support_whatsapp','tickets':'arg_support_tickets'}.get(rec.arg_support_channel)
            if field and not rec[field]:
                raise ValidationError(_('Completá el destino del canal principal o elegí Sin configurar.'))
