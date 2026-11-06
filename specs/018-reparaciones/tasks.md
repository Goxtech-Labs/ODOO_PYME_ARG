# Tasks: Reparaciones y servicio técnico ARG

Estado:1.2 instalada técnicamente en aislado, con circuito, correcciones/continuidad y reporte. Promoción a demo completada; QA/aceptación posteriores pendientes.


## Setup

- [x] T001 Inspeccionar candidato nativo, licencia/APIs y hooks de esta composición; registrar decisión en specs/018-reparaciones/research.md

## Foundation

- [x] T002 Fijar identidad, campos y transiciones del contrato en specs/018-reparaciones/data-model.md
- [x] T003 Crear manifest/dependencias opcionales sin ciclo ni core modificado en addons/arg_pyme_reparaciones/__manifest__.py

## US1

- [x] T004 [US1] Implementar carga básica, valores por contexto y las invariantes: El equipo del cliente no aumenta stock propio ni su valoración. Destino addons/arg_pyme_reparaciones/models/repair_case.py
- [x] T005 [US1] Crear roles y reglas multiempresa; sin sudo para operaciones del usuario en addons/arg_pyme_reparaciones/security/ir.access.csv
- [x] T006 [US1] Presentar fecha/tercero/documento/detalle y secundarios progresivos en addons/arg_pyme_reparaciones/views/repair_views.xml

## US2

- [x] T007 [US2] Implementar operaciones y relaciones descritas en contracts/operaciones.md con idempotencia/corrección; destino addons/arg_pyme_reparaciones/models/repair_intervention.py
- [x] T008 [US2] Implementar operaciones y relaciones descritas en contracts/operaciones.md con idempotencia/corrección; destino addons/arg_pyme_reparaciones/models/repair_stock_bridge.py
- [x] T009 [US2] Hacer cumplir en servidor: Confirmar el diagnóstico no factura ni consume repuestos.; Cada consumo, devolución y factura conserva su origen por línea.; Garantía y presupuesto aceptado son condiciones explícitas; no se inventan por fecha. Destino addons/arg_pyme_reparaciones/models/repair_commercial.py y repair_sales_bridge.py

## US3

- [x] T010 [US3] Exponer consulta/estados/origen y adaptador de hechos sin doble suma en addons/arg_pyme_reparaciones/models/report_adapter.py
- [x] T011 [US3] Crear informe/documento con moneda, estado y evidencia en addons/arg_pyme_reparaciones/report/repair_document.xml y work_document.xml

## Polish

- [ ] T012 Documentar manual, ejemplos, límites y ficha de tutorial versionada en docs/usuario/018-reparaciones.md
- [x] T013 Resolver sintaxis, carga de vistas e instalación/arranque de composición; registrar sin atribuir QA en docs/entregas/018-reparaciones.md
- [x] T014 Fijar paquete/versiones, respaldo y promoción autorizada con hashes en composition/versions.lock.json

## Dependencies & Execution Order

Setup → Foundation → US1 → US2 → US3 → Polish. US2 depende de contrato/roles US1; US3 usa efectos ya definidos.
MVP: carga y circuito mínimo completo, sin activar canales externos. No delegar escrituras de archivos compartidos en paralelo.

## Parallel Examples

Con contratos fijados, manual y recursos de ayuda pueden prepararse en archivos separados mientras se implementa cada historia.
US1: fichas/roles separados; US2: adaptadores separados sólo tras fijar interfaz; US3: manual e informe con grano acordado.

## Implementation Strategy

Entregas pequeñas completas y composición fijada. Las tareas de implementación permanecen sin marcar hasta evidencia de código/instalación.
QA funcional/visual y aceptación no forman parte del conteo de implementación; se registran después mediante quickstart.md.

## Incremento de recepción20.0.1.0.0

T004/T005/T006 tienen código de captura, roles y vistas; AST/XML/manifest/ACL y revisión estática
independiente sin bloqueantes. Instalación y comprobación del registro real aún pendientes.
T002 conserva el contrato completo y agrega submodelo de recepción; no fija aún todos los puentes.
T009 avanza con recepción y diagnóstico sin efectos físicos/comerciales; faltan las invariantes de
intervención. T010/T011 incluyen ejes/informe de custodia, sin reemplazar informes del circuito completo.
T012 tiene guía escrita y tutorial pendiente; T013/T014 no realizados. Parent016T015 sigue abierta.
No se crean productos, quants, asientos ni documentos comerciales desde la recepción.

## Incremento de trabajo20.0.1.1.0

T002/T007/T008/T009 avanzan con PRE/PED/autorización/PTM/stock nativo y entrega reparada; T010/T011
con ejes por fuente e impresión PTM. No instalados ni validados en circuito real. Correcciones de
recepción/diagnóstico, reportes completos, ejemplos/tutoría y T013/T014 continúan pendientes.
No marcar el alcance completo por un paquete estático. Parent016T015 permanece abierta.

## Incremento de correcciones20.0.1.2.0

Contrato y fuente agregan corrección de recepción/diagnóstico, nueva visita con REP independiente,
snapshot/UUID inmutables, vínculo real al hijo y reporte de hechos/pendientes. T002/T004–T011 tienen
fuente para su alcance; no regenerarla por estar pendientes las comprobaciones técnicas de registro.
Al preparar la fuente T013/T014 y los cargadores estaban pendientes. El 2026-11-06 se completó T013
en aislado y se cargaron borrador/catálogo ficticios. Las tareas marcadas acreditan código instalado,
no ejecución de sus recorridos ni PDF/QA. T012 conserva tutoriales y ejemplos de circuito pendientes;
T014 se completó con la promoción técnica a demo. Parent016T015 sigue abierta por T012.
[Promoción](../../docs/entregas/EXPANSION-PROMOCION.md). [Evidencia](../../docs/entregas/EXPANSION-INSTALACION-AISLADA.md).
