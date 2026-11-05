# Contrato · Punto de venta ARG

## Entrada mínima

Abrir sesión autorizada, elegir artículos/cantidades y medios; fecha/hora nativas automáticas. Fecha de hoy propuesta, tipo desde la tarea y número automático; conservar valores existentes.

## Efectos y límites

Conservar pagos, stock, impuestos y asientos del POS nativo; puentes ARG sólo enlazan y clasifican. No crear REC duplicado por cada pago ya registrado por POS.

- Un cobro y un movimiento POS se registran una sola vez aunque exista enlace ARG.
- Un ticket no acredita autorización fiscal.
- Devolución y devolución de dinero son efectos separados con origen.
- La cuenta de demo no determina los permisos definitivos de cajero.

## Flujo

Sesión → venta → cobro → ticket/factura según caso → devolución → cierre y conciliación.
Validar permiso/compañía, precondición y clave estable de operación; confirmar atómicamente identidad,
evento y efecto. Los errores no dejan marcas de completado. Frente a operación externa incierta,
consultar estado antes de repetir mediante Integraciones ARG. No enviar al cargar ni abrir pantalla.

## Escenario de referencia

Pedido POS con dos medios y devolución parcial conserva un único cobro/stock; cierre diferencia efectivo contado de saldo esperado y factura vinculada no duplica venta.

## Contratos compartidos

- [Interfaz](../../001-pyme-argentina/contracts/interfaz.md).
- [Administración](../../009-administracion/contracts/operaciones.md).
- [Integraciones](../../012-integraciones/contracts/operaciones.md).
- [Documento](../../015-documentos/contracts/operaciones.md).
