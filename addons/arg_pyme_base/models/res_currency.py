import math
from odoo import fields, models, _
from odoo.exceptions import AccessError, UserError


class Currency(models.Model):
    _inherit='res.currency'

    def _arg_require_conversion(self,other,company,date):
        """Require an explicit company rate selected by the native engine; never accept its implicit 1 fallback."""
        self.ensure_one();other.ensure_one();company.ensure_one()
        if company not in self.env.companies:raise AccessError(_('Compañía no habilitada para la cotización.'))
        if self==other:return {}
        day=fields.Date.to_date(date)
        rates=(self|other)._get_rates(company,day)
        evidence={}
        for currency in self|other:
            if currency==company.currency_id:continue
            rate,rate_date=rates[currency.id]
            explicit=self.env['res.currency.rate'].search([
                ('currency_id','=',currency.id),('company_id','=',company.root_id.id),('name','=',rate_date)],limit=1) if rate_date else self.env['res.currency.rate']
            if (not explicit or rate_date>day or not math.isfinite(rate) or rate<=0
                    or not math.isclose(explicit.rate,rate,rel_tol=1e-10,abs_tol=1e-12)):
                raise UserError(_('Falta una cotización propia vigente y efectiva para %(currency)s en esta compañía y fecha.',currency=currency.name))
            evidence[str(currency.id)]={'rate_id':explicit.id,'date':str(rate_date),'native_rate':rate}
        return evidence
