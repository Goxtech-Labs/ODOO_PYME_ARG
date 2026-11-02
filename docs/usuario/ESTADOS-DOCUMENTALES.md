# Cómo leer los estados de un documento ARG

Cada documento tiene un estado propio y muestra por separado el avance de las operaciones que le corresponden.
Las etiquetas se presentan siempre en el mismo orden: confirmación → entrega o recepción → facturación → cobro o pago.
Recibos y órdenes de pago muestran además su aplicación. Cada pendiente permite abrir el detalle que lo explica.

| Operación | Sin avance | Parte realizada | Terminada |
| --- | --- | --- | --- |
| Confirmar presupuesto | Pendiente de confirmar | Confirmado parcialmente | Confirmado |
| Generar pedidos desde presupuesto | Pendiente de generar pedido | Pedido generado parcialmente | Pedidos generados |
| Entregar pedido de cliente | Pendiente de entregar | Entregado parcialmente | Entregado |
| Recibir pedido al proveedor | Pendiente de recibir | Recibido parcialmente | Recibido |
| Facturar | Pendiente de facturar | Facturado parcialmente | Facturado |
| Cobrar factura de venta | Pendiente de cobro | Cobrado parcialmente | Cobrado |
| Pagar factura del proveedor | Pendiente de pago | Pagado parcialmente | Pagado |
| Aplicar recibo u orden de pago | Pendiente de aplicar | Aplicado parcialmente | Aplicado |

Estas son las etiquetas funcionales del contrato. El encabezado común también puede resumirlas como
«Entrega: Parcial» o «Facturación: Pendiente». Sólo aparecen los ejes aplicables al tipo documental.
La confirmación técnica del pedido o la publicación de la factura conservan su estado nativo;
el avance parcial corresponde a cantidades o importes efectivamente aceptados, entregados, facturados o aplicados.

## Ejemplo de un pedido

PED-000001 solicita 10 unidades de un mismo producto y está confirmado.
Se entregaron 4 y se facturaron 2: muestra **Confirmado · Entregado parcialmente · Facturado parcialmente**.
En el detalle de entrega se ve realizado 4, pendiente 6 y los remitos relacionados.
En facturación se ve realizado 2, pendiente 8 y las facturas relacionadas.

Si se cobró toda la factura de esas 2 unidades, la factura muestra **Cobrado**.
El pedido distingue **cobro sobre lo facturado** y **alcance facturado del pedido**: quedan 8 unidades por facturar.
Los números son un ejemplo de lectura, no operaciones ejecutadas en la demo.

## Ejemplo de un recibo

REC-000001 registra un ingreso de $100.000. Se aplicaron $60.000 a una factura:
**Aplicado parcialmente**, con $40.000 libres para aplicar posteriormente.
Aplicar el mismo recibo a varias facturas conserva un único ingreso de dinero.
Un anticipo sin factura comienza pendiente de aplicar, aunque el ingreso ya esté confirmado.

En una factura, «pendiente de recibo» significa **Pendiente de cobro**. Crear un recibo en borrador
no la cobra. Si la factura es de$100.000 y se aplican$40.000 de un recibo confirmado, muestra
**Cobrado parcialmente**, con$60.000 pendientes y el recibo vinculado. Puede haber varios recibos
para una factura y un mismo recibo aplicado a varias facturas. Para proveedores funciona igual
con órdenes de pago y las etiquetas Pendiente de pago, Pagado parcialmente y Pagado.

## Correcciones y excepciones

Las etiquetas se calculan desde los documentos y operaciones vinculados; el usuario registra la operación,
sin tener que volver a escribir el estado. Devoluciones, notas, reversiones y desaplicaciones actualizan
el eje afectado y conservan su explicación histórica.

Si se entregan 4 de 10 y se cancelan las otras 6, se muestra **Cerrado con faltante**, junto con el avance real.
Un servicio sin entrega física muestra **No corresponde** en entrega.
Una deuda saldada con una nota de crédito o un ajuste conserva esa explicación: no acredita dinero cobrado.
Cantidades se comparan por línea y unidad; importes por moneda, sin sumar ARS y USD.
Si no se puede demostrar cuánto dinero se aplicó, aparece **No determinado** con su explicación;
no se inventa un importe cero ni se presenta la deuda saldada como dinero cobrado.

Consultar [Documentos ARG](015-documentos.md) y el [contrato técnico de estados](../tecnica/ESTADOS-Y-PENDIENTES.md).
Los ejes monetarios requieren Administración009, instalada técnicamente en la demo; QA funcional y aceptación siguen pendientes.
