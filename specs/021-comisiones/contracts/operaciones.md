# Contrato · Agentes y comisiones ARG

## Entrada mínima

Elegir agente, regla y período; mostrar propuesta antes de liquidar. Fecha de hoy propuesta, tipo desde la tarea y número automático; conservar valores existentes.

## Efectos y límites

Base explícita por facturación neta o cobro efectivo aplicado; separar comisión devengada de pagada y conservar devoluciones/rechazos. Regla inicial propuesta por facturación neta, seleccionable por compañía antes de activar.

- Una línea fuente y regla no devengan dos veces por reintento.
- Una liquidación confirmada conserva base y porcentaje históricos.
- Un cheque recibido sin acreditar no es cobro efectivo para una regla basada en liquidez.
- La liquidación no envía dinero; la OPA conserva su propia ejecución.

## Flujo

Regla versionada → devengamiento por fuente elegida → propuesta → liquidación → pago por OPA → ajustes.
Validar permiso/compañía, precondición y clave estable de operación; confirmar atómicamente identidad,
evento y efecto. Los errores no dejan marcas de completado. Frente a operación externa incierta,
consultar estado antes de repetir mediante Integraciones ARG. No enviar al cargar ni abrir pantalla.

## Escenario de referencia

Liquidar una factura y su devolución parcial; la segunda ejecución no duplica comisión. Para base cobro efectivo, la recepción de cheque no devenga hasta el evento previsto.

## Contratos compartidos

- [Interfaz](../../001-pyme-argentina/contracts/interfaz.md).
- [Administración](../../009-administracion/contracts/operaciones.md).
- [Integraciones](../../012-integraciones/contracts/operaciones.md).
- [Documento](../../015-documentos/contracts/operaciones.md).
