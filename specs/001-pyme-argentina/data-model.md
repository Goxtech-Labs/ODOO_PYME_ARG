# Data model

Definir modelo conceptual y correspondencia nativa propuesta; validar campos en cada spec independiente.

## Entidades

| Entidad | Modelo candidato | Restricciones |
| --- | --- | --- |
| Empresa | `res.company` | Compañía y moneda explícitas en documentos operativos |
| Tercero | `res.partner` | Compartir identidad; combinar roles cliente/proveedor sin duplicar ficha |
| Producto/servicio | `product.template`, `product.product` | SKU textual; conservar ceros iniciales; unidad y tipo explícitos |
| Presupuesto | `arg.pyme.quotation`, `arg.pyme.quotation.line` | Documento propio PRE; sin efectos físicos, contables o financieros |
| Pedido cliente | `sale.order`, `sale.order.line` extendidos | Documento posterior PED; enlazar presupuesto confirmado y sus líneas |
| Pedido proveedor | `purchase.order`, `purchase.order.line` | Proveedor, compañía, moneda y líneas al confirmar |
| Entrada/remito/traspaso | `stock.picking`, `stock.move`, `stock.move.line` | Cambiar existencias sólo por movimientos validados |
| Factura/nota | `account.move`, `account.move.line` | Conservar libro nativo, moneda e importes históricos |
| Cobro/pago | `account.payment` y conciliación nativa | Medio, importe positivo, moneda y contraparte; aplicación explícita |
| Caja/banco | `account.journal` | Configurar por compañía; separar monedas |
| Lote/serie | `stock.lot` | Exigir sólo cuando el producto requiera trazabilidad |
| Tipo y secuencia | Extensión + `ir.sequence` | Prefijo de 2 a 4 letras ASCII; contador mínimo de seis dígitos |
| Relación documental | Relaciones nativas y extensiones justificadas | Origen, destino, línea, cantidad/importe aplicado y pendiente |

## Entidades transversales de ayuda y soporte

- **Recurso de ayuda**: módulo, tarea, URL YouTube/lista, manual, versión demostrada, versiones compatibles,
fecha/responsable de revisión, estado y sustituto. Mantener referencias editables sin reinstalar addons.
- **Configuración de soporte**: centro de ayuda, canal principal, correo, WhatsApp y URL de tickets.
Mantener destinos bajo permisos administrativos y habilitar sólo canales realmente configurados.
- **Identidad del bot**: nombre visible GOXTECHBOT, avatar y textos vigentes; conservar registros y relaciones nativas.

## Identidad documental

Mantener identificador técnico separado del código legible.
Garantizar unicidad de `(company_id, tipo_documental, serie_interna, numero_interno)`.
En el contrato Base v1 la serie interna es única e implícita: la restricción más fuerte
`(company_id, document_type_id, number)` evita también colisiones de esa tupla. No se ofrece
una selección de series ni se mezcla con el punto de venta fiscal. Ver contrato de identidad
de specs/002-base-arg/data-model.md.
Asignar código en el primer guardado; mostrar «Nuevo» antes de persistir.
No reutilizar códigos anulados ni editar identificadores asignados.
Mantener continuidad entre ejercicios por defecto; no prometer ausencia de saltos técnicos.
Configurar prefijos antes de la primera asignación y conservar referencias fiscales por separado.

| Circuito | Documento | Código propuesto |
| --- | --- | --- |
| Ventas | Presupuesto | `PRE-000001` |
| Ventas | Pedido cliente | `PED-000001` |
| Ventas/Stock | Remito salida | `REM-000001` |
| Ventas | Factura venta | `FAC-000001` |
| Ventas | Nota crédito/débito | `NCV-000001` / `NDV-000001` |
| Compras | Pedido proveedor | `PPC-000001` |
| Compras/Stock | Entrada | `ENT-000001` |
| Compras | Factura recibida | `FRC-000001` |
| Compras | Devolución proveedor | `DCP-000001` |
| Stock | Transferencia | `TRA-000001` |
| Stock | Inventario/ajuste | `INV-000001` / `AJU-000001` |
| Administración | Recibo cobro | `REC-000001` |
| Administración | Orden pago | `OPA-000001` |
| Administración | Movimiento entre cajas | `MCA-000001` |

Usar DCL para devolución física de cliente, DCP para devolución física a proveedor y NCP para nota de crédito recibida. Ver diccionario documental canónico.
Conservar identidad fiscal y referencia del proveedor sin reemplazarlas por estos códigos internos.

## Estados y efectos

| Documento | Estados propuestos | Efecto |
| --- | --- | --- |
| Presupuesto | Borrador, emitido, confirmado, rechazado, vencido, cancelado | Propuesta comercial |
| Pedido | Borrador, confirmado, parcial, cumplido, cancelado | Compromiso; reservas según política explícita |
| Entrada/remito | Borrador, preparado, parcial, validado, cancelado | Movimiento físico al validar |
| Factura/nota | Borrador, contabilizada, revertida | Registro contable; autorización fiscal independiente |
| Recibo/pago | Borrador, confirmado, aplicado/parcial, revertido | Movimiento financiero y aplicación conciliable |
| Inventario | Borrador, contado, validado | Diferencia física mediante ajuste identificado |
| Informe | Consulta | Ningún efecto operativo |

Separar estado documental de entregado, facturado, cobrado y autorizado fiscalmente.
Usar reversiones para efectos confirmados y preservar sus vínculos.
Resolver transiciones exactas y versionado de presupuesto en sus specs de módulo.
Conservar presupuesto y pedido como registros documentales distintos; no limitar su separación a vistas o estados del mismo registro.

## Hechos y dimensiones

| Hecho | Granularidad | Medidas | Fecha |
| --- | --- | --- | --- |
| Demanda | Línea pedido confirmado | Cantidad pedida/pendiente | Confirmación |
| Venta facturada | Línea factura contabilizada | Neto, impuestos, total, cantidad; NC con signo contrario | Factura |
| Compra facturada | Línea factura recibida contabilizada | Neto, impuestos, total; notas con signo correspondiente | Comprobante |
| Movimiento físico | Línea movimiento validado | Cantidad en unidad base por ubicación | Validación |
| Flujo financiero | Movimiento financiero confirmado | Entrada/salida por cuenta y moneda | Movimiento |
| Aplicación | Imputación de cobro/pago a deuda | Importe aplicado y pendiente | Aplicación |
| Vencimiento | Cuota pendiente | Saldo y días de atraso | Vencimiento |

Usar dimensiones compartidas: compañía, tercero, producto/variante, categoría, depósito/ubicación,
moneda, tipo documental, documento, estado y fechas con roles diferenciados.
Agregar vendedor, canal, lote/serie y atributos sectoriales solamente cuando correspondan.
Conservar cotización histórica y política de conversión explícitas.

Aplicar reglas contra duplicación:

- Medir facturación desde facturas, sin sumar presupuestos, pedidos y remitos.
- Medir existencias desde movimientos físicos, sin sumar facturas como movimientos nuevos.
- Medir dinero desde flujos financieros, sin volver a sumar imputaciones.
- Mantener traslados internos neutros para la empresa y visibles por depósito/caja.
- Distinguir pagado de imputado y deuda documental de movimiento de caja.
- Excluir borradores y cancelaciones de hechos confirmados; mostrarlos en consultas propias.
- Aplicar permisos y filtros de compañía antes de agrupar o exportar.
