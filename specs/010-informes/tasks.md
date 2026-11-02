# Tasks: Circuito Informes ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Desarrollado e instalado técnicamente demo y entorno aislado; QA funcional/visual y aceptación pendientes.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [x] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_informes/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [x] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_informes/security/ según data-model.md.

## Phase 2: User Story 1 Leer hechos separados

**Independent Test**: Consultar facturación neta por fecha, tercero y producto con grano línea de factura.

- [x] T003 [US1] Implementar leer hechos separados en addons/arg_pyme_informes/report/facts.py, aplicando "No es caja ni presupuesto"; "No repetir pago por cada factura relacionada"; "Reglas de acceso también en consultas SQL y exports". (FR-001, FR-002)
- [x] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_informes/views/report_menu.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Filtrar y explicar

**Independent Test**: Filtrar compañía, período y moneda y abrir las líneas que componen un total.

- [x] T005 [US2] Implementar filtrar y explicar en addons/arg_pyme_informes/report/dimensions.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [x] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_informes/views/report_filters.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Exportar e imprimir

**Independent Test**: Exportar CSV UTF-8 y PDF con filtros, moneda, fecha y totales consistentes.

- [x] T007 [US3] Implementar exportar e imprimir en addons/arg_pyme_informes/report/export.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [x] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_informes/report/report_templates.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [x] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/010-informes.md y docs/tecnica/010-informes.md.
- [x] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/010-informes.md.

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

Los checks acreditan código/entrega técnica; los Independent Test y quickstart siguen reservados para QA posterior. Evidencia en docs/entregas/010-informes.md.

## Correcciones de cierre contractual

- [x] T012 Aplicar precisión monetaria y decimal de cantidades después de agregar, compartida por HTML/CSV/PDF, sin limitar a doce cifras significativas ni cuantizar cantidades al paso UOM. (FR-005 FR-006)

Controles de instalación/arranque en docs/entregas/CIERRE-DE-CONTRATOS.md; QA y aceptación posteriores.
