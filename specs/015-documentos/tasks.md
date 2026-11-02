# Tasks: Motor documental e impresión ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Desarrollado e instalado técnicamente; QA funcional/visual y aceptación pendientes.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [X] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_documentos/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [X] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_documentos/security/ según data-model.md.

## Phase 2: User Story 1 Identificar documento

**Independent Test**: Abrir PRE-000001 y distinguir su número interno de referencias fiscales o externas.

- [X] T003 [US1] Implementar identificar documento en addons/arg_pyme_documentos/models/document_mixin.py, aplicando "Número único por compañía/tipo"; "No usar sólo origin textual"; "Documento fiscal sólo con estado/autorización válidos". (FR-001, FR-002)
- [X] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_documentos/views/document_header.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Vincular derivados

**Independent Test**: Desde PRE confirmado abrir PED distinto con trazabilidad de cada línea.

- [X] T005 [US2] Implementar vincular derivados en addons/arg_pyme_documentos/models/document_links.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [X] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_documentos/views/document_links.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Imprimir

**Independent Test**: Generar PDF con identidad ARG, tercero, detalle, totales y estado correcto.

- [X] T007 [US3] Implementar imprimir en addons/arg_pyme_documentos/report/document_report.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [X] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_documentos/report/document_templates.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [X] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/015-documentos.md y docs/tecnica/015-documentos.md.
- [X] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/015-documentos.md.

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

- [X] T011 Implementar indicadores independientes pendiente/parcial/completo del contrato docs/tecnica/ESTADOS-Y-PENDIENTES.md en modelos y vistas del circuito; no reemplazar estados técnicos nativos ni confundir cierre con cumplimiento. (FR-003; mecanismo común, adaptadores por circuito y QA posterior separados.)

## Correcciones de cierre contractual

- [x] T012 Presentar razón de ejes indeterminados en pantalla/PDF y conservar icono/texto de estados; helper de alcance exclusivo de facturas sin sudo ni reparto inventado. (FR-003 FR-005 FR-006)

Controles de instalación/arranque en docs/entregas/CIERRE-DE-CONTRATOS.md; QA y aceptación posteriores.
