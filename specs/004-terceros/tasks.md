# Tasks: Terceros ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Desarrollado e instalado; QA funcional/visual y aceptación pendientes.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [X] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_terceros/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [X] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_terceros/security/ según data-model.md.

## Phase 2: User Story 1 Alta mínima

**Independent Test**: Guardar un contacto de ejemplo con nombre y rol y continuar el documento.

- [X] T003 [US1] Implementar alta mínima en addons/arg_pyme_terceros/models/res_partner.py, aplicando "Una identidad por tercero; roles cliente/proveedor combinables"; "No depender de customer_rank/supplier_rank cuando account no está instalado"; "No inventar identificadores fiscales ni sobrescribir condiciones históricas". (FR-001, FR-002)
- [X] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_terceros/views/res_partner_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Combinar roles

**Independent Test**: Agregar rol proveedor a un cliente y conservar identidad, contactos e historia.

- [X] T005 [US2] Implementar combinar roles en addons/arg_pyme_terceros/models/res_partner.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [X] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_terceros/views/res_partner_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Aplicar condiciones

**Independent Test**: Aplicar moneda, tarifa, plazo y dirección conocidas al crear un documento.

- [X] T007 [US3] Implementar aplicar condiciones en addons/arg_pyme_terceros/models/res_partner.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [X] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_terceros/views/res_partner_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [X] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/004-terceros.md y docs/tecnica/004-terceros.md.
- [X] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/004-terceros.md.

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
