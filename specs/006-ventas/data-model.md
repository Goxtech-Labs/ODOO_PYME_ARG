# Data model: Circuito Ventas ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Presupuesto | `arg.pyme.quotation y arg.pyme.quotation.line` | PRE, cliente, moneda, fechas, líneas, condiciones, revisión | Documento propio distinto del pedido; confirmar no mueve stock ni dinero |
| Pedido | `sale.order y sale.order.line extendidos` | PED, arg_quotation_id, arg_quotation_line_id, generation_key, cantidades y condiciones | Varios pedidos parciales por presupuesto; generación idempotente por operación y control de cantidades por raíz/revisión |
| Derivados | `stock.picking y account.move` | relaciones nativas de líneas y accesos a Administración | No duplicar movimientos ni usar origin textual como único vínculo |

## Estados, efectos y seguridad

- Estados de presupuesto: borrador, emitido, parcialmente confirmado, confirmado, rechazado, vencido y cancelado; registrar revisión al cambiar condiciones confirmadas.
- Generar pedido mediante acción explícita; ofrecer confirmar y generar como acción combinada sólo si explica ambos efectos.
- Asignar PRE al presupuesto y PED al pedido; conservar numeración fiscal separada.
- Conservar sale.order como única fuente operativa de pedidos, entregas y facturación.
- Mantener bloqueo idempotente contra doble clic o concurrencia en generación del pedido.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.

Usar accepted_quantity, ordered_quantity_net, commercial_root_id, commercial_line_key y relación order_ids. Las condiciones aceptadas tienen snapshot histórico según contrato PRE/PED v1.1; no basta conservar IDs de maestros.

## Diseño de implementación fijado

- Identidad común: arg_identity_id/arg_number del mixin. PRE tiene compañía, tercero opcional en borrador, direcciones, tarifa/moneda, pago, posición fiscal, modo fiscal documental y fecha/tasa conocidas.
- target_quantity_total es cantidad objetivo acumulada; accepted_target_total incluye compromiso arrastrado, y ordered_quantity_net se consulta desde líneas PED de toda la raíz, incluidos cancelados todavía no liberados.
- Cada revisión conserva carried_commitments con IDs/cantidades y condiciones de los PED previos. Su precio nuevo se aplica al saldo target-carried; la impresión separa compromisos anteriores del saldo propuesto. Si se libera alguno de esos compromisos previos, exigir una nueva revisión antes de aceptar/generar, para no aplicar condiciones nuevas a cantidades aceptadas bajo otras condiciones.
- Eventos aceptación/liberación inmutables, claves y hashes de payload. Actualización efectiva de auditoría de raíz para serialización REPEATABLE READ, unicidad SQL complementaria; buscar reintento ya confirmado antes de rechazar por estado/revisión posterior.
- El wizard asigna UUID de operación al crearse y lo conserva al reintentar. Confirmación PRE no llama sale.order.action_confirm ni crea PED.
- Snapshot desde primera aceptación: nombres/domicilios, pago, posición fiscal, tarifa, moneda/tasa/fecha, impuestos/definiciones/importes por línea. Cambios de maestros no reescriben evidencia. Antes de generar, verificar compatibilidad de los impuestos actuales, no forzar motores fiscales.
- El grupo Ventas ARG comparte pedidos derivados ARG dentro de sus compañías para que los compromisos de una raíz no queden ocultos por la regla nativa de vendedor propio. Mantener restricciones globales multiempresa; no usar sudo para generar pedidos ni sumar cantidades invisibles.
- Valores calculados por account.tax nativo20. Terms con descuento fiscal mixto requieren adaptación específica: rechazar de forma explícita si no se puede conservar equivalencia, sin cálculo aproximado.
- La secuencia de implementación del puente físico queda pendiente hasta Stock ARG; no marcar T012 ni capacidades físicas como completas antes de instalarlo.
