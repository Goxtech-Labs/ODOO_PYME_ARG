# Tasks: Contrato futuro ARCA dentro de Integraciones ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Tareas para programación; implementación de addons propios pendiente.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [ ] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_integraciones/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [ ] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_integraciones/security/ según data-model.md.

## Phase 2: User Story 1 Configurar emisor

**Independent Test**: Validar configuración de homologación sin usar CUIT o certificados reales del usuario.

- [ ] T003 [US1] Implementar configurar emisor en addons/arg_pyme_integraciones/services/providers/arca/config.py, aplicando "Configuración fiscal real fuera de fixtures"; "Producción desactivada"; "No reemplazar número fiscal por FAC interno". (FR-001, FR-002)
- [ ] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_integraciones/views/arca_config_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Autorizar comprobante

**Independent Test**: Preparar solicitud consistente y registrar autorización, rechazo o resultado incierto.

- [ ] T005 [US2] Implementar autorizar comprobante en addons/arg_pyme_integraciones/services/providers/arca/authorization.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [ ] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_integraciones/views/arca_job_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Mostrar evidencia

**Independent Test**: Distinguir borrador, pendiente, autorizado y rechazado en pantalla e impresión.

- [ ] T007 [US3] Implementar mostrar evidencia en addons/arg_pyme_integraciones/services/providers/arca/evidence.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [ ] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_integraciones/report/arca_templates.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [ ] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/013-arca.md y docs/tecnica/013-arca.md.
- [ ] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/013-arca.md.

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

- [ ] T011 Implementar consulta del comprobante exacto y comparación de solicitud, preservación de uncertain y evidencia fiscal durable; no usar último autorizado como prueba de identidad.
