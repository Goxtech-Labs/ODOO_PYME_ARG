# Contrato · Reparaciones y servicio técnico ARG

## Entrada mínima

Registrar cliente, equipo y síntoma con fecha de hoy, sin exigir diagnóstico ni técnico al recibir. Fecha de hoy propuesta, tipo desde la tarea y número automático; conservar valores existentes.

## Efectos y límites

Consumir/devolver repuestos mediante stock nativo; mano de obra como servicio; facturar desde el documento comercial vinculado sin duplicar pedido ni consumo.

- El equipo del cliente no aumenta stock propio ni su valoración.
- Confirmar el diagnóstico no factura ni consume repuestos.
- Cada consumo, devolución y factura conserva su origen por línea.
- Garantía y presupuesto aceptado son condiciones explícitas; no se inventan por fecha.

## Flujo

Recepción → diagnóstico → presupuesto vinculado → autorización → trabajo → listo → entrega; facturación y cobro por ejes independientes.
Validar permiso/compañía, precondición y clave estable de operación; confirmar atómicamente identidad,
evento y efecto. Los errores no dejan marcas de completado. Frente a operación externa incierta,
consultar estado antes de repetir mediante Integraciones ARG. No enviar al cargar ni abrir pantalla.

## Escenario de referencia

Recibir equipo, presupuestar, autorizar, usar un repuesto y dos horas; entregar y facturar una sola vez. Cancelar antes del trabajo no mueve stock; devolver un repuesto deja movimiento inverso trazable.

## Contratos compartidos

- [Interfaz](../../001-pyme-argentina/contracts/interfaz.md).
- [Administración](../../009-administracion/contracts/operaciones.md).
- [Integraciones](../../012-integraciones/contracts/operaciones.md).
- [Documento](../../015-documentos/contracts/operaciones.md).
