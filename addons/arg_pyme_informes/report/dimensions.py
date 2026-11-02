import math
from collections import defaultdict
from markupsafe import Markup
from odoo.tools.misc import formatLang
from .number_format import decimal_digits, numeric_value
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError
from .facts import SOURCES

COLUMNS = [('day','Fecha'), ('document','Documento'), ('original','Origen / contrapartida'),
 ('partner','Tercero'), ('product','Producto'), ('location','Ubicación'), ('flow','Hecho físico'),
 ('description','Detalle'), ('state','Estado propio'), ('progress','Avance documental'),
 ('quantity','Cantidad'), ('unit','Unidad'), ('reserved','Reservado'), ('available','Disponible'),
 ('net','Neto'), ('tax','Impuesto por línea'), ('total','Importe')]
NUMERIC = {'quantity','reserved','available','net','tax','total'}


def total_values(rows):
    return {key:math.fsum(row[key] for row in rows if row[key] is not None) if any(row[key] is not None for row in rows) else None for key in NUMERIC}


class ReportDimensions(models.AbstractModel):
    _inherit = 'arg.pyme.report.engine'

    def _snapshot(self, wizard):
        wizard._validate_query()
        rows = self._collect(wizard)
        # Currency is fixed by the query. Quantity totals always retain native UoM (and physical flow).
        buckets = defaultdict(list)
        for row in rows:
            key = (row['flow'], row['unit_id'], row['unit'])
            buckets[key].append(row)
        totals = []
        for key, part in buckets.items():
            values = total_values(part)
            if any(values[k] is not None for k in ('quantity','reserved','available')):
                totals.append({'flow':key[0], 'unit':key[2], 'unit_rounding':part[0]['unit_rounding'], **{k:(None if k in ('net','tax','total') else v) for k,v in values.items()}})
        money = total_values(rows)
        if any(money[k] is not None for k in ('net','tax','total')):
            totals.append({'flow':_('Total monetario'), 'unit':'', **{k:(v if k in ('net','tax','total') else None) for k,v in money.items()}})
        if wizard.group_by != 'none':
            grouped = defaultdict(list)
            for row in rows:
                # Group by identity, not a potentially duplicated display label.
                key = (row.get(wizard.group_by+'_key', row[wizard.group_by]), row['unit_id'], row['unit'], row['flow'])
                grouped[key].append(row)
            visible = []
            for key, part in grouped.items():
                visible.append({'dimension':part[0][wizard.group_by] or _('Sin dato'), 'flow':key[3], 'unit':key[2],
                    'unit_rounding':part[0]['unit_rounding'], 'count':len(part), **total_values(part)})
            visible.sort(key=lambda row:(str(row['dimension']),str(row['unit']),str(row['flow'])))
            columns = [('dimension',_('Agrupación')), ('flow',_('Hecho físico')), ('count',_('Filas fuente')),
                       ('quantity',_('Cantidad')), ('unit',_('Unidad')), ('reserved',_('Reservado')), ('available',_('Disponible')),
                       ('net',_('Neto')), ('tax',_('Impuesto por línea')), ('total',_('Importe'))]
        else:
            visible = rows
            columns = list(COLUMNS)
        columns = [(key,_(label)) for key,label in columns if key in ('day','document','dimension','count') or any(row.get(key) is not None and row.get(key) != '' for row in visible)]
        # Aggregate raw values first; format once at the currency/unit precision for all outputs.
        quantity_digits = self.env['decimal.precision'].precision_get('Product Unit')
        for row in visible + totals:
            row['display_values'] = {}
            row['export_values'] = {}
            for key in NUMERIC:
                value = row.get(key)
                if value is None:
                    continue
                rounding = wizard.currency_id.rounding if key in ('net', 'tax', 'total') else row.get('unit_rounding')
                if not rounding or not math.isfinite(rounding) or rounding <= 0:
                    raise ValidationError(_('No se pudo determinar la precisión de la moneda o unidad del resultado.'))
                rounded, digits, canonical = (numeric_value(value, rounding=rounding) if key in ('net', 'tax', 'total')
                                               else numeric_value(value, digits=max(quantity_digits, decimal_digits(rounding))))
                row['display_values'][key] = formatLang(self.env, rounded, digits=digits, rounding_method='HALF-UP')
                row['export_values'][key] = canonical
        now = fields.Datetime.now()
        meta = SOURCES[wizard.source]
        note = _('Neto/impuesto/total corresponden a las líneas seleccionadas; no incluyen líneas de redondeo ni reconstruyen el total fiscal de cabecera.') if wizard.source in ('sales','purchases','sale_orders','purchase_orders') else ''
        if wizard.source in ('customer_debt','supplier_debt'):
            note = _('Saldo residual actual, filtrado por vencimiento. No es saldo histórico al fin del período.')
        elif wizard.source == 'applications':
            note = _('Conciliaciones vigentes en moneda de compañía; una aplicación contable no acredita dinero. Las eliminadas se consultan en historial ARG, no son aplicaciones vigentes.')
        elif wizard.source == 'cash':
            note = _('Entradas positivas y salidas negativas en cuentas de liquidez publicadas; sin repetir por facturas o aplicaciones. Cuentas transitorias excluidas.')
        elif wizard.source == 'stock_at':
            note = _('Desde el inicio del historial hasta fin de la fecha final en su zona horaria. Fecha inicial ignorada; sin reservas históricas ni valoración. Sólo productos actualmente almacenables y ubicaciones internas propias; cambios históricos de clasificación o compañía requieren revisión. Usa quantity_product_uom nativo en unidad base; conserva cada extremo interno y vínculo al movimiento.')
        elif wizard.source == 'stock_now':
            note = _('Existencia física actual y reservas actuales. El período no filtra quants. No es existencia histórica ni valoración monetaria.')
        elif wizard.source == 'movements':
            note = _('Cantidad por circuito físico: entregas/recepciones positivas y sus retornos negativos. Transferencias y otros movimientos indican origen/destino; no sumar circuitos como variación de stock.')
        return {'title':_(meta[0]), 'grain':_(meta[2]), 'date_basis':_(meta[3]), 'source_model':meta[1],
                'company':self._label(wizard.company_id), 'currency':self._label(wizard.currency_id) if meta[4] else '',
                'from':str(wizard.date_from), 'to':str(wizard.date_to), 'timezone':self._timezone(wizard),
                'generated_at':str(now)+' UTC', 'partner':self._label(wizard.partner_id),
                'product_filter':wizard.product_query or '', 'location_filter':wizard.location_query or '',
                'group_by':dict(wizard._fields['group_by']._description_selection(self.env))[wizard.group_by],
                'rows':visible, 'columns':columns, 'totals':totals, 'source_count':len(rows), 'result_count':len(visible),
                'note':note, 'demo':bool(getattr(wizard.company_id,'arg_demo_mode',False))}

    def _html(self, data, page):
        start = page*50
        if start >= data['result_count'] and page:
            raise ValidationError(_('La página quedó fuera del resultado. Volvé a la primera página.'))
        text = Markup('<div class="arg_report_result"><p><strong>%s</strong> · %s · %s</p><p>%s → %s · %s · %s</p><p>%s · %s · %s</p><p>%s</p>') % (
            data['title'],data['company'],data['currency'],data['from'],data['to'],data['timezone'],data['generated_at'],
            data['grain'],data['source_model'],data['date_basis'],data['note'])
        text += Markup('<p>%s registros fuente · %s filas · página %s</p><div class="table-responsive"><table class="table table-sm table-striped"><thead><tr>') % (data['source_count'],data['result_count'],page+1)
        for key,label in data['columns']:text += Markup('<th>%s</th>') % label
        text += Markup('</tr></thead><tbody>')
        for row in data['rows'][start:start+50]:
            text += Markup('<tr>')
            for key,label in data['columns']:
                value = row.get(key)
                if value is None: value = ''
                if key in NUMERIC and value != '': value = row['display_values'][key]
                link = row.get('source_url') if key == 'document' else row.get('original_url') if key == 'original' else None
                text += (Markup('<td><a href="%s" target="_blank" rel="noopener">%s</a></td>') % (link,value)) if link else Markup('<td>%s</td>') % value
            text += Markup('</tr>')
        text += Markup('</tbody></table></div><p>Totales del corte completo (no sólo esta página), separados por unidad y hecho físico:</p><ul>')
        for total in data['totals']:
            values = ' · '.join(key+': '+total['display_values'][key] for key in sorted(NUMERIC) if total[key] is not None)
            text += Markup('<li>%s · %s · %s</li>') % (total['flow'],total['unit'],values)
        if not data['rows']:text += Markup('<li>Sin registros para este corte.</li>')
        return text+Markup('</ul></div>')


class ReportQuery(models.TransientModel):
    _name = 'arg.pyme.report.query'
    _description = 'Consulta de informes ARG'
    _check_company_auto = True

    def _sources(self):
        return self.env['arg.pyme.report.engine']._available()

    source = fields.Selection(selection='_sources', string='Hecho', default=lambda s:next(iter(s._sources()),(False,))[0])
    company_id = fields.Many2one('res.company',string='Compañía',required=True,default=lambda s:s.env.company)
    currency_id = fields.Many2one('res.currency',string='Moneda de importes',default=lambda s:s.env.company.currency_id)
    date_from = fields.Date(string='Desde',required=True,default=lambda s:fields.Date.context_today(s).replace(day=1))
    date_to = fields.Date(string='Hasta / corte',required=True,default=fields.Date.context_today)
    partner_id = fields.Many2one('res.partner',string='Tercero',check_company=True)
    product_query = fields.Char(string='Producto contiene')
    location_query = fields.Char(string='Ubicación contiene')
    group_by = fields.Selection([('none','Detalle'),('day','Fecha'),('document','Documento'),('partner','Tercero'),('product','Producto'),('location','Ubicación'),('state','Estado propio')],required=True,default='none',string='Ver por')
    page_number = fields.Integer(string='Página interna',default=0)
    result_html = fields.Html(string='Resultado',compute='_compute_result',sanitize=True,compute_sudo=False)

    def _validate_query(self):
        self.ensure_one()
        engine = self.env['arg.pyme.report.engine'];engine._authorize()
        if isinstance(self.id,int):
            self.check_access('read')
        if self.company_id not in self.env.companies:
            raise AccessError(_('La compañía no está habilitada.'))
        self.company_id.read(['display_name','currency_id'])
        if self.source not in dict(engine._available()):
            raise AccessError(_('Hecho no disponible: requiere el módulo y permiso de lectura de su fuente.'))
        if not self.date_from or not self.date_to or self.date_from > self.date_to:
            raise ValidationError(_('Seleccione un período válido.'))
        if SOURCES[self.source][4] and not self.currency_id:
            raise ValidationError(_('Seleccione una moneda única para los importes.'))
        if self.currency_id:self.currency_id.read(['display_name','rounding'])
        if self.partner_id:
            self.partner_id.read(['display_name','company_id'])
            if self.partner_id.company_id and self.partner_id.company_id != self.company_id:
                raise AccessError(_('El tercero pertenece a otra compañía.'))
        if self.page_number < 0 or self.page_number > 100000:
            raise ValidationError(_('Página no válida.'))
        if any(len(value or '') > 100 for value in [self.product_query,self.location_query]):
            raise ValidationError(_('Use filtros de hasta100caracteres.'))

    @api.onchange('source','company_id','currency_id','date_from','date_to','partner_id','product_query','location_query','group_by')
    def _onchange_filters(self):
        self.page_number = 0

    @api.onchange('company_id')
    def _onchange_company(self):
        self.currency_id = self.company_id.currency_id
        self.partner_id = False

    @api.depends('source','company_id','currency_id','date_from','date_to','partner_id','product_query','location_query','group_by','page_number')
    def _compute_result(self):
        for query in self:
            if not query.source or not query.company_id or not query.date_from or not query.date_to:
                query.result_html = '<p>Seleccione un hecho disponible y complete los filtros. Informes no concede acceso a fuentes de otros módulos.</p>'
                continue
            engine = query.env['arg.pyme.report.engine']
            query.result_html = engine._html(engine._snapshot(query),query.page_number)

    def _action_self(self):
        return {'type':'ir.actions.act_window','name':_('Informes ARG'),'res_model':self._name,'res_id':self.id,'view_mode':'form','target':'current'}

    def action_refresh(self):
        self._validate_query();self.write({'page_number':0});return self._action_self()

    def action_next(self):
        data = self.env['arg.pyme.report.engine']._snapshot(self)
        if (self.page_number+1)*50 < data['result_count']:self.write({'page_number':self.page_number+1})
        return self._action_self()

    def action_previous(self):
        self._validate_query();self.write({'page_number':max(0,self.page_number-1)});return self._action_self()

    def action_csv(self):
        self._validate_query()
        return {'type':'ir.actions.act_url','url':'/arg/informes/%s/csv' % self.id,'target':'download'}

    def action_pdf(self):
        self._validate_query()
        return self.env.ref('arg_pyme_informes.action_report_pdf').report_action(self)
