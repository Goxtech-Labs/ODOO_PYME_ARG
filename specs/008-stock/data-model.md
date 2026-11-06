# Data model: Circuito Stock ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Existencia | `stock.quant` | producto, ubicación, lote, cantidad, reserva | No escribir quantity directamente para simular movimientos |
| Movimiento | `stock.picking/stock.move/stock.move.line` | origen, destino, cantidad, unidad, lote y relaciones | Mover existencias sólo al validar operaciones nativas |
| Conteo | `arg.pyme.inventory.count y líneas` | INV, ubicación, teórico, contado, diferencia y movimientos | Aplicar diferencias mediante stock.quant.action_apply_inventory con control concurrente |

## Estados, efectos y seguridad

- Una transferencia interna es neutra para el total de empresa y cambia saldos por ubicación.
- Distinguir demanda product_uom_qty, cantidad operada quantity y cantidades finalizadas.
- Usar backorders y retornos nativos, conservando enlaces.
- No escribir qty_delivered o qty_received comerciales cuando derivan de movimientos.
- No generar stock por editar tarifas ni contabilizar otra entrada al registrar factura.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.

## Implementación

arg.pyme.inventory.adjustment es evidencia AJU única por count_id y enlace a stock.move; no otro saldo.
arg_stock_revision en product.product es nonce técnico de concurrencia. INV conserva baseline/fingerprint por
producto/lote/paquete/propietario y scope_snapshot de nombres/unidades; AJU conserva líneas/diferencias.
StockMove.arg_closed_quantity_base registra cierre explícito en unidad base; no altera demanda/quantity ni saldo.
Picking captura demanda al finalizar/cancelar, agrupa por producto en unidad base y recorre backorders y devoluciones.
Los puentes propios poseen toda relación comercial física; el core no consulta modelos de Ventas/Compras ausentes.

## F14 · representación de consulta y alta

`arg.pyme.stock.trace` abstracto reúne stock.lot, stock.move.line y stock.quant de compañía actual.
No persiste resultados, saldo ni genealogía. Una fila es una línea nativa terminada; los detalles
de cantidades son quants actuales, con ámbito/fecha separados del rango histórico.
`arg.pyme.lot.create` transitorio contiene producto, número, referencia, compañía y enlace protegido
al lote creado. Confirma una sola vez por asistente; serializa asistente/producto antes de crear y
conserva resultado para reintentos. No contiene cantidad física ni un documento comercial nuevo.

stock.lot conserva su identidad y validación nativas; la extensión serializa create y write de
nombre/producto/compañía mediante el lock técnico de los productos implicados. Ningún saldo nuevo.
