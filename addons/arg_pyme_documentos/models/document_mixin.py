from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.float_utils import float_compare


class Company(models.Model):
    _inherit = 'res.company'
    arg_demo_mode = fields.Boolean(string='Datos de ejemplo ARG', default=False, groups='base.group_user')


class DocumentMixin(models.AbstractModel):
    _name = 'arg.pyme.document.mixin'
    _description = 'Contrato documental ARG'
    _arg_document_enabled = True
    _log_access = True

    arg_demo = fields.Boolean(readonly=True, copy=False, groups='base.group_user')
    arg_identity_id = fields.Many2one('arg.pyme.document.identity', readonly=True, copy=False, ondelete='restrict', groups='base.group_user')
    arg_document_type_id = fields.Many2one(related='arg_identity_id.document_type_id', readonly=True, store=True, groups='base.group_user')
    arg_number = fields.Char(related='arg_identity_id.code', readonly=True, store=True, index=True, groups='base.group_user')
    arg_reference = fields.Char(string='Referencia externa', copy=False, groups='base.group_user')
    arg_completion_axes = fields.Json(compute='_compute_arg_completion_axes', string='Pendientes ARG', compute_sudo=False, groups='base.group_user')

    def _arg_document_code(self):
        # Concrete adapters opt in by returning a registered code. No universal transaction table.
        return False

    @api.model_create_multi
    def create(self, vals_list):
        if (any(v.get('arg_identity_id') or v.get('arg_number') or v.get('arg_document_type_id') for v in vals_list)
                or any(self.env.context.get('default_'+key) for key in ('arg_identity_id','arg_number','arg_document_type_id'))):
            raise AccessError(_('La identidad se asigna automáticamente al guardar.'))
        vals_list=[{**values,'arg_demo':self.env['res.company'].browse(values.get('company_id') or self.env.company.id).arg_demo_mode} for values in vals_list]
        records = super().create(vals_list)
        for record in records:
            code = record._arg_document_code()
            if code:
                identity = self.env['arg.pyme.document.identity']._allocate_for(record, code)
                # Internal field assignment only; never sudo business records or trust RPC context flags.
                super(DocumentMixin, record).write({'arg_identity_id': identity.id})
        return records

    def write(self, values):
        if {'arg_identity_id','arg_number','arg_document_type_id','arg_demo'} & values.keys():
            raise AccessError(_('La identidad documental no se edita.'))
        if values.get('company_id') and any(r.arg_identity_id and r.company_id.id != values['company_id'] for r in self):
            raise UserError(_('Un documento numerado conserva su compañía.'))
        return super().write(values)

    def unlink(self):
        if any(r.arg_identity_id for r in self):
            raise UserError(_('Conserve el documento y use la cancelación o reversión de su circuito.'))
        return super().unlink()

    def _arg_check_document_access(self):
        self.ensure_one()
        self.check_access('read')
        if self.env.user.share or not self.env.user.has_group('arg_pyme_base.group_operator'):
            raise AccessError(_('El documento requiere acceso interno ARG.'))
        if self.company_id not in self.env.companies:
            raise AccessError(_('Compañía no habilitada.'))

    @api.depends('write_date')
    def _compute_arg_completion_axes(self):
        for record in self:
            record.arg_completion_axes = record._arg_get_completion_axes()

    def _arg_get_completion_axes(self):
        # Circuit adapters extend dependencies and compute only from their actual native sources.
        return []

    @api.model
    def _arg_unknown_axis(self, label, explanation):
        return {'label': label, 'state': 'unknown', 'closed_shortfall': False,
                'lines': [], 'explanation': explanation}

    def _arg_invoice_scope_reason(self, invoices, origin_field):
        # Native reconciliation is at invoice level, not at commercial-line level.
        # Only invoices whose every monetary product line belongs exclusively to this order
        # can supply an amount attributed to it. Never apportion a shared payment implicitly.
        self.ensure_one()
        for invoice in invoices:
            if not invoice.has_access('read'):
                return _('No hay permisos suficientes para determinar el alcance de las facturas relacionadas.')
            lines = invoice.invoice_line_ids.filtered(lambda line: line.display_type == 'product')
            if not lines or not lines.has_access('read'):
                return _('No hay detalle suficiente para atribuir las facturas relacionadas a este pedido.')
            for line in lines:
                origins = line[origin_field]
                if not origins or not origins.has_access('read') or any(origin.order_id != self for origin in origins):
                    return _('Una factura relacionada contiene líneas de otros pedidos o sin origen exclusivo. La conciliación nativa no atribuye dinero ni deuda a cada pedido; consulte las facturas y sus aplicaciones, sin prorrateo implícito.')
        return ''

    @api.model
    def _arg_axis(self, label, lines):
        # Never aggregate quantities of incompatible units. Classify each eligible line, then the axis.
        eligible = []; progressed = False; shortfall = False
        for raw in lines:
            row = dict(raw)
            rounding = row.get('rounding', 0.01)
            if rounding <= 0: raise ValidationError(_('La precisión debe ser positiva.'))
            target = row.get('target', 0)
            if float_compare(target, 0, precision_rounding=rounding) <= 0: continue
            done = max(0, row.get('done', 0))
            complete = float_compare(done, target, precision_rounding=rounding) >= 0
            row_progressed = float_compare(done, 0, precision_rounding=rounding) > 0
            progressed |= row_progressed
            closed = max(0, row.get('closed', 0))
            shortfall |= not complete and float_compare(closed, 0, precision_rounding=rounding) > 0
            row.update(done=done, pending=max(0, target-done-closed), closed=closed,
                       state='complete' if complete else ('partial' if row_progressed else 'pending'))
            eligible.append(row)
        state = 'na' if not eligible else ('complete' if all(r['state']=='complete' for r in eligible) else ('partial' if progressed else 'pending'))
        return {'label':label,'state':state,'closed_shortfall':shortfall,'lines':eligible}

    def _arg_report_payload(self):
        raise UserError(_('Este circuito todavía no tiene adaptador de impresión ARG.'))

    def action_arg_print(self):
        self._arg_check_document_access()
        if not self.arg_identity_id:
            raise UserError(_('Guarde primero el documento válido para asignar su número.'))
        return self.env.ref('arg_pyme_documentos.action_report_document').report_action(self, data={'arg_model':self._name,'arg_ids':self.ids})
