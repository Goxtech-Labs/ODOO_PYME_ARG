# Tasks: Extensiones por rubro y personalizaciones ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Tareas para programación; implementación de addons propios pendiente.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [ ] T001 Preparar estructura documental de docs/rubros/ y mapa de enlaces según plan.md.
- [ ] T002 Definir autores, privacidad, licencia propuesta y estados de publicación en docs/rubros/README.md; no crear ACL de addon para esta entrega documental.

## Phase 2: User Story 1 Definir alcance

**Independent Test**: Completar plantilla con problema, documentos, campos mínimos y exclusiones.

- [ ] T003 [US1] Implementar definir alcance en docs/rubros/plantillas/spec-rubro.md, aplicando "No seleccionar rubro inicial sin decisión de producto"; "No bifurcar core"; "Incompatibilidades explícitas". (FR-001, FR-002)
- [ ] T004 [US1] Documentar el recorrido, ejemplos y reglas mediante docs/rubros/plantillas/alcance.md, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Extender sin duplicar

**Independent Test**: Proponer addon arg_pyme_rubro_nombre con extensiones y relaciones al núcleo.

- [ ] T005 [US2] Implementar extender sin duplicar en docs/rubros/plantillas/composicion.md, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [ ] T006 [US2] Documentar el recorrido, ejemplos y reglas mediante docs/rubros/plantillas/compatibilidad.md, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Documentar entrega

**Independent Test**: Encontrar manual, datos de ejemplo, tutorial y notas de compatibilidad por rubro.

- [ ] T007 [US3] Implementar documentar entrega en docs/rubros/plantillas/entrega.md, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [ ] T008 [US3] Documentar el recorrido, ejemplos y reglas mediante docs/rubros/plantillas/tutorial.md, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [ ] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/014-rubros.md y docs/tecnica/014-rubros.md.
- [ ] T010 Registrar controles de enlaces, formato y coherencia y reservar ejecución de quickstart para QA posterior en docs/entregas/014-rubros.md.

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
