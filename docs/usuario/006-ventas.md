# Ventas ARG — guía de uso

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Versión del addon: 20.0.1.0.4. Circuito comercial, puente físico y dinero aplicado instalados; QA funcional y aceptación pendientes.

## Recorrido documental

**PRE → PED → FAC**. El presupuesto y el pedido son documentos distintos, con número propio.
En Gestión ARG → Ventas → Presupuestos, elegí cliente, fecha y productos con cantidad y precio.
La moneda, lista, direcciones y condición de pago conocidas se proponen desde el cliente; se pueden
corregir antes de aceptar. Guardar conserva el borrador. Emitir prepara el presupuesto para su aceptación.

El responsable usa **Confirmar cantidades** para aceptar todo o parte del detalle. Esta acción conserva
las condiciones acordadas; todavía no genera un pedido ni mueve existencias o dinero. Después,
**Generar pedido** permite elegir cantidades aceptadas todavía disponibles. Cada operación crea un
PED independiente en borrador. Confirmar ese pedido es otra acción del responsable.

## Pendientes y parciales

Cada documento muestra su propio estado y los ejes que le corresponden. Un presupuesto puede estar
confirmado parcialmente y tener pedidos generados parcialmente. El pedido distingue su confirmación
de la facturación publicada. Los documentos relacionados explican cada avance.

Ejemplo preparado para revisión posterior: presupuesto de 10 unidades, pedido de 4 y nueva revisión
para las 6 restantes. La revisión conserva objetivo acumulado 10 y compromiso previo 4. Su precio nuevo
se aplica a las 6 pendientes; las 4 anteriores mantienen sus condiciones. No se vuelve a pedir lo comprometido.
Un servicio sin movimiento físico no debe mostrarse pendiente de entrega.

## Cambiar condiciones y cancelar

Antes de la primera aceptación podés editar el presupuesto. **Actualizar desde lista** reemplaza precios
e impuestos explícitamente; no se actualizan silenciosamente precios aceptados. Después de aceptar,
**Nueva revisión** conserva la historia y permite negociar el saldo. El cliente, moneda, producto y unidad
de un compromiso previo se conservan.

Cancelar un PED no libera automáticamente su cantidad para generar otro. El responsable debe usar
**Liberar compromiso**, indicar el motivo y resolver cualquier entrega o factura existente. Se conserva
el documento cancelado y el registro de liberación. Si cambió un compromiso arrastrado, creá una revisión
para acordar el saldo actualizado.

## Facturas e importes

**Preparar factura** abre el circuito contable nativo desde un pedido confirmado; la política de facturación
del producto sigue vigente. La entrega inicial admite un PED por preparación de factura.
Publicar o revertir requiere responsable ARG y los permisos contables nativos. FAC y NCV tienen código
interno propio; ese número no reemplaza el fiscal. Esta entrega no emite CAE ni comprobantes fiscales reales.

**Cancelación de deuda** muestra cuánto residual fue saldado. Puede incluir notas de crédito o ajustes;
no representa necesariamente dinero cobrado. Administración ARG aporta recibos y dinero aplicado sobre
lo facturado. El botón correspondiente prepara el recibo; confirmar registra el efecto. Si el addon no está
instalado, informa esa dependencia.

## Alcance de esta entrega

Incluye productos y servicios genéricos con unidad base. Talles, combos y otras políticas especializadas
se incorporan mediante sus módulos. El descuento de pronto pago con tratamiento fiscal mixto necesita
un adaptador y no se acepta silenciosamente. Las cotizaciones multimoneda deben estar configuradas
para la compañía y fecha; no se inventa una conversión 1 a 1 si faltan.

La entrega física, remitos, devoluciones y sus parciales requieren el puente Ventas–Stock ARG.
En esta composición el puente está instalado. Instalar Ventas sin ese puente no habilita sus controles.

## Ayuda

Ayuda ARG ofrece la guía por módulo. El catálogo permite vincular videos YouTube por versión sin
reinstalar el addon. Hasta que el responsable configure el canal y los tutoriales reales, esta guía es
la referencia disponible; no se inventan enlaces ni se envían mensajes de soporte automáticamente.

Actualización008: puente físico instalado. Ver [Stock ARG](008-stock.md) para movimientos, devoluciones y pendientes; QA funcional sigue pendiente.

Actualización009: [Administración ARG](009-administracion.md) instalada. El botón de Administración en FAC/FRC prepara REC/OPA con datos conocidos; no registra dinero hasta confirmar. Dinero aplicado sobre lo facturado admite pendiente/parcial/completo y No determinado cuando falta evidencia. QA funcional pendiente.
