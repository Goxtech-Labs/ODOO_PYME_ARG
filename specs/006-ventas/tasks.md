# Tasks: Circuito Ventas ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Comercial, puente físico y ejes de dinero instalados demo; QA funcional/visual y aceptación pendientes.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [x] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_ventas/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [x] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_ventas/security/ según data-model.md.

## Phase 2: User Story 1 Preparar y confirmar presupuesto

**Independent Test**: Guardar PRE-000001, confirmarlo y consultar sus líneas/condiciones sin movimientos de stock ni dinero.

- [x] T003 [US1] Implementar preparar y confirmar presupuesto en addons/arg_pyme_ventas/models/quotation.py, aplicando "Documento propio distinto del pedido; confirmar no mueve stock ni dinero"; "Varios pedidos parciales por presupuesto; generación idempotente por operación y control de cantidades por raíz/revisión"; "No duplicar movimientos ni usar origin textual como único vínculo". (FR-001, FR-002)
- [x] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_ventas/views/quotation_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Generar pedido cliente

**Independent Test**: Generar PED-000001 separado, enlazar PRE-000001 y conservar ambos documentos consultables.

- [x] T005 [US2] Implementar generar pedido cliente en addons/arg_pyme_ventas/models/sale_order.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [x] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_ventas/views/sale_order_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Entregar y facturar

**Independent Test**: Consultar cantidades pedidas, entregadas y facturadas con sus documentos de origen y acceder al cobro de Administración.

- [x] T007 [US3] Implementar entregar y facturar en addons/arg_pyme_ventas/models/account_move.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [x] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_ventas/views/sale_document_links.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [x] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/006-ventas.md y docs/tecnica/006-ventas.md.
- [x] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/006-ventas.md.

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

- [x] T012 Implementar addons/arg_pyme_ventas_stock/ con manifest, ACL y vistas de movimientos; mover allí toda referencia a stock/puente nativo y ocultar capacidades físicas cuando no esté instalado.

- [x] T013 Implementar eventos de aceptación/liberación con claves idempotentes y cantidades objetivo acumuladas por raíz; cubrir el ejemplo objetivo10/PED4/saldo6 de contrato PRE/PED v1.1 sin duplicar compromisos.

## Entrega de dependencias008/009

Puente físico y Administración instalados. Tareas completas como código/entrega técnica; incluye cantidades físicas y dinero sobre lo facturado, sin confundir deuda cancelada con caja. Escenarios de aceptación sin ejecutar. Evidencia de Administración en docs/entregas/009-administracion.md.

## Correcciones de cierre contractual

- [x] T014 Evitar atribuir importes completos de facturas compartidas a un PED; mostrar No determinado y razón sin prorrateo implícito. (FR-005 FR-006)

Controles de instalación/arranque en docs/entregas/CIERRE-DE-CONTRATOS.md; QA y aceptación posteriores.
