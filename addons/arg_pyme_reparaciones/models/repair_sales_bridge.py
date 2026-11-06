from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from .repair_event import _REPAIR_ENGINE, repair_engine


class Quotation(models.Model):
    _inherit = 'arg.pyme.quotation'

    arg_repair_case_id = fields.Many2one('arg.pyme.repair.case', readonly=True, copy=False,
                                         check_company=True, ondelete='restrict', index=True,
                                         string='Reparación origen')

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        inherited_default = self.default_get(['arg_repair_case_id']).get('arg_repair_case_id')
        if inherited_default and self.env.context.get('_arg_repair_engine') is not _REPAIR_ENGINE:
            raise AccessError(_('La reparación no se recibe desde preferencias de carga.'))
        for raw in vals_list:
            values = dict(raw)
            if ('arg_repair_case_id' in values or 'default_arg_repair_case_id' in self.env.context):
                if self.env.context.get('_arg_repair_engine') is not _REPAIR_ENGINE:
                    raise AccessError(_('El presupuesto de reparación se prepara desde su parte.'))
            root = self.browse(values.get('commercial_root_id')).exists()
            if root:
                root.check_access('read')
                if root.arg_repair_case_id:
                    values['arg_repair_case_id'] = root.arg_repair_case_id.id
            case = self.env['arg.pyme.repair.case'].browse(values.get('arg_repair_case_id')).exists()
            if case:
                case._commercial_check()
                case._lock()
                if case.state not in ('diagnosed', 'authorized', 'in_progress'):
                    raise UserError(_('El parte no está disponible para un presupuesto o revisión.'))
                if root and case.quotation_root_id != root:
                    raise UserError(_('La revisión conserva el presupuesto origen de la reparación.'))
                if not root and case.quotation_root_id:
                    raise UserError(_('Abrí el presupuesto existente o creá una revisión.'))
                if values.get('company_id') != case.company_id.id or values.get('partner_id') != case.partner_id.id:
                    raise UserError(_('El presupuesto conserva cliente y compañía de la reparación.'))
            prepared.append(values)
        return super().create(prepared)

    def write(self, values):
        if 'arg_repair_case_id' in values:
            raise AccessError(_('La reparación origen se conserva.'))
        return super().write(values)

    def _lock_root(self):
        root = super()._lock_root()
        if self.arg_repair_case_id:
            self.arg_repair_case_id._lock()
            self.arg_repair_case_id._orders()
        return root

    def _generate_order(self, key, values):
        if self.arg_repair_case_id:
            case = self.arg_repair_case_id
            case._commercial_check()
            case._lock()
            return super(Quotation, repair_engine(self))._generate_order(key, values)
        return super()._generate_order(key, values)

    def _arg_document_relations(self):
        return super()._arg_document_relations() + [{'label': _('Parte de reparación'), 'records': self.arg_repair_case_id}]


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    arg_repair_case_id = fields.Many2one(related='arg_quotation_id.arg_repair_case_id', store=True,
                                         compute_sudo=False, string='Reparación origen', index=True)

    @api.model_create_multi
    def create(self, vals_list):
        if (any('arg_repair_case_id' in values for values in vals_list)
                or 'default_arg_repair_case_id' in self.env.context
                or self.default_get(['arg_repair_case_id']).get('arg_repair_case_id')):
            raise AccessError(_('La reparación se deduce del presupuesto autorizado.'))
        orders = super().create(vals_list)
        for order in orders.filtered('arg_repair_case_id'):
            case = order.arg_repair_case_id
            case._commercial_check()
            case._lock()
            if (case.state not in ('diagnosed', 'authorized', 'in_progress')
                    or order.arg_quotation_id.commercial_root_id != case.quotation_root_id
                    or order.company_id != case.company_id or order.partner_id != case.partner_id):
                raise UserError(_('El pedido no corresponde al alcance vigente de la reparación.'))
            case._record('order', case.state, fields.Date.context_today(case), {'order_id': order.id},
                         request_key='order:' + str(order.id), order_id=order.id)
        return orders

    def write(self, values):
        if 'arg_repair_case_id' in values:
            raise AccessError(_('El pedido conserva su reparación de origen.'))
        return super().write(values)

    def action_confirm(self):
        self._arg_lock_roots()
        for order in self.filtered('arg_repair_case_id'):
            case = order.arg_repair_case_id
            case._commercial_check(manager=True)
            case._check_order(order)
            if case.state not in ('authorized', 'in_progress'):
                raise UserError(_('Registrá la autorización del trabajo antes de confirmar el pedido.'))
        return super().action_confirm()

    def action_cancel(self):
        self._arg_lock_roots()
        if self.filtered(lambda order: order.arg_repair_case_id.state in ('ready', 'delivered')):
            raise UserError(_('El trabajo listo conserva sus pedidos. Retomá el trabajo o prepará su corrección vinculada.'))
        return super().action_cancel()

    def _action_cancel(self):
        self._arg_lock_roots()
        if self.filtered(lambda order: order.arg_repair_case_id.state in ('ready', 'delivered')):
            raise UserError(_('Retomá el trabajo antes de cancelar un pedido de una reparación lista.'))
        return super()._action_cancel()

    def action_draft(self):
        self._arg_lock_roots()
        if self.filtered(lambda order: order.arg_repair_case_id and order.arg_repair_case_id.state not in ('diagnosed', 'authorized', 'in_progress')):
            raise UserError(_('El parte cerrado no admite reactivar su pedido.'))
        return super().action_draft()

    def _arg_document_relations(self):
        return super()._arg_document_relations() + [{'label': _('Parte de reparación'), 'records': self.arg_repair_case_id}]


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        for raw in vals_list:
            values = dict(raw)
            order = self.env['sale.order'].browse(values.get('order_id') or self.env.context.get('default_order_id'))
            if order.arg_quotation_id.arg_repair_case_id:
                # Source terms are explicit; no inherited fulfillment/expense defaults may create work.
                values.update(qty_delivered=0, qty_delivered_percent=0, is_expense=False, is_downpayment=False)
                values.pop('qty_delivered_method', None)
                probe = self.new(values)
                probe._compute_qty_delivered_method()
                values['qty_delivered_method'] = probe.qty_delivered_method
            prepared.append(values)
        lines = super().create(prepared)
        for line in lines.filtered(lambda row: row.order_id.arg_repair_case_id):
            expected = 'stock_move' if line.product_id.type == 'consu' else 'manual'
            if line.qty_delivered or line.qty_delivered_method != expected or line.is_expense or line.is_downpayment:
                raise UserError(_('El servicio o repuesto requiere un método compatible y cumplimiento inicial cero.'))
        return lines

    def write(self, values):
        if {'qty_delivered_method', 'is_downpayment', 'is_expense', 'display_type'} & values.keys() and self.filtered(lambda line: line.order_id.arg_repair_case_id):
            raise AccessError(_('El método y la naturaleza de la línea provienen del acuerdo y su configuración compatible.'))
        if {'qty_delivered', 'qty_delivered_percent'} & values.keys():
            affected = self.filtered(lambda line: line.order_id.arg_repair_case_id)
            if affected and self.env.context.get('_arg_repair_engine') is not _REPAIR_ENGINE:
                raise AccessError(_('Las cantidades trabajadas se registran y corrigen mediante partes de trabajo.'))
        return super().write(values)
