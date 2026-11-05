# Contrato · Fabricación y artículos compuestos ARG

## Entrada mínima

Seleccionar producto, cantidad y fecha; deducir lista de materiales configurada. Fecha de hoy propuesta, tipo desde la tarea y número automático; conservar valores existentes.

## Efectos y límites

Usar orden, consumos, producción, lotes y valoración nativos. Un kit comercial no registra producción ficticia.

- No escribir quants ni inventar un segundo libro de materiales.
- Fabricación parcial conserva cantidad pendiente y origen de componentes.
- Un kit y un producto fabricado no activan simultáneamente doble consumo.
- Un cambio de receta no modifica producción ya terminada.

## Flujo

Preparación → disponibilidad → orden → consumos/producción efectivos → terminación o cancelación.
Validar permiso/compañía, precondición y clave estable de operación; confirmar atómicamente identidad,
evento y efecto. Los errores no dejan marcas de completado. Frente a operación externa incierta,
consultar estado antes de repetir mediante Integraciones ARG. No enviar al cargar ni abrir pantalla.

## Escenario de referencia

Fabricar parcialmente dos de tres unidades con consumo trazable; cerrar o continuar el saldo explícitamente y verificar que vender un kit no duplica consumos.

## Contratos compartidos

- [Interfaz](../../001-pyme-argentina/contracts/interfaz.md).
- [Administración](../../009-administracion/contracts/operaciones.md).
- [Integraciones](../../012-integraciones/contracts/operaciones.md).
- [Documento](../../015-documentos/contracts/operaciones.md).
