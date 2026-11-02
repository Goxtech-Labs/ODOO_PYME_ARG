# Tasks: Circuito Compras ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Comercial, puente físico y ejes de dinero instalados demo; QA funcional/visual y aceptación pendientes.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [x] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_compras/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [x] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_compras/security/ según data-model.md.

## Phase 2: User Story 1 Pedir al proveedor

**Independent Test**: Guardar PPC-000001 y confirmar condiciones conocidas sin exigir circuitos departamentales adicionales.

- [x] T003 [US1] Implementar pedir al proveedor en addons/arg_pyme_compras/models/purchase_order.py, aplicando "Referencia de proveedor independiente del código interno"; "Existencias sólo desde movimientos validados"; "Conservar número original del proveedor sin reemplazarlo por FRC". (FR-001, FR-002)
- [x] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_compras/views/purchase_order_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Recibir y registrar factura

**Independent Test**: Recibir parte del pedido mediante ENT y registrar FRC vinculada sin duplicar entrada.

- [x] T005 [US2] Implementar recibir y registrar factura en addons/arg_pyme_compras/models/purchase_receipt.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [x] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_compras/views/purchase_receipt_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Gestionar devolución

**Independent Test**: Generar devolución desde entrada y consultar su efecto neto y documentos relacionados.

- [x] T007 [US3] Implementar gestionar devolución en addons/arg_pyme_compras/models/purchase_return.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [x] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_compras/views/purchase_return_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [x] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/007-compras.md y docs/tecnica/007-compras.md.
- [x] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/007-compras.md.

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

- [x] T012 Implementar addons/arg_pyme_compras_stock/ con manifest, ACL y vistas de movimientos; mover allí toda referencia a stock/puente nativo y ocultar capacidades físicas cuando no esté instalado.

## Entrega de dependencias008/009

Puente físico y Administración instalados. Tareas completas como código/entrega técnica; incluye cantidades físicas y dinero sobre lo facturado, sin confundir deuda cancelada con caja. Escenarios de aceptación sin ejecutar. Evidencia de Administración en docs/entregas/009-administracion.md.

## Correcciones de cierre contractual

- [x] T013 Evitar atribuir deuda/dinero de facturas compartidas a un PPC; conservar consulta de comprobantes y razón de alcance indeterminado. (FR-003 FR-004)

Controles de instalación/arranque en docs/entregas/CIERRE-DE-CONTRATOS.md; QA y aceptación posteriores.
