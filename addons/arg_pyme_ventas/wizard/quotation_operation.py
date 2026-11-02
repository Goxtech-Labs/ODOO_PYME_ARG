import uuid
from odoo import api, fields, models, Command, _
from odoo.exceptions import AccessError, UserError


class QuotationOperation(models.TransientModel):
    _name='arg.pyme.quotation.operation'
    _description='Confirmación o generación parcial ARG'
    quotation_id=fields.Many2one('arg.pyme.quotation',required=True,readonly=True)
    mode=fields.Selection([('accept','Confirmar presupuesto'),('generate','Generar pedido')],required=True,readonly=True)
    operation_key=fields.Char(required=True,readonly=True,copy=False)
    line_ids=fields.One2many('arg.pyme.quotation.operation.line','wizard_id',string='Cantidades')

    @api.model_create_multi
    def create(self,vals_list):
        prepared=[]
        for raw in vals_list:
            values=dict(raw);quote=self.env['arg.pyme.quotation'].browse(values['quotation_id'])
            quote._authorize()
            if values['mode']=='accept':quote._require_manager()
            values['operation_key']=uuid.uuid4().hex
            committed=quote._committed_map()
            lines=[]
            for line in quote.line_ids:
                available=(line.target_quantity_total-line.accepted_target_total if values['mode']=='accept'
                           else line.accepted_target_total-committed.get(line.commercial_line_key,0))
                if available>0:lines.append(Command.create({'quotation_line_id':line.id,'available':available,'quantity':available}))
            values['line_ids']=lines;prepared.append(values)
        return super().create(prepared)

    def write(self,values):
        if {'quotation_id','mode','operation_key'} & values.keys():raise AccessError(_('La operación conserva origen, tipo y clave de reintento.'))
        return super().write(values)

    def action_apply(self):
        self.ensure_one();self.check_access('write');self.quotation_id._authorize()
        selected=[{'line_id':line.quotation_line_id.id,'quantity':line.quantity} for line in self.line_ids]
        if self.mode=='accept':
            self.quotation_id._accept(self.operation_key,selected)
            return {'type':'ir.actions.act_window_close'}
        order=self.quotation_id._generate_order(self.operation_key,selected)
        return {'type':'ir.actions.act_window','res_model':'sale.order','res_id':order.id,'view_mode':'form',
                'views':[(self.env.ref('arg_pyme_ventas.order_form').id,'form')]}


class QuotationOperationLine(models.TransientModel):
    _name='arg.pyme.quotation.operation.line'
    _description='Cantidad parcial ARG'
    wizard_id=fields.Many2one('arg.pyme.quotation.operation',required=True,ondelete='cascade')
    quotation_line_id=fields.Many2one('arg.pyme.quotation.line',required=True,readonly=True)
    product_id=fields.Many2one(related='quotation_line_id.product_id')
    uom_id=fields.Many2one(related='quotation_line_id.uom_id')
    available=fields.Float(readonly=True,digits='Product Unit',string='Disponible al abrir')
    quantity=fields.Float(digits='Product Unit',string='Cantidad seleccionada')

    @api.model_create_multi
    def create(self,vals_list):
        for values in vals_list:
            wizard=self.env['arg.pyme.quotation.operation'].browse(values['wizard_id']);wizard.check_access('write')
            line=self.env['arg.pyme.quotation.line'].browse(values['quotation_line_id'])
            line.check_access('read')
            if line.quotation_id!=wizard.quotation_id:raise AccessError(_('La línea debe pertenecer al presupuesto.'))
        return super().create(vals_list)

    def write(self,values):
        if {'wizard_id','quotation_line_id','available'} & values.keys():raise AccessError(_('No cambie el origen de la cantidad.'))
        return super().write(values)


class ReleaseWizard(models.TransientModel):
    _name='arg.pyme.quotation.release.wizard'
    _description='Liberación explícita de compromiso ARG'
    order_id=fields.Many2one('sale.order',required=True,readonly=True)
    reason=fields.Text(required=True,string='Motivo')
    operation_key=fields.Char(required=True,readonly=True,copy=False,default=lambda s:uuid.uuid4().hex)

    @api.model_create_multi
    def create(self,vals_list):
        for values in vals_list:
            order=self.env['sale.order'].browse(values['order_id']);order._arg_check_document_access();order.check_access('write');order._arg_require_manager()
            values['operation_key']=uuid.uuid4().hex
        return super().create(vals_list)

    def write(self,values):
        if {'order_id','operation_key'} & values.keys():raise AccessError(_('La operación conserva origen y clave.'))
        return super().write(values)

    def action_apply(self):
        self.ensure_one();self.check_access('write')
        self.order_id._arg_release_commitment(self.operation_key,self.reason)
        return {'type':'ir.actions.act_window_close'}
