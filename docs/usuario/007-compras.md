# Compras ARG — guía de uso

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Circuito comercial, puente físico y dinero aplicado instalados; QA funcional y aceptación pendientes.
El ajuste de carga20.0.1.0.6 está preparado en fuente, pendiente de instalación.

## Pedido al proveedor

En Gestión ARG → Compras → Pedidos al proveedor, revisá la fecha propuesta, elegí proveedor y productos con cantidad y precio.
Las condiciones conocidas del proveedor se proponen al crear. Moneda, impuestos y condición de pago se
pueden revisar antes de confirmar. Guardar asigna `PPC-000001`; la referencia del proveedor se conserva aparte.
Confirmar requiere responsable ARG. Si la empresa configura doble aprobación, el pedido queda Por aprobar
hasta que un responsable con permiso nativo de aprobación lo apruebe.

El pedido conserva condiciones, líneas y totales acordados. Las referencias y fechas logísticas pueden completarse
sin cambiar el acuerdo. Para renegociar, el responsable cancela y vuelve a borrador sólo si no existen facturas
activas y las condiciones nativas de cancelación lo permiten. Se conserva el número y la historia; no se borra.

## Factura recibida parcial

Desde un pedido confirmado, **Preparar factura recibida** propone cantidades pendientes según la política del
producto. Elegí cuánto facturar ahora; cero excluye una línea. Al confirmar la selección se crea una **FRC en
borrador**, con relación real al PPC y sus líneas. Un reintento de esa operación devuelve la misma factura.
Si existe otra factura borrador vinculada, resolvela antes de preparar una nueva.

En la factura completá la fecha y el **número original del proveedor** antes de publicar. El código FRC interno
no reemplaza ese número. Publicar requiere responsable y permisos contables nativos. También podés registrar
una factura directa desde Facturas y notas recibidas, indicando que no procede de un pedido.

La disposición preparada20.0.1.0.6 presenta **fecha del comprobante → proveedor → número del
comprobante → artículos/conceptos**. La fecha nueva propone hoy; revisala si el documento recibido
tiene otra. Los datos tomados del pedido no se cargan de nuevo. FRC/NCP son códigos internos automáticos.
A la derecha quedan condiciones y contabilidad, conservando fecha contable, vencimiento, moneda,
diario y demás controles nativos. No se completan todas las fechas con hoy: cada una tiene su significado.
La misma ficha se abre desde menú, pedido o enlaces; incluye los recibos de proveedor nativos que
usen esa ficha, sin asignarles un nuevo código ARG. Este ajuste todavía no está instalado ni revisado visualmente.

Una factura vinculada no puede consumir cantidades de otro producto, usar otra unidad, superar el pedido o
lo recibido cuando así lo exige la política del producto. Los borradores no cuentan como facturación cumplida.
La publicación por lote comprueba el conjunto. Las facturas futuras programadas conservan la política nativa;
con cron desactivado en la demo no se publicarán automáticamente.

## Notas y pendientes

Las correcciones contables usan una nota vinculada mediante la acción nativa de reversión, conservando FRC
y NCP con números internos diferentes. Una nota vinculada al pedido no puede acreditar más unidades netas
que las facturadas. Una devolución física es otro documento y no se confunde con la nota contable.

El pedido distingue su confirmación de la facturación publicada. Cada eje muestra pendiente, parcial o completo
con sus cantidades y documentos explicativos. Un cierre con faltante no se presenta como cumplido.
**Cancelación de deuda** puede incluir notas o ajustes; no equivale necesariamente a dinero pagado. Los pagos,
órdenes de pago y anticipos se registran mediante Administración ARG, instalada en esta composición.

## Límites y ayuda

Esta entrega comercial usa productos/servicios genéricos y su unidad base. Los importes cero requieren aceptación
expresa. Las tasas multimoneda deben estar configuradas para la compañía y fecha; no se inventa un cambio1a1.
La recepción ENT, devolución DCP y sus parciales requieren el puente Compras–Stock ARG de la etapa Stock.
La facturación por recepción seguirá sin cantidades disponibles hasta registrar la recepción correspondiente.

Ayuda ARG ofrece primeros pasos. Los tutoriales YouTube reales se vinculan desde su catálogo por módulo y
versión cuando el responsable los configure; este manual sigue disponible sin contratar soporte.

Actualización008: puente físico instalado. Ver [Stock ARG](008-stock.md) para movimientos, devoluciones y pendientes; QA funcional sigue pendiente.

Actualización009: [Administración ARG](009-administracion.md) instalada. El botón de Administración en FAC/FRC prepara REC/OPA con datos conocidos; no registra dinero hasta confirmar. Dinero aplicado sobre lo facturado admite pendiente/parcial/completo y No determinado cuando falta evidencia. QA funcional pendiente.
