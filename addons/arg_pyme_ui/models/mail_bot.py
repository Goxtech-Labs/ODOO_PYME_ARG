from markupsafe import Markup
from odoo import models

class MailBot(models.AbstractModel):
    _inherit = 'mail.bot'

    def _get_style_dict(self):
        values = super()._get_style_dict()
        values['document_link_start'] = Markup('<a href="/arg/ayuda" target="_blank" rel="noopener">')
        return values

    def _get_answer(self, *args, **kwargs):
        answer = super()._get_answer(*args, **kwargs)
        if isinstance(answer, str):
            renamed = answer.replace('OdooBot', 'GOXTECHBOT').replace('Odoobot', 'GOXTECHBOT')
            return Markup(renamed) if isinstance(answer, Markup) else renamed
        return answer
