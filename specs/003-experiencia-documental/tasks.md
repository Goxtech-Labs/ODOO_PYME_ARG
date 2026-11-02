# Tasks: Experiencia y presentación ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Tareas para programación; desarrollado y desplegado; QA funcional/visual posterior pendiente.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [x] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_ui/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [x] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_ui/security/ según data-model.md.

## Phase 2: User Story 1 Navegar por circuitos

**Independent Test**: Abrir Presupuestos, Pedidos, Entradas y Recibos desde sus áreas y conservar filtros al volver.

- [x] T003 [US1] Implementar navegar por circuitos en addons/arg_pyme_ui/static/src/navigation/areas.js, aplicando "Guardar y Descartar mantienen significado semántico en ambos temas"; "Respetar permisos y guardas nativas de salida"; "No crear otro usuario ni cambiar XML IDs del bot". (FR-001, FR-002)
- [x] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_ui/static/src/navigation/areas.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Editar con un patrón común

**Independent Test**: Recorrer tercero, generales, detalle, totales y acciones mediante teclado.

- [x] T005 [US2] Implementar editar con un patrón común en addons/arg_pyme_ui/static/src/components/document_actions.js, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [x] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_ui/static/src/components/document_matrix.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Reconocer ARG y su ayuda

**Independent Test**: Encontrar tutoriales por módulo, soporte general y GOXTECHBOT en superficies inventariadas.

- [x] T007 [US3] Implementar reconocer arg y su ayuda en addons/arg_pyme_ui/hooks.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [x] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_ui/views/help_support.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [x] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/003-experiencia-documental.md y docs/tecnica/003-experiencia-documental.md.
- [x] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/003-experiencia-documental.md.

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

## Correcciones de cierre contractual

- [x] T011 Completar SVG originales con texto en áreas/acciones y Acerca de ARG autenticado, preservando atribuciones. (FR-001 FR-003 FR-005)

Controles de instalación/arranque en docs/entregas/CIERRE-DE-CONTRATOS.md; QA y aceptación posteriores.

## Canales públicos elegidos por el titular

- [x] T012 Mostrar web/canal configurados en Ayuda, Soporte y Acerca de sin confundir el canal con un tutorial compatible. (FR-005 FR-006)
