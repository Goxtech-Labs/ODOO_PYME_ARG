# Data model: Circuito Compras ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Pedido proveedor | `purchase.order/purchase.order.line` | PPC, proveedor, partner_ref, moneda, product_qty, uom_id | Referencia de proveedor independiente del código interno |
| Entrada | `stock.picking/stock.move` | ENT y purchase_line_id con cantidades efectivas | Existencias sólo desde movimientos validados |
| Factura recibida | `account.move/account.move.line` | FRC, referencia fiscal proveedor y líneas de compra | Conservar número original del proveedor sin reemplazarlo por FRC |

## Estados, efectos y seguridad

- Estados nativos de compra: draft, sent, to approve, purchase y cancel; etiquetas ARG sin falsificar estado real.
- Usar product_qty, qty_received, qty_invoiced y qty_to_invoice según política del producto.
- Conservar unidad uom_id de purchase.order.line en la rama Odoo20 verificada.
- Usar relaciones de líneas, no sólo texto origin.
- No interpretar receipt_status full como prueba de todas las cantidades recibidas.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.

## Decisiones implementadas para la entrega comercial

PPC sobre purchase.order; FRC/NCP sobre account.move. Wizard arg.pyme.purchase.bill.wizard selecciona cantidades;
arg.pyme.purchase.bill.operation conserva clave/hash/actor/documento para reintentos. No son libros paralelos.
Snapshot de confirmación conserva también líneas y totales para reimpresión histórica. El detalle confirmado no
se edita; cancelación/reapertura controlada conserva número/historia. Preparación factura fuerza tipo in_invoice/draft.
Facturación publicada agrega lote por línea y controla neto, producto/unidad; borradores no acreditan cumplimiento.
Fechas soft futuras siguen programación nativa. Guard/precio de proveedor se ejecutan bajo la misma compañía.
Rutas comerciales de factura están en models/account_move.py y views/account_move_views.xml.
Las rutas purchase_receipt/purchase_return previstas pertenecen al puente008; no se crean cascarones sin funcionamiento.
