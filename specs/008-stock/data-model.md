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

## F15 · reglas, propuestas y evidencia

| Entidad | Representación | Restricciones y efectos |
| --- | --- | --- |
| Regla | `stock.warehouse.orderpoint` | Producto almacenable, compañía actual, depósito/ubicación interna compatibles; mínimo/máximo finitos, `0 ≤ mínimo ≤ máximo`; nueva regla ARG manual; conservar modalidad existente |
| Propuesta | Servicio abstracto `arg.pyme.replenishment` y estado de interfaz | Hasta30 reglas por página/confirmación; momento de consulta y horizonte explícitos; cantidades elegidas finitas y positivas; mantener unidad y huella por regla; no persistir otro saldo |
| Operación | `arg.pyme.replenishment.operation` | Compañía/actor, `operation_key` UUID canónico de36 caracteres, hash de payload y propuesta, instante de confirmación, cantidades aceptadas y resultados nativos; sólo creación interna validada, sin write/unlink ni lectura/exportación ORM para usuarios de gestión |
| Resultado | Contenido inmutable de operación con referencias y deltas | Modelo/id/compañía/unidad/cantidad anterior y posterior/estado cuando corresponda, siempre con permisos revalidados al abrir; PO/MO nuevas o ampliadas y ramas/componentes identificados; no sumar componentes como unidades del kit |

Unicidad técnica `(company_id, operation_key)`. Reintento idéntico conserva operación; nueva carga
con la misma clave se rechaza. No exponer UUID técnico como número de documento comercial.
La fecha/hora de consulta/registro se propone actual, pero las fechas planificadas elegidas/nativas
son dimensiones diferentes y se conservan. Nunca sustituir cantidades desconocidas por cero.
La propuesta no persiste documentos y el recibo no constituye saldo, pedido, producción o movimiento.


La evidencia cruda sólo puede leerse por el servicio técnico elevado, después de autorizar rol y
compañía. Todo resultado/replay revalida sus dimensiones como solicitante ACTUAL de esa lectura, sin sudo, y deniega
la representación completa si alguna relación dejó de ser legible, con mensaje genérico sin datos
ocultos. El actor original también puede perder acceso; create_uid no sustituye esta comprobación.
No conceder ACL de read/export raw a roles de gestión ni exponer JSON mediante campos relacionados.

Distinguir identidad de ejecución y de lectura: el actor original guardado identifica/autorizó los
efectos de la confirmación; otra persona responsable puede pedir el recibo después. Su respuesta
siempre se valida con los permisos actuales de quien la recibe, no con los del actor histórico.
