# Stock ARG y puentes — implementación

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

F15 reposición tiene [fuente parcial sin instalar](../entregas/008-reposicion.md). La configuración
usa el servicio `arg.pyme.replenishment`, nunca `_get_orderpoint_action` como consulta. El guardado
compara un token de `write_date` previo al lock de configuración; no garantiza estabilidad de la
previsión. Selector de múltiplos desde el cómputo nativo con dimensiones propuestas y revalidación
posterior a inversas. Revisar la [frontera de mutadores pendiente](../../specs/008-stock/contracts/reposicion-mutadores.md)
antes de implementar confirmación. La evidencia privada existente tampoco completa replay.

Core arg_pyme_stock depende de Base/UI/Catálogo/Documentos y stock. Puentes arg_pyme_ventas_stock y
arg_pyme_compras_stock dependen de su circuito, Stock ARG y sale_stock/purchase_stock respectivamente;
auto_install sólo cuando se satisface esa composición. Son puentes internos, no proveedores externos.

## Fuente y consultas

stock.quant y stock.move/move.line/picking conservan los libros nativos. Matriz paginada30 por depósito, ubicación,
producto y compañía activa; contexto actual explícito limpia to_date/lot/owner/package heredados. Físico/free/
entrante/saliente/previsto son campos nativos; reservado es suma de quants en el mismo dominio de ubicación.
No calcular reservado como físico-disponible porque hay cantidades no utilizables por otras restricciones.

## Documento físico y estados

Picking hereda contrato documental y códigos por tipo/devolución. Demanda se captura al finalizar/cancelar,
no al abrir un wizard que todavía puede abandonarse. El eje agrupa por producto en unidad base, recorre la
familia de backorders y devoluciones/correcciones con signo. arg_closed_quantity_base conserva faltante explícito
de cancelación o no-backorder, incluso cuando Odoo no crea otro movimiento cancelado. No confundir retorno con
faltante cerrado. El pedido usa qty_delivered/qty_received nativos y la política to_refund; servicios físicosNA.

Validación/cancelación requieren responsable ARG y acceso nativo. Se protegen estados terminales, quants y
dimensiones, alias quant_id, relaciones padre y líneas comerciales contra cambios directos RPC. Una devolución
serializa el original y controla cantidad ya devuelta más lote actual. No se desactiva la comprobación de lotes
ni la lógica nativa de backorders; el formulario simple abre el detalle nativo.

Los puentes componen mediante super, conservan referencias reales y agregan acciones/vínculos/ejes físicos.
Locks SQL actualizan sólo metadatos del origen tras validar escritura del movimiento y compañía; no leen importes
ni usan sudo para consultar negocio oculto. Sirven para serializar recepción/entrega con cancelación/liberación.
La línea comercial de un movimiento se fija al crear: cambiarla exige otro movimiento. Se validan producto,
compañía, pedido confirmado o retorno y compromiso no liberado antes de finalizar.

## Inventario y concurrencia

INV y líneas agrupan conteo/evidencia. AJU es evidencia documental del efecto nativo, único por count_id; no libro
paralelo. Tomar referencia captura cantidad, huella de quants y revisión técnica por producto. La revisión es un
nonce sin cantidad monetaria/stock, cambiado por create/write/unlink de quant. Un UPDATE efectivo serializa aún
si antes no había quant y el competidor inserta uno; el aislamiento/reintento es el nativo PostgreSQL/Odoo.

Se bloquean también template y unidad antes de comparar revisiones para detectar cambios concurrentes de maestros.
Huella incorpora unidad/precisión/tracking/is_storable y metadatos de conteo nativo. Se validan todos los baselines
antes de mover la primera línea: los movimientos propios ya pueden avanzar revisiones después. El bloqueo por
producto es conservador entre ubicaciones/compañías compartidas; no publica cantidades de otros ámbitos.

Aplicar INV exige conteo cerrado, responsable y ACL nativas. Crea AJU con token Python privado, configura
inventory_quantity y llama action_apply_inventory/_apply_inventory. _get_inventory_move_values enlaza cada movimiento
al AJU mediante ese contexto privado. No escribe quantity directamente ni confirma una tabla de saldos propia.
Reintento abre adjustment_id; unicidadSQL previene doble AJU. Fallo/conflicto aborta toda transacción; no commits internos.
No diferencias implica documento de evidencia sin movimientos ficticios. Máximo500líneas por aplicación técnica.

## Compatibilidad y revisión

Odoo20 usa stock.move.uom_id y quantity; tracking=False significa seguimiento por cantidad, no 'none'. Devolución
está en stock.picking.action_return; no hay wizard stock.return.picking en este runtime. to_refund pertenece a
stock_account, por eso no se referencia desde la vista del core Stock sin esa dependencia.

La composición demo ya tenía puentes nativos sale_stock/purchase_stock instalados. Se inventarían pedidos/movimientos
antes de añadir los puentes ARG; no se afirma ausencia de efectos por conocer el nombre del addon. Cero operaciones
previas elimina en esta entrega la necesidad de migrar pedidos abiertos. Otras instalaciones requieren su preflight.
Instalación/arranque es control técnico. Escenarios quickstart y comprobación funcional de concurrencia/multiempresa/
permisos/cantidades quedan para QA posterior, según preferencia vigente. No se ejecutaron movimientos reales de ejemplo.

## F14 · Stock20.0.1.1.1 instalado en aislado y demo

`arg.pyme.stock.trace` abstracto expone options/reference/choices/page/quantities y acciones
from_lot/open_lot/open_document/advanced/create_lot. Contexto limpio compañía/lang/tz; rol Stock
ARG/admin y ACL nativas. Selectores/líneas/quants30; historial done por compañía y fecha/id.
Unidad base desde quantity_product_uom; no se calcula saldo sumando movimientos. lot.product_qty
y detalle de quants usan el mismo dominio nativo de ubicaciones, lote y contexto; ausencia de
permiso de cantidad/unidad produce no determinado. Related targets se autorizan antes de nombrarlos.

`arg.pyme.lot.create` transitorio toma producto+número/ref opcional y devuelve el lote nativo
creado. Protege resultado de vals/context/ir.default, bloquea la fila para reintentos y conserva
el resultado. El alta completada queda inmutable. Extensión stock.lot.create/write de identidad
toma el lock técnico de productos existentes/nuevos antes de super(), con permisos nativos;
no exige roles ARG a todos los consumidores nativos. Afecta al maestro usado por Stock/POS,
sin tablas de saldo nuevas ni escrituras de cantidad. Concurrencia funcional aún sin QA.

OWL conserva entradas, rango aplicado y páginas al navegar; paginar no aplica fechas pendientes.
DateTimeInput nativo presenta zona local y transmite UTC. Quantresult lleva unidad propia, aunque
el historial esté restringido. Ficha/traza avanzada usan acciones nativas, sin impresión automática.
Wiring/manifest/ACL y delta fuente fueron revisados por otra sesión de la misma familia/cuenta;
no es auditoría externa. Controles técnicos y límites en [entrega](../entregas/008-trazabilidad.md).

Stock ARG implica `stock.group_production_lot` desde20.0.1.1.1 para habilitar los campos nativos
de lote/serie en movimientos. El upgrade propaga el grupo a los usuarios actuales de Stock ARG.
La comprobación técnica de grupos no ejecuta movimientos ni cambia seguimiento por producto.
