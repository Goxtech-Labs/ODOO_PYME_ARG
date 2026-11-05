# Contrato · Servicios recurrentes, reservas y expedientes ARG

## Entrada mínima

Crear expediente o servicio con cliente y concepto; periodicidad/recurso sólo si corresponde. Fecha de hoy propuesta, tipo desde la tarea y número automático; conservar valores existentes.

## Efectos y límites

Recurrencia genera borradores idempotentes por período; reservas de agenda no son reservas de stock ni cobros. Documentos emitidos conservan origen y evidencia.

- Un abono genera como máximo una ocurrencia efectiva por período y compañía.
- No publicar factura ni cobrar automáticamente por ejecutar el planificador inicial.
- Una reserva no supera la capacidad del recurso ni solapa en concurrencia sin regla de capacidad.
- Cancelar una reserva no borra una factura ni libera stock no vinculado.

## Flujo

Expediente → contrato/abono o reserva → prestación → propuesta de documento comercial → factura/cobro existentes.
Validar permiso/compañía, precondición y clave estable de operación; confirmar atómicamente identidad,
evento y efecto. Los errores no dejan marcas de completado. Frente a operación externa incierta,
consultar estado antes de repetir mediante Integraciones ARG. No enviar al cargar ni abrir pantalla.

## Escenario de referencia

Generar dos veces el mismo período produce un borrador. Dos reservas simultáneas del mismo recurso/capacidad1 no se confirman ambas. El expediente conserva los enlaces al cancelar.

## Contratos compartidos

- [Interfaz](../../001-pyme-argentina/contracts/interfaz.md).
- [Administración](../../009-administracion/contracts/operaciones.md).
- [Integraciones](../../012-integraciones/contracts/operaciones.md).
- [Documento](../../015-documentos/contracts/operaciones.md).
