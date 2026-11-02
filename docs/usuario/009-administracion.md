# Administración ARG

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Administración reúne cuentas de clientes/proveedores, recibos REC, órdenes de pago OPA,
aplicaciones y consulta de caja/banco. Versión20.0.1.1.1 instalada técnicamente en la demo;
QA funcional/visual y aceptación pendientes. Los ejemplos siguientes no se ejecutaron.

## Consultar deuda y crédito

Abrí Administración → Cuentas de clientes o Cuentas de proveedores. La lista muestra apuntes
publicados por vencimiento, agrupados inicialmente por compañía y moneda, con filtro Con saldo.
Buscá por tercero, documento o descripción; usá Vencidos con saldo para revisar vencimientos.
Cada fila es un apunte/cuota: tres cuotas de una factura son tres vencimientos, sin repetir su total.

Saldo positivo representa deuda del cliente o deuda a pagar al proveedor, según la consulta.
Saldo negativo representa crédito/anticipo. Los importes conservan su moneda; no se suman ARS y USD.
Quitá Con saldo para consultar operaciones ya saldadas. Documento de origen abre el comprobante.
Pendiente, parcial y saldado indican cancelación de deuda: una nota o ajuste puede saldarla sin dinero.

## Preparar un recibo o una orden de pago

Abrí Recibos o Órdenes de pago y elegí Nuevo. Completá tercero → fecha/moneda → medios e importes.
La compañía y el medio predeterminado se completan desde configuración. Elegí las facturas a aplicar
si el dinero corresponde a deuda existente; sin facturas se registra un anticipo al confirmar.
Desde una FAC o FRC publicada, la acción de cobro/pago prepara un documento nuevo con los datos conocidos.
Una factura sin deuda pendiente dirige a la consulta de cuenta; no crea dinero automáticamente.

Guardar prepara el borrador con su código REC-000001 u OPA-000001. **Confirmar registra dinero y
contabilidad** mediante pagos nativos; requiere Responsable Administración ARG. Elegí correctamente
el medio antes de confirmar. Registrar una transferencia manual no la ejecuta en el banco.
El documento confirmado conserva datos históricos y no permite editar sus medios/importes.
Un borrador puede cancelarse conservando su número; un confirmado se corrige con reversión.

## Leer y aplicar el saldo

El documento conserva su estado propio y muestra aplicación pendiente, parcial o completa,
importe aplicado y libre por aplicar. Un REC confirmado de$100.000 con$60.000 aplicados muestra
Aplicado parcialmente y$40.000 libres. Es un único ingreso, aunque cubra varias facturas.
Un REC en borrador no cambia el cobro de una factura. Un anticipo confirmado está pendiente de aplicar.

Aplicar saldo permite elegir una factura publicada del mismo tercero y compañía. Aplica el menor
entre saldo libre y deuda, por vencimiento; el resto sigue libre o pendiente. La primera versión
no ofrece un importe arbitrario en ese diálogo: prepará el recibo por el importe deseado.
Cada medio genera su pago nativo; un excedente queda libre como anticipo, sin generar otra deuda.
Las solapas muestran aplicaciones vigentes, pagos/asientos e historial con actor y fecha.

Desaplicar libera las conciliaciones que tenía el documento al abrir el diálogo y pide un motivo.
El dinero continúa registrado y queda disponible para otra aplicación. Repetir la misma operación
no debe borrar aplicaciones posteriores. **Revertir** pide fecha y motivo, genera asientos inversos,
libera sus aplicaciones y conserva el original y su historia. Si existe conciliación bancaria de
la liquidez, el sistema pide revisarla antes de revertir. Son acciones del responsable.

## Caja, banco y dinero aplicado

Caja y banco consulta apuntes publicados de cuentas de liquidez, filtrables por diario, cuenta,
fecha, compañía y moneda. Registros de cobro y pago muestra también pagos en cuentas transitorias,
su asiento y si el efecto está registrado, revertido o requiere revisión. Un registro de transferencia
en una cuenta transitoria no acredita por sí solo un movimiento en la cuenta bancaria.

FAC/FRC distingue deuda saldada de dinero aplicado. Notas, compensaciones, descuentos y diferencias
no se presentan automáticamente como dinero. Si falta evidencia para determinarlo, aparece
No determinado con explicación y el importe demostrable; no se inventa un cero.
PED/PPC indica dinero sobre lo facturado y mantiene aparte el alcance pendiente de facturación.
Consultar la [guía de estados](ESTADOS-DOCUMENTALES.md) para todos los ejes y parciales.

## Configuración y permisos

Operación Administración ARG consulta y prepara borradores; incluye lectura contable nativa.
Responsable Administración ARG confirma, aplica, desaplica y revierte, con permisos contables nativos.
Administrador ARG incluye al responsable. Se respetan las compañías habilitadas y reglas existentes;
otros grupos del usuario pueden otorgar permisos adicionales.

Antes de confirmar, configurá medios manuales de entrada/salida para diarios caja/banco de la compañía,
sus cuentas explícitas de pago y la moneda compatible del diario. La compañía permite elegir medios
predeterminados. Monedas distintas requieren cotizaciones explícitas; el sistema no inventa cotización.
En la demo están Caja de ejemplo ARG y Banco de ejemplo ARG, sin credenciales ni datos fiscales reales.
Cheques, ejecución bancaria, conciliación automática e integraciones quedan para incrementos posteriores.

Tutorial YouTube pendiente de publicación. Ayuda contiene guía escrita para Odoo20; no se inventan enlaces.
