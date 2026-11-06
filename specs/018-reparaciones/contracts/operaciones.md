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

## Subcircuito de recepción implementado en fuente

Nuevo → borrador REP; Recibir registra fecha/cliente/equipo/síntoma/condiciones y entra en received.
Fecha futura puede guardarse como borrador, pero no afirmar una recepción efectiva. Diagnóstico
se completa después de recibir; Registrar diagnóstico conserva evidencia y pasa a diagnosed.
No autoriza trabajo, no genera PRE/PED ni consume existencias. Cancelar sólo afecta draft.

Devolver sin reparar desde received/diagnosed exige fecha efectiva, receptor y motivo. La fecha
no precede al último hecho ni es futura. Registra return y cierra custodia en returned, sin afirmar
trabajo terminado ni diagnóstico realizado si falta. Operaciones registradas no se borran. Repetir
la misma acción no duplica el evento; repetir una devolución con distinta constancia se rechaza.

El incremento no permite aún corregir una recepción/diagnóstico confirmado; esa corrección futura
será explícita y preservará el original. Presupuesto/autorización/intervenciones/stock/factura y
entrega reparada continúan en el contrato completo; este subcircuito no los sustituye.

## Incremento de trabajo1.1

El código agrega PRE/PED, autorización, repuestos nativos, PTM, listo/retomar/entrega reparada y
vínculos de factura/cobro. Aplicar [trabajo-autorizado.md](trabajo-autorizado.md), sin atribuir instalación.
