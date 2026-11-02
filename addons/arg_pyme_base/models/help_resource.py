import re
from urllib.parse import urlsplit
from odoo import release
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class HelpResource(models.Model):
    _name = 'arg.pyme.help.resource'
    _description = 'Manual y tutorial ARG'
    _order = 'module_key, sequence, id'

    name = fields.Char(required=True, string='Título')
    module_key = fields.Char(required=True, index=True, string='Módulo')
    task = fields.Char(string='Tarea')
    sequence = fields.Integer(default=10)
    version_min = fields.Char(default='20.0', string='Versión mínima')
    version_max = fields.Char(string='Versión máxima')
    url = fields.Char(string='Video o lista de YouTube')
    manual_url = fields.Char(string='Manual alternativo')
    manual_text = fields.Html(string='Guía escrita', sanitize=True)
    state = fields.Selection([('planned','Planeado'),('current','Vigente'),('review','Por revisar'),('replaced','Reemplazado')], default='planned', required=True, string='Estado')
    is_compatible = fields.Boolean(compute='_compute_compatible', string='Compatible con esta instalación')
    review_date = fields.Date(string='Última revisión')
    reviewer_id = fields.Many2one('res.users', string='Responsable')
    replacement_id = fields.Many2one('arg.pyme.help.resource', string='Reemplazo', ondelete='set null')
    active = fields.Boolean(default=True)

    @api.depends('version_min', 'version_max')
    def _compute_compatible(self):
        current = tuple(release.version_info[:2])
        for rec in self:
            lower = tuple(map(int, rec.version_min.split('.'))) if rec.version_min and re.fullmatch(r'[0-9]+\.[0-9]+', rec.version_min) else (0, 0)
            upper = tuple(map(int, rec.version_max.split('.'))) if rec.version_max and re.fullmatch(r'[0-9]+\.[0-9]+', rec.version_max) else (999, 0)
            rec.is_compatible = lower <= current <= upper

    @api.constrains('version_min', 'version_max')
    def _check_versions(self):
        for rec in self:
            for value in (rec.version_min, rec.version_max):
                if value and not re.fullmatch(r'[0-9]+\.[0-9]+', value):
                    raise ValidationError(_('Indicá la versión Odoo como mayor.menor, por ejemplo 20.0.'))
            if rec.version_min and rec.version_max and tuple(map(int, rec.version_min.split('.'))) > tuple(map(int, rec.version_max.split('.'))):
                raise ValidationError(_('La versión máxima no puede ser anterior a la mínima.'))

    @api.constrains('url', 'manual_url', 'state', 'replacement_id')
    def _check_links(self):
        for rec in self:
            if rec.url:
                url = urlsplit(rec.url)
                if url.scheme != 'https' or url.hostname not in {'youtube.com','www.youtube.com','youtu.be','m.youtube.com'} or url.username or url.password:
                    raise ValidationError(_('Usá una URL HTTPS válida de YouTube.'))
            if rec.manual_url and not rec.manual_url.startswith('/arg/'):
                url = urlsplit(rec.manual_url)
                if url.scheme != 'https' or not url.hostname or url.username or url.password:
                    raise ValidationError(_('El manual debe usar HTTPS o una ruta interna /arg/.'))
            if rec.replacement_id == rec:
                raise ValidationError(_('Un recurso no puede reemplazarse a sí mismo.'))
            if rec.state == 'current' and not (rec.url or rec.manual_url or rec.manual_text):
                raise ValidationError(_('Agregá el video o una guía antes de marcar el recurso vigente.'))

    def action_open_video(self):
        self.ensure_one();self.check_access('read')
        if self.state != 'current' or not self.url or not self.is_compatible:
            raise UserError(_('No hay un video vigente. Consultá el manual escrito.'))
        return {'type': 'ir.actions.act_url', 'url': self.url, 'target': 'new'}
