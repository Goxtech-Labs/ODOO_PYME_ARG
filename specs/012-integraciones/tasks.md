# Tasks: Integraciones ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Tareas para programación; implementación de addons propios pendiente.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [ ] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_integraciones/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [ ] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_integraciones/security/ según data-model.md.

## Phase 2: User Story 1 Configurar proveedor

**Independent Test**: Crear configuración por compañía y entorno con secreto referenciado fuera de Git.

- [ ] T003 [US1] Implementar configurar proveedor en addons/arg_pyme_integraciones/models/integration_connector.py, aplicando "Proveedor como adaptador interno; no nuevo addon por proveedor"; "Clave única por compañía/proveedor/ambiente/clave de operación comercial, independiente de rotación del conector"; "Error incierto no equivale a rechazo". (FR-001, FR-002)
- [ ] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_integraciones/views/integration_connector_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Ejecutar con control

**Independent Test**: Encolar una operación con clave idempotente y registrar resultado sanitizado.

- [ ] T005 [US2] Implementar ejecutar con control en addons/arg_pyme_integraciones/models/integration_job.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [ ] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_integraciones/views/integration_job_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Diagnosticar y detener

**Independent Test**: Pausar proveedor y consultar intentos sin contenido sensible.

- [ ] T007 [US3] Implementar diagnosticar y detener en addons/arg_pyme_integraciones/services/health.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [ ] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_integraciones/views/integration_health_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [ ] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/012-integraciones.md y docs/tecnica/012-integraciones.md.
- [ ] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/012-integraciones.md.

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

- [ ] T011 Implementar identidad por ambiente/operación estable y guardas de desinstalación con exportación/evidencia durable según contracts/operaciones.md.
