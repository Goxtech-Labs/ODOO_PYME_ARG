# Tasks: Base ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Tareas para programación; desarrollado y desplegado; QA funcional/visual posterior pendiente.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [x] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_base/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [x] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_base/security/ según data-model.md.

## Phase 2: User Story 1 Identificar documentos

**Independent Test**: Asignar PRE-000001 y PED-000001 desde secuencias independientes y conservar ambos códigos.

- [x] T003 [US1] Implementar identificar documentos en addons/arg_pyme_base/models/document_identity.py, aplicando "Prefijo de 2 a 4 letras ASCII; secuencia independiente por compañía y tipo"; "Unicidad por compañía, tipo y número; código asignado inmutable"; "No mostrar un enlace ficticio como tutorial disponible"; "Sólo administradores modifican destinos; no guardar credenciales de proveedores aquí". (FR-001, FR-002)
- [x] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_base/views/document_type_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Configurar roles y preferencias

**Independent Test**: Asignar a una persona Ventas, Compras y Administración según permisos expresos.

- [x] T005 [US2] Implementar configurar roles y preferencias en addons/arg_pyme_base/models/res_users.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [x] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_base/security/roles.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Ayuda y soporte central

**Independent Test**: Actualizar un enlace YouTube central sin reinstalar el módulo y encontrarlo desde su ayuda.

- [x] T007 [US3] Implementar ayuda y soporte central en addons/arg_pyme_base/models/help_resource.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [x] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_base/views/help_support_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [x] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/002-base-arg.md y docs/tecnica/002-base-arg.md.
- [x] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/002-base-arg.md.

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

- [x] T011 Corregir registro AJU al modelo de ajuste e incorporar migración que preserve identidades existentes en addons/arg_pyme_base/migrations/. (FR-001 FR-002)

Controles de instalación/arranque en docs/entregas/CIERRE-DE-CONTRATOS.md; QA y aceptación posteriores.
