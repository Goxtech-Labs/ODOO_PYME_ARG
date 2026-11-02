# Estados y pendientes documentales ARG v1

Cada documento conserva su estado propio y ejes de cumplimiento independientes. Todo eje aplicable admite
**pendiente, parcial y completo** con cantidad/importe realizado y restante. No condensar todo en un solo estado.

| Documento | Estado / eje de confirmación | Ejes derivados |
| --- | --- | --- |
| PRE | Borrador, emitido; aceptación pendiente/parcial/confirmada; rechazado/vencido/cancelado | Generación de PED pendiente/parcial/completa |
| PED | Borrador/confirmado/cancelado; aceptación de líneas cuando corresponda | Entrega, facturación y cobro pendiente/parcial/completo |
| PPC | Borrador/por aprobar/confirmado/cancelado | Recepción, facturación recibida y pago pendiente/parcial/completo |
| REM/ENT | Preparado/validado/cancelado | Cantidades pendientes/parciales/completas y facturación vinculada |
| FAC/FRC | Borrador/publicado/revertido; fiscal independiente | Cobro/pago pendiente/parcial/completo |
| REC/OPA | Borrador/confirmado/revertido | Aplicación pendiente/parcial/completa; importe libre de anticipo |
| INV | Borrador/en conteo/contado/aplicado | Conteo y aplicación pendiente/parcial/completa por líneas |

Confirmar una operación atómica nativa no crea un estado técnico inventado: una entrega parcial se valida
por su cantidad efectiva y deja backorder/pendiente. La etiqueta comercial se deriva de cantidades, no reemplaza state nativo.
Una cancelación de faltante no significa cumplimiento: distinguir completo de cerrado con faltante.
No aplicar entrega a servicios que no la requieren; mostrar **No corresponde**, sin falso pendiente.
Un recibo aplicado a varias facturas se mide por importe aplicado, sin duplicar el dinero recibido.

Por línea: base elegible, realizado neto, pendiente abierto y faltante cerrado. Total por eje: pendiente si no hay avance,
completo si todas las líneas elegibles cumplen dentro de precisión, parcial en otro caso. No sumar unidades incompatibles.
Deuda pendiente por moneda y residual nativo: saldada sólo dentro de precisión monetaria.
Cobro/pago efectivo deriva de dinero aplicado mediante conciliación nativa, separando notas, ajustes,
diferencias de cambio y descuentos. Un residual cero no prueba caja. Separar crédito/anticipo libre.
Notas, devoluciones, cancelaciones y desaplicaciones recalculan el eje afectado conservando historial.
No escribir manualmente indicadores derivados. Detalle muestra documentos que explican cada cantidad/importe.

Ejemplo: PED confirmado, entrega 4/10 parcial, facturación 2/10 parcial y cobranza parcial sobre lo facturado.
No presentar como totalmente cobrado el pedido sólo porque está saldada la única factura parcial.
En pedido mostrar cobro sobre facturado y alcance facturado del pedido como dos indicadores distintos.

## Etiquetas visibles comunes

| Eje | Sin avance | Avance parcial | Cumplimiento total |
| --- | --- | --- | --- |
| Aceptación PRE | Pendiente de confirmar | Confirmado parcialmente | Confirmado |
| Entrega PED | Pendiente de entregar | Entregado parcialmente | Entregado |
| Recepción PPC | Pendiente de recibir | Recibido parcialmente | Recibido |
| Facturación | Pendiente de facturar | Facturado parcialmente | Facturado |
| Cobro FAC | Pendiente de cobro | Cobrado parcialmente | Cobrado |
| Pago FRC | Pendiente de pago | Pagado parcialmente | Pagado |
| Aplicación REC/OPA | Pendiente de aplicar | Aplicado parcialmente | Aplicado |

La etiqueta corresponde a su eje; mostrar varias juntas cuando sean aplicables.
El estado confirmado del pedido no cambia al registrar una entrega o una factura parcial.

## Recibos vinculados y calidad del dato

La expresión «pendiente de recibo» se presenta al usuario como **Pendiente de cobro**:
el hecho medido es dinero confirmado y aplicado a la factura, no la mera existencia de un REC.
Un REC en borrador no acredita cobro. Uno confirmado como anticipo acredita ingreso de dinero,
pero no el cobro de una factura hasta su aplicación. Un único REC puede cubrir varias facturas y
una factura puede recibir varios REC; medir importes nativos aplicados, sin contar vínculos como dinero.
Para proveedores aplicar el mismo criterio con OPA y el eje de pago.

Si la información o los permisos no permiten demostrar el importe monetario, mostrar
**No determinado**, conservar el importe comprobable y explicar qué falta. No sustituir un dato
desconocido por cero ni marcar cobro completo sólo porque el residual nativo de deuda sea cero.
Este estado expresa calidad de información; no es una cuarta etapa de avance.

## Orden visual y consulta

Mantener confirmación → entrega/recepción → facturación → cobro/pago en todos los documentos aplicables.
En REC/OPA mostrar aplicación y monto libre. Cada eje despliega realizado, pendiente abierto, faltante cerrado
y documentos fuente accesibles. El estado propio permanece visible junto a esos ejes.
Ver [guía de lectura](../usuario/ESTADOS-DOCUMENTALES.md) para etiquetas funcionales y ejemplos.

## Alcances que requieren evidencia adicional

Una factura compartida entre pedidos no atribuye su importe ni sus pagos a cada pedido.
Los ejes monetarios del pedido muestran No determinado y explican la falta de origen exclusivo;
no se reparte dinero por cantidades, importes o cantidad de relaciones. La factura conserva su
residual y aplicaciones comprobables. Lo mismo aplica cuando contiene líneas sin pedido de origen.

REM/ENT conserva su eje físico desde la demanda preparada. La relación nativa factura–pedido
no prueba qué entrega/recepción concreta se facturó: el eje Facturación vinculada muestra
No determinado y permite consultar facturas de pedidos relacionados sin atribuirlas al movimiento.
Su estado propio y cantidades físicas continúan independientes. Entrega/Recepción precede a
facturación y dinero; la falta de evidencia no se presenta como cero o cumplimiento.
