# F15 · frontera de cambios de la propuesta

Inventario de implementación para T027–T029. **No acredita cobertura implementada ni pruebas de
concurrencia.** Complementa el [contrato de reposición](reposicion.md). La consulta y ficha de
configuración son un incremento distinto de la confirmación completa de compra y fabricación.

## Regla de participación

El collector privado autoriza y registra efectos de una confirmación ARG. Por sí solo no estabiliza
una propuesta: cambios nativos ajenos a esa confirmación también deben invalidarla o serializarse.
La participación técnica global conserva permisos nativos y `super`; no impone un rol ARG a todos
los usuarios ni otorga acceso de negocio mediante sudo.

Adquirir una revisión técnica efectiva antes del primer efecto pertinente, no sólo una lectura o un
lock que no modifica la fila. Cubrir altas, bajas y uniones de productos/dimensiones anteriores y
nuevos, incluyendo registros archivados que participan en selección. Un alta de proveedor o BOM
puede cambiar la elección aunque no existiera al revisar: bloquear sólo candidatos ya seleccionados
no cubre esa inserción. Las definiciones compartidas necesitan una revisión de alcance apropiado.

Coordinar un orden común entre entradas: configuración compartida → plantillas/unidades → productos
→ reglas/documentos/movimientos/quants, con IDs ordenados dentro de cada clase. Es un orden a
armonizar con los consumidores existentes, no una garantía por enumerarlo. SerializationFailure o
deadlock revierte y reintenta la transacción completa según Odoo; nunca continuar una porción.

## Matriz de consumidores y mutadores

Fuentes seleccionadas de Odoo Community, revisión
`bb238af6f0ddd70d7ff91521c6104472583661d1`. Rutas relativas al árbol oficial; evidencia de comparación
de archivos seleccionados con runtime fuera de Git. No equivale a igualdad de todo el core.

| Frontera | Entradas y dimensiones a cubrir | Fuente primaria seleccionada |
| --- | --- | --- |
| Previsión física | `stock.move` create/write/unlink y confirmación/reserva/cancelación/finalización: producto, cantidad, UOM, estado, fecha, ubicaciones, ubicación prevista y relaciones de abastecimiento/MO; incluir producto final de las MO relacionadas con insumos | `addons/stock/models/stock_move.py` |
| Existencia y reserva | `stock.quant` y `stock.move.line` CRUD: cantidades, producto, ubicación, lote, propietario y paquete. Prelock antes de `_update_available_quantity`, que adquiere locks nativos; `_merge_quants` modifica por SQL y requiere cobertura propia | `addons/stock/models/stock_quant.py`, `stock_move_line.py` |
| Pipeline de compra | PO y líneas CRUD, estados/cabecera, producto/cantidad/UOM/compañía/tipo de operación/ubicación prevista/enlaces a movimientos y reglas. RFQ draft/sent/to approve también sin orderpoint; no asumir filtro por fecha planificada | `addons/purchase_stock/models/product.py`, `purchase_order.py`, `purchase_order_line.py` |
| Fecha de compra | `purchase_stock.purchase.order.line.write` puede ajustar movimientos antes de `super`; serializar antes. Cambios de estado o tipo de operación de cabecera abarcan sus productos | `addons/purchase_stock/models/purchase_order_line.py` |
| Pipeline de fabricación | MO create/write/unlink, producto/cantidad/UOM/BOM/estado/ubicaciones/tipo de operación/regla/fechas. Draft agrupa producto y ubicación prevista; confirmadas dependen del horizonte | `addons/mrp/models/stock_orderpoint.py`, `mrp_production.py` |
| Efectos indirectos MRP | Trabajos CRUD, estado/duración/fechas/centro/planificación y movimientos de insumos/terminados afectan estado y fechas de MO. `mrp.workorder.write` y `change_prod_qty` cambian efectos antes de `MO.write`; cubrir producto final y componentes anteriores/nuevos antes de esa cascada | `addons/mrp/models/mrp_workorder.py`, `mrp_production.py`, `addons/mrp/wizard/change_production_qty.py` |
| Selección de proveedor | Variantes, plantillas y supplierinfo CRUD/archivo: compañía, almacenable, UOM, categoría/rutas, proveedor/producto/plantilla, mínimo/vigencia/precio/descuento/moneda/secuencia/plazo. Incluir variantes archivadas anteriores/nuevas. Selección compara precio convertido y fecha | `addons/product/models/product_product.py`, `product_template.py`, `product_supplierinfo.py` |
| BOM y operaciones | BOM, componentes, subproductos y operaciones CRUD: aplicabilidad/atributos/variante, normal/phantom, compañía/tipo de operación/secuencia/cantidad/UOM/lote/plazos. Altas de BOM genéricas modifican candidatos | `addons/mrp/models/mrp_bom.py`, `mrp_routing.py` |
| Rutas y topología | Regla de reposición, stock.rule, stock.route, categorías/padres, ubicaciones/jerarquía, almacén y tipo de operación CRUD: activo/compañía/secuencia/acción/origen/destino/rutas heredadas/pasos/plazos/autoconfirmación. `warehouse.write` inicia cascadas; intervenir antes | `addons/stock/models/stock_orderpoint.py`, `stock_rule.py`, `stock_location.py`, `stock_warehouse.py`, `stock_picking_type.py`; `addons/product/models/product_category.py` |
| Definiciones compartidas | Factores y unidad relativa, descendientes UOM, precisión Product Unit, horizonte/lead times de compañía, calendario, centros/capacidad/operaciones y sus fechas | `addons/uom/models/uom_uom.py`, `odoo/addons/base/models/decimal_precision.py`, modelos company/resource/mrp seleccionados |

## Conflictos detectados en los consumidores ARG existentes

- StockMove ARG no toma actualmente `_arg_lock_stock`; bloquear sólo quant no cubre la previsión.
- Quant.write ARG bloquea producto actual, pero hay que incorporar el nuevo `product_id` y el
  prelock de `_update_available_quantity` antes del lock quant nativo.
- Compras `_arg_lock` comienza por PO; añadir producto → PO en otro camino invierte el orden.
- INV usa conteo → plantilla → unidad → producto; matriz de catálogo usa lista → plantilla → producto.
  Armonizar entradas o documentar/reintentar conflictos; ordenar IDs no resuelve por sí solo el orden
  entre clases. Conservar contratos de conteo, precios y compras al cambiar estas entradas.

## Cobertura todavía por completar

El inventario de fuentes seleccionadas no cubre aún todos los mutadores de monedas/tipos de cambio,
campos de agrupación y comprador (`buyer_id`, `group_rfq`, `group_on`), recurso, asistencias/ausencias
de calendario ni atributos de variantes. Sus consumidores afectan precios, agrupación, disponibilidad
y BOM aplicable. Completar su procedencia y hooks antes de acreditar la frontera completa.

Compra calcula parte del pipeline con sudo nativo. No atribuir a esa lectura permisos individuales
de cada RFQ ni inventar un cero por falta de acceso. Revisar aislamiento por compañía/ubicaciones
compartidas en el adaptador ARG, sin sustituir el motor por máximo menos físico ni alterar el
comportamiento global del scheduler. La ficha actual no consulta ese pipeline.

La salida de T027–T029 requiere una matriz final campo/método/hook/alcance del paquete y sus
consumidores, además de revisión de fuente. QA funcional y concurrencia se ejecutarán en la fase
posterior acordada; ni este inventario ni AST prueban atomicidad en ejecución.
