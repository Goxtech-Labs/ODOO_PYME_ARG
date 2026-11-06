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

## F14 · trazabilidad y alta mínima (US4/US5)

- [x] T014 Fijar contrato y referencias nativas en specs/008-stock/contracts/trazabilidad-series-lotes.md y research.md, con revisión independiente.
- [x] T015 [US4] Implementar consulta/ACL/compañía/paginación en addons/arg_pyme_stock/models/traceability.py; no tabla de movimientos nueva. (FR-007–010)
- [x] T016 [US4] Crear acción OWL, selectores30, rango opcional y navegación preservada en addons/arg_pyme_stock/static/src/traceability.js y traceability.xml. (FR-007–010)
- [x] T017 [US5] Crear asistente de alta única en addons/arg_pyme_stock/models/lot_create.py y views/traceability_views.xml: número1–256/ref0–256, resultado protegido y lock de identidad también en altas nativas, sin movimiento físico. (FR-011)
- [x] T018 Documentar uso/límites/ejemplos y tutorial planeado en docs/usuario/008-stock.md, docs/tecnica/008-stock.md y docs/comunidad/youtube/catalogo.json.
- [x] T019 Revisar delta exacto/secretos/paquete y registrar instalación técnica aislada en docs/entregas/008-trazabilidad.md.
- [x] T020 Promover mismo paquete con respaldo/restauración, lectura posterior y publicación en main; fijar composición y docs/entregas/008-trazabilidad.md.

T014→T015→T016/T017→T018→T019→T020. No ejecutar los escenarios funcionales en esta fase.
Parent016T009 conserva F15/reposición pendiente después de esta entrega; mantener el objetivo completo.

T015–T018 acreditan fuente/documentación y controles estáticos. T019 y T020 completadas como
entrega técnica: paquete299, registro/vistas/arranque, rol nativo propagado, respaldo recuperado,
mismo paquete en demo y publicación de fuentes/composición/documentación. QA y aceptación pendientes.

## F15 · Phase 1: Fundamentos de reposición

- [x] T021 Fijar y revisar independientemente specs/008-stock/contracts/reposicion.md, research.md y plan.md con fuentes nativas, efectos encadenados y permisos antes de implementación. (FR-012–017)
- [ ] T022 [US6] Extender regla nativa en addons/arg_pyme_stock/models/replenishment.py: producto almacenable, compañía/depósito/ubicación compatibles y "0 ≤ mínimo ≤ máximo", valores finitos; crear manual sólo en entrada ARG y no cambiar modalidades existentes. (FR-012)
- [ ] T023 [US6] Crear servicio arg.pyme.replenishment en addons/arg_pyme_stock/models/replenishment.py con consulta paginada30, contexto/ACL efectivos y dimensiones autorizadas; no ejecutar _get_orderpoint_action ni abastecimiento al consultar. (FR-012/013/017)
- [ ] T024 [US6] Crear ficha/acción de configuración en addons/arg_pyme_stock/views/replenishment_views.xml con datos deducidos, campos delimitados y avanzado opcional; guardar no genera PO/MO. (FR-012)

## F15 · Phase 2: Propuesta y confirmación (US7)

- [ ] T025 [US7] Implementar propuesta/huella/grafo revisado en addons/arg_pyme_stock/models/replenishment.py desde cálculo nativo, pipeline, rutas/proveedor/BOM, MO previas y ramas/componentes; "Hasta30 reglas por página/confirmación" y "cantidades elegidas finitas y positivas". (FR-013/014/015/017)
- [ ] T026 [US7] Crear evidencia en addons/arg_pyme_stock/models/replenishment_operation.py y security/ir.access.csv: "operation_key UUID canónico de36 caracteres", "Unicidad técnica (company_id, operation_key)", sólo creación interna e inmutabilidad; sin ACL read/export raw para gestión, servicio valida todas las dimensiones sin sudo como solicitante ACTUAL antes de lectura/replay o deniega representación completa; referencias/deltas/actor/compañía sin otro saldo. (FR-016)
- [ ] T027 [US7] Implementar contexto privado, collector y guardas core en addons/arg_pyme_stock/models/replenishment.py y stock_quant.py: autorizar actor antes de efectos native sudo, bloquear en orden y cubrir mutadores nativos de físico/previsión/pipeline/maestros incluso sin collector (permisos nativos, sin rol ARG global); mantener llamadas hijas dentro de alcance y errores atómicos; no flags RPC ni commits/cursor nuevo. (FR-015/016/017)
- [ ] T028 [US7] Ampliar compra en addons/arg_pyme_compras_stock/models/replenishment.py y __init__.py: hooks PO/líneas create/write, demanda/resultado nuevo o ampliado, UOM/condiciones anteriores/resultantes y guardas ARG existentes, sin referencia comercial artificial. (FR-015/016/017)
- [ ] T029 [US7] Crear puente opcional addons/arg_pyme_stock_mrp/__manifest__.py y models/replenishment.py, mrp_production.py: BOM/kit/lote, nuevas/ampliadas/previas MO, action_confirm/change_prod_qty, componentes/trabajos y abastecimiento hijo autorizados/capturados; serializar mutadores MRP/BOM relevantes también sin collector con permisos nativos y conservar super. (FR-015/016/017)
- [ ] T030 [US7] Implementar confirmar/reintentar en addons/arg_pyme_stock/models/replenishment.py: búsqueda de recibo antes de recomparar propuesta, cantidad manual explícita sin inverse, confirmación nativa con errores, consumo de override y postcondiciones completas en misma transacción. (FR-014/015/016)
- [ ] T031 [US7] Implementar interfaz en addons/arg_pyme_stock/static/src/replenishment.js y replenishment.xml con selección/cantidades preservadas, revisión de efectos/errores y apertura autorizada de resultados; no mostrar claves técnicas como documento. (FR-013–017)

## F15 · Phase 3: Entrega transversal

- [ ] T032 Documentar reglas/propuesta/confirmación/efectos/ejemplos optativos y tutorial planeado en docs/usuario/008-stock.md, docs/tecnica/008-stock.md y docs/comunidad/youtube/catalogo.json.
- [ ] T033 Revisar diff/secretos/paquete e instalar composición aislada compra+MRP/puentes; registrar registry/vistas/arranque/fuentes en docs/entregas/008-reposicion.md sin ejecutar QA funcional.
- [ ] T034 Promover mismo paquete con respaldo fresco restaurado/copia sin red y lectura posterior de instalación/servicios en docs/entregas/008-reposicion.md, sin reemplazar datos ni activar canales reales.
- [ ] T035 Publicar fuentes/composición/manuales en main mediante revisión final y actualizar docs/entregas/RELEASE.md; cerrar parent016T009 sólo por F14/F15 técnicos completos, manteniendo QA/aceptación separadas.

T021→T022→T023/T024→T025→T026/T027→T028/T029→T030→T031→T032→T033→T034→T035.
US6 se puede entregar incrementalmente pero no completa F15. Compra y MRP comparten contrato y
orquestación antes de cerrar US7. Manual y catálogo tutorial pueden prepararse en archivos separados
tras fijar contratos; no implica delegar mutaciones paralelas. No crear tareas de ejecución de QA
antes del despliegue por la preferencia vigente. Escenarios y criterios independientes en spec/quickstart.
