# Contrato · Obras, capítulos y costos ARG

## Entrada mínima

Crear obra con cliente, nombre y fecha; agregar capítulos cuando hagan falta. Fecha de hoy propuesta, tipo desde la tarea y número automático; conservar valores existentes.

## Efectos y límites

Costos reales desde compras, consumos y horas nativos; distinguir comprometido, devengado y pagado. No sumar dos veces compra y consumo del mismo material.

- Material comprado para depósito y material consumido en obra son hechos distintos.
- Costo previsto, real, facturado y pagado no se suman como una misma medida.
- Cambiar la tarifa vigente no reescribe horas ni presupuestos aceptados.
- Una obra admite un operador con roles combinados.

## Flujo

Presupuesto de obra → capítulos → compras/consumos/horas → avance → facturación por capítulos o hitos → cierre.
Validar permiso/compañía, precondición y clave estable de operación; confirmar atómicamente identidad,
evento y efecto. Los errores no dejan marcas de completado. Frente a operación externa incierta,
consultar estado antes de repetir mediante Integraciones ARG. No enviar al cargar ni abrir pantalla.

## Escenario de referencia

Obra con dos capítulos: consumir material sólo en uno, registrar horas, comparar previsto/real y facturar un hito sin repetir costo ni consumo.

## Contratos compartidos

- [Interfaz](../../001-pyme-argentina/contracts/interfaz.md).
- [Administración](../../009-administracion/contracts/operaciones.md).
- [Integraciones](../../012-integraciones/contracts/operaciones.md).
- [Documento](../../015-documentos/contracts/operaciones.md).
