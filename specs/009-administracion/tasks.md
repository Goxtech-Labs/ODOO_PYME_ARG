# Tasks: Circuito Administración ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Desarrollado e instalado técnicamente demo y entorno aislado; QA funcional/visual y aceptación pendientes.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [x] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_administracion/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [x] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_administracion/security/ según data-model.md.

## Phase 2: User Story 1 Consultar deuda

**Independent Test**: Consultar facturas publicadas y saldos residuales separados por moneda y compañía.

- [x] T003 [US1] Implementar consultar deuda en addons/arg_pyme_administracion/models/current_account.py, aplicando "No mantener saldo paralelo"; "Configurar outstanding_account_id; no asumir move_id siempre existente"; "Saldo desde apuntes/residuales, nunca invoice_ids por sí solo". (FR-001, FR-002)
- [x] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_administracion/views/current_account_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Cobrar o pagar

**Independent Test**: Crear REC u OPA con un medio y aplicar un pago parcial conservando saldo pendiente.

- [x] T005 [US2] Implementar cobrar o pagar en addons/arg_pyme_administracion/models/treasury_document.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [x] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_administracion/views/treasury_document_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Revisar caja y revertir

**Independent Test**: Consultar caja por diario y fecha y revertir una aplicación conservando historial.

- [x] T007 [US3] Implementar revisar caja y revertir en addons/arg_pyme_administracion/models/cash_report.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [x] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_administracion/views/cash_report_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [x] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/009-administracion.md y docs/tecnica/009-administracion.md.
- [x] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/009-administracion.md.

## Dependencies & Execution Order

Completar Setup antes de las historias; implementar US1 → US2 → US3 para conservar contratos comunes.
Respetar dependencias del catálogo y no iniciar todos los módulos simultáneamente.
Mantener código, instalación, QA, aceptación y publicación como hitos independientes.

## Parallel Examples

Después de fijar contratos, preparar manual y ejemplos en archivos diferentes.
Mantener secuencial la escritura de modelos/vistas compartidos; no implica delegar implementación paralela.

## Implementation Strategy

Entregar primero US1 con el caso mínimo; agregar US2 y US3 conservando fuente única.
Usar ejemplos, resolver controles técnicos y realizar QA funcional/visual en la fase posterior acordada.

- [x] T011 Implementar indicadores independientes pendiente/parcial/completo del contrato docs/tecnica/ESTADOS-Y-PENDIENTES.md en modelos y vistas del circuito; no reemplazar estados técnicos nativos ni confundir cierre con cumplimiento.

- [x] T012 Implementar ruta de anticipos independiente del wizard y eventos inmutables de aplicación/desaplicación en models/treasury_document.py y models/treasury_audit_event.py, sin otro libro de saldos.

T001–012 completadas como código/entrega técnica20.0.1.1.1. Los Independent Test y quickstart no se ejecutaron: QA funcional/visual y aceptación siguen pendientes. Evidencia en docs/entregas/009-administracion.md.
