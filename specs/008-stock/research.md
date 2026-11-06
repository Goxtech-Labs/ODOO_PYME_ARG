# Research: Circuito Stock ARG

Fecha: 2026-11-01. Separar comportamiento nativo comprobado y decisiones de diseño ARG.

## Decisiones

### D01

**Decision**: Conservar stock.quant y movimientos nativos como única fuente de existencias.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D02

**Decision**: El documento ARG de conteo agrupa decisiones y evidencia; sus efectos se registran en movimientos nativos.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D03

**Decision**: Activación de stock con ventas/compras previas exige previsualizar hooks sale_stock/purchase_stock y respaldo recuperable.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

## Fuentes primarias

- [Fuente oficial 1](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_quant.py)
- [Fuente oficial 2](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_move.py)
- [Fuente oficial 3](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_picking.py)
- [Fuente oficial 4](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/sale_stock/__manifest__.py)
- [Fuente oficial 5](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/purchase_stock/__manifest__.py)

Consultar además [investigación general](../001-pyme-argentina/research.md) y [hallazgos nativos](../../docs/tecnica/DECISIONES-ODOO20.md).
Registrar revisión exacta y dependencias antes de instalar un addon. La existencia de un modelo no acredita cobertura Enterprise.

## F14 ·2026-11-06

**Decision**: consultar líneas finalizadas y cantidades actuales nativas, no copiar stock_report ni
arbitrariamente sumar un historial como saldo. Paginar en servidor y abrir el origen.
**Rationale**: una línea representa un hecho físico; reservas y facturación tienen otras granularidades.
**Alternatives considered**: usar action_lot_open_transfers como toda la traza (sólo entregas), o
editar location_id desde el maestro (inverse con movimiento real); descartadas para la consulta ARG.

Stock20 de la revisión fijada conserva product_qty nativa y quantity_product_uom por línea. Sus
archivos lot/move_line/traceability y vistas inspeccionados se contrastaron con runtime y GitHub
oficial bb238af6f0ddd70d7ff91521c6104472583661d1; no se afirma igualdad de todo el core.
[Lot](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_lot.py),
[líneas](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_move_line.py),
[traza](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/report/stock_traceability.py).

## F15 · investigación2026-11-06

### D04 · cálculo y ejecución nativos separados de la consulta

**Decision**: acción ARG propia sobre `stock.warehouse.orderpoint`; nuevas reglas manuales,
propuesta desde físico/previsto/pipeline y `_get_qty_to_order()`, confirmación con cantidad aceptada.
**Rationale**: `_get_orderpoint_action` elimina/recalcula/crea reglas; `action_replenish` reemplaza
cantidad por manual/to_max. `_procure_orderpoint_confirm` permite mantener la transacción y errores.
**Alternatives considered**: usar el menú nativo como lectura inocua o calcular máximo menos físico;
descartadas porque producen efectos o ignoran abastecimiento y reglas vigentes.

### D05 · recibo y captura de efectos

**Decision**: evidencia inmutable con clave/payload en la misma transacción; collector privado y
hooks sobre destinos autorizados, sin una referencia comercial artificial por operación.
**Rationale**: compra puede ampliar una línea existente; fabricación puede ampliar MO o crear
varias por tamaño de lote. Una referencia única altera el agrupamiento nativo. El retorno vacío
no demuestra generación y el core usa sudo; autorizar como actor original en los límites de efecto.
**Alternatives considered**: contar documentos nuevos, filtrar sólo por write_date, cambiar origin
para correlacionar o declarar seguridad sólo por super(); descartadas por pérdida de evidencia
exacta, modificación de agrupación o permisos insuficientemente garantizados.

### D06 · fabricación modular sin recorte de alcance

**Decision**: puente opcional Stock–MRP y compra en el puente existente de Compras–Stock.
**Rationale**: una pyme genérica no necesita MRP instalado para Stock, pero F15 incluye implementar
y entregar compra/fabricación. La demo actual103 módulos no tiene MRP; su código fuente sí existe.
Kits phantom se expanden antes del despacho; una sugerencia del kit no equivale a fabricar su SKU.
**Alternatives considered**: dependencia MRP obligatoria o dar por terminado F15 con compras;
descartadas por modularidad y por reducir el alcance acordado.

Se verificaron cinco archivos seleccionados purchase_stock/mrp del runtime contra la revisión
oficial fijada; igualdad de esas fuentes, no de todo el core. No se ejecutó una reposición como QA.
[Orderpoint](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_orderpoint.py),
[compra/pipeline](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/purchase_stock/models/stock.py),
[compra/reglas](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/purchase_stock/models/stock_rule.py),
[fabricación/reglas](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/mrp/models/stock_rule.py),
[fabricación/orderpoint](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/mrp/models/stock_orderpoint.py).


### D07 · confirmación de previos y abastecimiento hijo

**Decision**: incluir las MO borrador preexistentes que el postprocesado nativo confirma, autorizar
`action_confirm` y el wizard de cambio de cantidad; extender el alcance revisado a reposiciones hijas.
**Rationale**: MRP `_post_process_scheduler` no se limita a nuevas MO; `change_prod_qty` ajusta
movimientos/subproductos/trabajos y dispara scheduler de insumos. `_trigger_scheduler` nativo pide
`raise_user_error=False`; dentro de operación ARG privada se fuerza propagación de errores y la
misma transacción, sin modificar el scheduler global ni omitir ramas.
**Alternatives considered**: confirmar sólo MO nuevas, desactivar esos efectos globalmente o
permitir éxito raíz con fallo hijo; descartadas por alterar semántica o violar la atomicidad.

La cantidad aceptada se fija mediante qty_to_order_manual directamente; la inversa de qty_to_order
borra el manual en reglas auto. La propuesta explica el override pendiente y su consumo al completar.
El wizard y stock.move seleccionados se verificaron además contra runtime/revisión fijada.
[Wizard MRP](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/mrp/wizard/change_production_qty.py),
[abastecimiento hijo](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_move.py).

### D08 · frontera global y configuración práctica

La [matriz de mutadores](contracts/reposicion-mutadores.md) identifica entradas directas, cascadas,
conflictos de orden existentes y fuentes aún pendientes antes de cerrar T027–T029. Es diseño de
implementación; no prueba cobertura global ni concurrencia. El collector privado no reemplaza esa frontera.

La ficha US6 conserva esenciales visibles y ruta/presentación plegadas. Seleccionar busca treinta
opciones por página sin descartar límites editados; cambiar página conserva filtros aplicados.
Guardar valida permisos nativos y un token de configuración para evitar sobrescribir una edición
posterior; el token no acredita estabilidad de la previsión. Ficha Odoo abre sólo el formulario
nativo de esa regla, sin ejecutar `_get_orderpoint_action`; no se atribuyen a ese formulario
campos que no expone. Los selectores ARG de proveedor/BOM y el horizonte se completarán junto
con los adaptadores y propuesta; T024 conserva ese alcance pendiente. Al quitar una ruta,
simular las limpiezas nativas de proveedor/BOM y validar el múltiplo efectivo tras guardar en la
misma transacción. Fuente US6 pendiente de instalación; FR013 y confirmación US7 siguen abiertas.
