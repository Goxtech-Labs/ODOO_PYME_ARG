# Tasks: Circuito Stock ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Código y puentes desplegados demo; QA funcional/visual y aceptación pendientes.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [x] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_stock/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [x] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_stock/security/ según data-model.md.

## Phase 2: User Story 1 Consultar cantidades claras

**Independent Test**: Consultar producto y depósito mostrando cada cantidad con unidad y fecha de corte.

- [x] T003 [US1] Implementar consultar cantidades claras en addons/arg_pyme_stock/models/stock_quant.py, aplicando "No escribir quantity directamente para simular movimientos"; "Mover existencias sólo al validar operaciones nativas"; "Aplicar diferencias mediante stock.quant.action_apply_inventory con control concurrente". (FR-001, FR-002)
- [x] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_stock/views/stock_matrix_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Registrar movimiento

**Independent Test**: Validar una entrega parcial y encontrar su remito, movimiento y pendiente vinculado.

- [x] T005 [US2] Implementar registrar movimiento en addons/arg_pyme_stock/models/stock_picking.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [x] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_stock/views/stock_picking_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Contar inventario

**Independent Test**: Guardar INV, comparar contado/teórico y aplicar AJU enlazado a movimientos nativos.

- [x] T007 [US3] Implementar contar inventario en addons/arg_pyme_stock/models/inventory_count.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [x] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_stock/views/inventory_count_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [x] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/008-stock.md y docs/tecnica/008-stock.md.
- [x] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/008-stock.md.

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

Checks de implementación/entrega técnica; no acreditan ejecución de Independent Test ni aceptación. Ver docs/entregas/008-stock.md.

## Correcciones de cierre contractual

- [x] T012 Mostrar demanda provisional y pendientes antes de validar sin congelar snapshot ni bloquear líneas nuevas incompletas. (FR-003 FR-004)
- [x] T013 Mostrar facturación vinculada como No determinado cuando no exista evidencia por movimiento y anteponer Entrega/Recepción a los ejes financieros. (FR-003 FR-004)

Controles de instalación/arranque en docs/entregas/CIERRE-DE-CONTRATOS.md; QA y aceptación posteriores.
