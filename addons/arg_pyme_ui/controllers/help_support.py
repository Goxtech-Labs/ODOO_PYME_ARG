import re
from urllib.parse import quote
from werkzeug.exceptions import Forbidden
from odoo import http, release
from odoo.http import request

class HelpSupport(http.Controller):
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
        return request.render('arg_pyme_ui.help_page', {'resources': records, 'module_key':module})

    @http.route('/arg/acerca', type='http', auth='user', methods=['GET'])
    def about(self, **kwargs):
        self._require_internal()
        return request.render('arg_pyme_ui.about_page', {'odoo_version': release.version})
