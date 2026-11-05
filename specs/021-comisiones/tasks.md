# Tasks: Agentes y comisiones ARG

Estado: pendientes; planificación no equivale a código instalado. QA/aceptación posteriores en quickstart.md.


## Setup

- [ ] T001 Inspeccionar candidato nativo, licencia/APIs y hooks de esta composición; registrar decisión en specs/021-comisiones/research.md

## Foundation

- [ ] T002 Fijar identidad, campos y transiciones del contrato en specs/021-comisiones/data-model.md
- [ ] T003 Crear manifest/dependencias opcionales sin ciclo ni core modificado en addons/arg_pyme_comisiones/__manifest__.py

## US1

- [ ] T004 [US1] Implementar carga básica, valores por contexto y las invariantes: Una línea fuente y regla no devengan dos veces por reintento. Destino addons/arg_pyme_comisiones/models/commission_rule.py
- [ ] T005 [US1] Crear roles y reglas multiempresa; sin sudo para operaciones del usuario en addons/arg_pyme_comisiones/security/ir.model.access.csv
- [ ] T006 [US1] Presentar fecha/tercero/documento/detalle y secundarios progresivos en addons/arg_pyme_comisiones/views/commission_views.xml

## US2

- [ ] T007 [US2] Implementar operaciones y relaciones descritas en contracts/operaciones.md con idempotencia/corrección; destino addons/arg_pyme_comisiones/models/commission_accrual.py
- [ ] T008 [US2] Implementar operaciones y relaciones descritas en contracts/operaciones.md con idempotencia/corrección; destino addons/arg_pyme_comisiones/models/commission_settlement.py
- [ ] T009 [US2] Hacer cumplir en servidor: Una liquidación confirmada conserva base y porcentaje históricos.; Un cheque recibido sin acreditar no es cobro efectivo para una regla basada en liquidez.; La liquidación no envía dinero; la OPA conserva su propia ejecución. Destino addons/arg_pyme_comisiones/models/operaciones.py

## US3

- [ ] T010 [US3] Exponer consulta/estados/origen y adaptador de hechos sin doble suma en addons/arg_pyme_comisiones/models/report_adapter.py
- [ ] T011 [US3] Crear informe/documento con moneda, estado y evidencia en addons/arg_pyme_comisiones/report/document.xml

## Polish

- [ ] T012 Documentar manual, ejemplos, límites y ficha de tutorial versionada en docs/usuario/021-comisiones.md
- [ ] T013 Resolver sintaxis, carga de vistas e instalación/arranque de composición; registrar sin atribuir QA en docs/entregas/021-comisiones.md
- [ ] T014 Fijar paquete/versiones, respaldo y promoción autorizada con hashes en composition/versions.lock.json

## Dependencies & Execution Order

Setup → Foundation → US1 → US2 → US3 → Polish. US2 depende de contrato/roles US1; US3 usa efectos ya definidos.
MVP: carga y circuito mínimo completo, sin activar canales externos. No delegar escrituras de archivos compartidos en paralelo.

## Parallel Examples

Con contratos fijados, manual y recursos de ayuda pueden prepararse en archivos separados mientras se implementa cada historia.
US1: fichas/roles separados; US2: adaptadores separados sólo tras fijar interfaz; US3: manual e informe con grano acordado.

## Implementation Strategy

Entregas pequeñas completas y composición fijada. Las tareas de implementación permanecen sin marcar hasta evidencia de código/instalación.
QA funcional/visual y aceptación no forman parte del conteo de implementación; se registran después mediante quickstart.md.
