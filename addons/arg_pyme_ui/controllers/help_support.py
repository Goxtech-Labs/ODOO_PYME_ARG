import re
from urllib.parse import quote, urlsplit
from werkzeug.exceptions import Forbidden
from odoo import http, release
from odoo.http import request

class HelpSupport(http.Controller):
    def _project_links(self):
        params = request.env['ir.config_parameter'].sudo()
        result = {}
        for key, parameter in [('project_website', 'arg_pyme.project.website'), ('youtube_channel', 'arg_pyme.help.youtube_channel')]:
            value = params.get_str(parameter, '')
            try:
                url = urlsplit(value)
                url.port  # Ignore a malformed parameter instead of emitting its link.
                valid = (url.scheme == 'https' and bool(url.hostname) and url.username is None
                         and url.password is None and not any(character.isspace() or ord(character) < 32 for character in value))
                if key == 'youtube_channel':
                    valid = valid and url.hostname in {'youtube.com', 'www.youtube.com', 'm.youtube.com'}
            except ValueError:
                valid = False
            result[key] = value if valid else False
        return result

    def _require_internal(self):
        if not request.env.user._is_internal():raise Forbidden()

    @http.route('/arg/soporte', type='http', auth='user', methods=['GET'])
    def support(self, **kwargs):
        self._require_internal()
        params = request.env['ir.config_parameter'].sudo()
        email = params.get_str('arg_pyme.support.email', '')
        phone = params.get_str('arg_pyme.support.whatsapp', '')
        tickets = params.get_str('arg_pyme.support.tickets', '')
        return request.render('arg_pyme_ui.support_page', {
            **self._project_links(),
            'support_email': email, 'email_url': 'mailto:' + quote(email, safe='@.+') if email else False,
            'whatsapp_url': 'https://wa.me/' + phone.lstrip('+') if phone else False,
            'tickets_url': tickets, 'primary': params.get_str('arg_pyme.support.channel', 'none')})

    @http.route('/arg/ayuda', type='http', auth='user', methods=['GET'])
    def help(self, module=None, **kwargs):
        self._require_internal()
        if module and not re.fullmatch(r'arg_pyme_[a-z0-9_]+', module):module = None
        domain = [('module_key','=',module)] if module else []
        resources = request.env['arg.pyme.help.resource']
        records = resources.search(domain) if request.env.user.has_group('arg_pyme_base.group_operator') else resources.browse()
        return request.render('arg_pyme_ui.help_page', {**self._project_links(), 'resources': records, 'module_key':module})

    @http.route('/arg/acerca', type='http', auth='user', methods=['GET'])
    def about(self, **kwargs):
        self._require_internal()
        return request.render('arg_pyme_ui.about_page', {**self._project_links(), 'odoo_version': release.version})
