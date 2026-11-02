# Stock ARG — guía de uso

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Addon 20.0.1.0.3 y puentes Ventas–Stock/Compras–Stock 20.0.1.0.1. QA funcional y aceptación pendientes.

## Existencias

En Stock → Existencias elegí depósito y, si hace falta, ubicación o producto. Cada fila conserva su unidad.
**Físico** es cantidad actual; **Reservado** proviene de reservas nativas; **Disponible** es cantidad utilizable;
**Previsto** incorpora entradas/salidas pendientes. Otras restricciones, como vencimientos, pueden reducir lo
utilizable sin constituir una reserva. La consulta muestra compañía y fecha/hora UTC; no suma unidades distintas.
El listado pagina treinta productos y nunca guarda existencias desde una celda.

En Productos y servicios podés activar control de existencias. Elegí seguimiento por lote/serie sólo cuando
corresponda; no se exige para productos controlados por cantidad. Los servicios sin movimiento físico muestran
No corresponde en el eje de entrega/recepción, conservando sus políticas comerciales nativas.

## Movimientos y parciales

Desde Ventas/Pedidos, abrí **Entregas y devoluciones**; desde Compras/Pedidos, **Entradas y devoluciones**.
También existe Stock → Movimientos para entradas, salidas y transferencias. Cada documento tiene código propio:
REM, ENT, TRA, DCL o DCP. Elegí tipo, origen/destino y detalle; la compañía y el tipo se conservan una vez numerado.

Prepará el movimiento y revisá **Cantidad operada**. Lotes / detalle abre las operaciones nativas para series,
lotes y paquetes. Reservar disponible no equivale a mover físicamente. **Validar cantidades** requiere responsable.
El asistente nativo permite dejar pendiente mediante otro documento o cerrar expresamente lo que falta.
Un faltante cerrado no se presenta como cumplido. Los pendientes derivados y sus orígenes quedan enlazados.

Desde un movimiento validado, **Preparar devolución** crea otro documento. Proponer pendiente de devolución
ayuda a cargar la cantidad; revisala antes de validar. No puede devolverse más cantidad que la efectivamente
movida y disponible para ese origen. No se altera ni borra un movimiento terminado, ni se cambia su línea comercial.
Las correcciones de devolución conservan los enlaces; los indicadores netos se recalculan.

Los pedidos muestran cantidad entregada/recibida desde Odoo. Se mantiene la opción nativa de actualizar cantidades
comerciales al devolver (`to_refund`); por defecto está activa. Una devolución para cambio/otra política puede tratarse
diferente por decisión explícita. Desde una factura los vínculos físicos se rotulan como movimientos de sus pedidos
origen: no se afirma una imputación exacta factura–remito cuando la fuente nativa no la provee.

## Inventario INV y ajuste AJU

1. Creá INV para una ubicación interna y motivo. Agregá productos o usá Cargar ubicación en un conteo vacío.
2. Tomar referencia conserva el teórico, lote/serie, paquete y propietario. No mueve existencias.
3. Registrá cantidades y marcá Contado. Una cantidad cero explícita es diferente de una línea sin contar.
4. Cerrá el conteo. Un responsable aplica las diferencias; se crea AJU enlazado a movimientos nativos.

Si cambió stock, reserva, referencia o unidad mientras contabas, no se sobrescribe la cantidad nueva: conservá
el conteo y prepará uno actualizado. Los bloqueos de revisión son conservadores por producto, por lo que un
movimiento de ese producto en otra ubicación también puede pedir actualizar el conteo. La aplicación es atómica;
un reintento abre el mismo AJU. Un conteo sin diferencias conserva evidencia y no inventa movimientos.
Para series, cada línea admite cero o una unidad. Paquete y propietario son opcionales para el caso genérico.
Un conteo trabaja hasta quinientas líneas por aplicación; podés dividirlo en documentos por ubicación o subconjunto.
Si hay quants duplicados o un conteo nativo pendiente, resolvelos antes de tomar una referencia nueva.

## Ayuda y límites

Las existencias sólo cambian mediante movimientos/ajustes del motor nativo. No se permite reasignar cantidades,
lotes, propietarios o paquetes mediante edición directa de quants; usá las operaciones nativas correspondientes.
Las operaciones terminadas conservan su detalle. Transferencias internas cambian ubicación y son neutras para
el total de compañía. Los cobros/pagos siguen perteneciendo a Administración, no a Stock.
Guía y tutoriales se mantienen por módulo/versión desde Ayuda ARG; no se inventan videos ni destinos de soporte.
