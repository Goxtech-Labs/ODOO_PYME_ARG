# Tasks: Portada y documentación pública ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Entrega documental implementada; controles técnicos registrados en docs/entregas/011-web-comunidad.md. Publicación remota y aceptación pendientes.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [x] T001 Preparar estructura documental de docs/site/ y mapa de enlaces según plan.md.
- [x] T002 Definir autores, privacidad, licencia adoptada y estados de publicación en docs/site/README.md; no crear ACL de addon para esta entrega documental.

## Phase 2: User Story 1 Conocer el proyecto

**Independent Test**: Abrir README y encontrar propósito, cinco circuitos, autoría y enlaces de inicio.

- [x] T003 [US1] Implementar conocer el proyecto en docs/site/README.md, aplicando "No publicar fotos/capturas ajenas sin permiso"; "No URL ficticia activada"; "Publicación y envío externos requieren autorización correspondiente". (FR-001, FR-002)
- [x] T004 [US1] Documentar el recorrido, ejemplos y reglas mediante docs/site/assets/banner.svg, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Aprender por módulo

**Independent Test**: Encontrar manual y ficha de video por módulo, versión y estado.

- [x] T005 [US2] Implementar aprender por módulo en docs/site/tutoriales/catalogo.yml, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [x] T006 [US2] Documentar el recorrido, ejemplos y reglas mediante docs/site/tutoriales/README.md, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Participar

**Independent Test**: Encontrar CONTRIBUTING, roadmap y plantilla de propuesta con referencia a spec.

- [x] T007 [US3] Implementar participar en docs/site/CONTRIBUTING.md, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [x] T008 [US3] Documentar el recorrido, ejemplos y reglas mediante docs/site/comunidad/README.md, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [x] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/011-web-comunidad.md y docs/tecnica/011-web-comunidad.md.
- [x] T010 Registrar controles de enlaces, formato y coherencia y reservar ejecución de quickstart para QA posterior en docs/entregas/011-web-comunidad.md.

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
