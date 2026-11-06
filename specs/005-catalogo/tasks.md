# Tasks: Catálogo y precios ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.
**Estado**: Catálogo previo instalado; incremento de variantes instalado técnicamente en aislado; promoción y QA pendientes.
**Tests**: Escenarios preparados para QA posterior; controles técnicos durante instalación.

## Phase 1: Setup

- [X] T001 Preparar estructura y dependencias declaradas de addons/arg_pyme_catalogo/ según plan.md; no modificar core ni introducir dependencias externas obligatorias.
- [X] T002 Definir grupos/permisos y aislamiento por compañía en addons/arg_pyme_catalogo/security/ según data-model.md.

## Phase 2: User Story 1 Crear producto o servicio

**Independent Test**: Crear un producto de ejemplo con nombre, tipo, unidad y precio sin completar atributos de un rubro ajeno.

- [X] T003 [US1] Implementar crear producto o servicio en addons/arg_pyme_catalogo/models/product_template.py, aplicando "SKU textual con ceros iniciales conservados"; "No sumar ni mostrar precios de monedas diferentes sin identificación"; "No imponer dimensiones de un rubro al núcleo". (FR-001, FR-002)
- [X] T004 [US1] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_catalogo/views/product_template_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-001, FR-002)

## Phase 3: User Story 2 Actualizar precios

**Independent Test**: Filtrar productos y editar precios en columnas alineadas, revisando antes de guardar.

- [X] T005 [US2] Implementar actualizar precios en addons/arg_pyme_catalogo/models/pricelist_matrix.py, aplicando los invariantes de contracts/operaciones.md. (FR-003, FR-004)
- [X] T006 [US2] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_catalogo/views/pricelist_matrix_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-003, FR-004)

## Phase 4: User Story 3 Extender sin imponer rubro

**Independent Test**: Agregar un atributo opcional y conservar el mismo catálogo y sus referencias.

- [X] T007 [US3] Implementar extender sin imponer rubro en addons/arg_pyme_catalogo/models/product_attributes.py, aplicando los invariantes de contracts/operaciones.md. (FR-005, FR-006)
- [X] T008 [US3] Exponer el recorrido y sus mensajes/acciones mediante addons/arg_pyme_catalogo/views/product_attribute_views.xml, conservando datos mínimos, orden y permisos efectivos. (FR-005, FR-006)

## Phase 5: Entrega transversal

- [X] T009 Documentar uso, ejemplos, límites y tutoriales versionados en docs/usuario/005-catalogo.md y docs/tecnica/005-catalogo.md.
- [X] T010 Registrar controles técnicos de instalación y reservar ejecución de quickstart para QA posterior en docs/entregas/005-catalogo.md.

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

## Incremento de variantes FR-007/008 · 2026-11-06

- [x] T011 Implementar consulta paginada, ejes/fijos, exclusiones y acciones autorizadas en addons/arg_pyme_catalogo/models/variant_matrix.py, sin generar variantes ni usar lookup con sudo.
- [x] T012 Exponer matriz OWL, selector de valores paginado, selección persistente y acceso desde ficha en addons/arg_pyme_catalogo/static/src/variant_matrix.* y views/variant_matrix_views.xml.
- [x] T013 Agregar adaptador opcional de cantidades nativas en addons/arg_pyme_stock/models/variant_matrix.py; ausencia de permiso es no determinado, nunca cero inventado.
- [x] T014 Enlazar precios existentes por plantilla y etiquetas nativas con revalidación de selección, sin duplicar maestros ni imprimir automáticamente.
- [x] T015 Documentar alcance, límites y escenarios pendientes; completar controles estáticos y revisión independiente del delta.
- [ ] T016 Fijar paquete e instalar en aislado y demo con respaldo recuperable; registrar versión/lectura posterior y QA posterior pendiente.

Orden:T011→T012/T013→T014→T015→T016. Estas tareas amplían las históricas, no reabren ni acreditan de nuevo el catálogo previo. Parent016T008 sigue abierta hasta F19/condiciones; F17/F22 conservan etiquetas/importación ampliadas pendientes.

2026-11-06:T011–T015 tienen fuente/registro/instalación aislada y documentación revisados, sin QA funcional/visual. T016 conserva promoción a demo pendiente. [Entrega](../../docs/entregas/005-variantes.md).
