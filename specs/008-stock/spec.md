# Feature Specification: Circuito Stock ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Desarrollado y desplegado; QA funcional/visual y aceptación pendientes.

**Input**: Consultar existencias y operar entradas, salidas, transferencias, inventarios y ajustes con trazabilidad nativa.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consultar cantidades claras (Priority: P1)

Como responsable necesito distinguir stock físico, reservado, disponible y previsto.

**Why this priority**: Entregar consultar cantidades claras con el orden común y decisiones mínimas.

**Independent Test**: Consultar producto y depósito mostrando cada cantidad con unidad y fecha de corte.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** consultar producto y depósito mostrando cada cantidad con unidad y fecha de corte.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** no presentar cantidad prevista como existencia física ni sumar el mismo traslado dos veces.

### User Story 2 - Registrar movimiento (Priority: P2)

Como operador necesito una entrada o salida con origen y cantidades reales.

**Why this priority**: Entregar registrar movimiento con el orden común y decisiones mínimas.

**Independent Test**: Validar una entrega parcial y encontrar su remito, movimiento y pendiente vinculado.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** validar una entrega parcial y encontrar su remito, movimiento y pendiente vinculado.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** pedir serie/lote sólo al producto trazable y ofrecer dejar pendiente o cerrar faltante explícitamente.

### User Story 3 - Contar inventario (Priority: P2)

Como operador necesito registrar cantidad contada y aplicar diferencias de forma trazable.

**Why this priority**: Entregar contar inventario con el orden común y decisiones mínimas.

**Independent Test**: Guardar INV, comparar contado/teórico y aplicar AJU enlazado a movimientos nativos.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** guardar INV, comparar contado/teórico y aplicar AJU enlazado a movimientos nativos.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** detectar cambios concurrentes antes de aplicar y evitar sobrescribir cantidad real sin evidencia.

### User Story 4 - Seguir una serie o un lote (Priority: P1)

Como operador necesito buscar un número de serie/lote y ver sus entradas, traslados, salidas,
ajustes y devoluciones con fecha, cantidad, unidad y documento, sin volver a cargar esa historia.

**Independent Test**: Elegir una serie/lote y recorrer su historia paginada, abrir el origen autorizado
y distinguir los movimientos terminados de la existencia visible actual.

**Acceptance Scenarios**:

1. **Given** un lote con entradas, traslados, salidas y devoluciones, **When** se consulta su historia,
   **Then** cada hecho conserva origen/destino, fecha, documento y cantidad nativos, sin duplicar stock.
2. **Given** un rango histórico o acceso parcial, **When** se consulta, **Then** el filtro sólo limita
   movimientos y las cantidades actuales se identifican aparte; un dato restringido no se inventa.

### User Story 5 - Dar de alta una serie o un lote (Priority: P2)

Como operador necesito elegir un producto rastreable e ingresar su número, conservando ceros
iniciales y referencias del fabricante, para usarlo después en la recepción o el inventario.

**Independent Test**: Crear un lote con producto y número, volver a su consulta y reconocer que
las existencias se registran mediante operaciones de stock; repetir la misma solicitud no duplica el alta.

**Acceptance Scenarios**:

1. **Given** producto rastreable y número válido, **When** se confirma el alta explícita, **Then**
   se crea el maestro nativo en la compañía actual y se abre la consulta sin generar movimientos.
2. **Given** un producto sin seguimiento, un número ocupado o una solicitud repetida, **When** se
   confirma, **Then** se requiere configuración/corrección o se devuelve el alta ya realizada,
   conservando el producto, su configuración y las cantidades existentes.

### User Story 6 - Configurar reposición simple (Priority: P1)

Como responsable necesito indicar producto, depósito y mínimos/máximos para revisar faltantes,
sin generar un pedido al guardar la configuración. Las reglas existentes conservan su modalidad.

**Independent Test**: Crear una regla manual con producto y límites, completar depósito/ubicación
desde la configuración y comprobar que guardar sólo conserva esa regla.

**Acceptance Scenarios**:

1. **Given** un producto con existencias y un depósito configurado, **When** guardo mínimo y máximo,
   **Then** veo su unidad y ubicación, sin un pedido o una orden de fabricación por ese guardado.
2. **Given** una regla automática existente, **When** abro la consulta ARG, **Then** reconozco esa
   modalidad y no se convierte silenciosamente en manual, ni se vuelve a ejecutar al consultar.

### User Story 7 - Revisar y confirmar reposición (Priority: P1)

Como responsable necesito revisar físico, previsto, abastecimiento pendiente, cantidad sugerida
y cantidad elegida antes de generar o ampliar compras u órdenes de fabricación.

**Independent Test**: Revisar una propuesta de compra y otra de fabricación, confirmar cantidades
explícitas y abrir sus documentos originales; reintentar la misma confirmación conserva el resultado.

**Acceptance Scenarios**:

1. **Given** faltantes con ruta/proveedor o lista de materiales válidos, **When** reviso la propuesta,
   **Then** distingo cantidades, unidad, fecha/horizonte y efecto esperado, sin efectos por consultar.
2. **Given** cantidades elegidas y permisos suficientes, **When** confirmo, **Then** se generan o
   amplían los documentos nativos por las cantidades aceptadas y puedo reconocer sus referencias.
3. **Given** una propuesta modificada, permisos insuficientes o configuración incompleta, **When**
   confirmo, **Then** recibo una explicación para corregir/revisar y ninguna reposición parcial oculta.
4. **Given** una confirmación ya terminada, **When** la reintento, **Then** veo los mismos resultados;
   una nueva reposición requiere otra revisión que contemple lo que ya está en curso.

### Edge Cases

- Una transferencia interna es neutra para el total de empresa y cambia saldos por ubicación.
- Distinguir demanda product_uom_qty, cantidad operada quantity y cantidades finalizadas.
- Usar backorders y retornos nativos, conservando enlaces.
- No escribir qty_delivered o qty_received comerciales cuando derivan de movimientos.
- No generar stock por editar tarifas ni contabilizar otra entrada al registrar factura.
- Una reposición puede ampliar un pedido o una orden existente, y una fabricación puede dividirse
  en lotes de producción; no exigir que cada confirmación cree exactamente un documento nuevo.
- Un conjunto de productos puede tener abastecimiento encadenado o componentes; explicar sus
  efectos y permisos antes de confirmar. Fabricar no equivale a recibir físicamente el producto.
- La modalidad automática existente continúa siendo una decisión independiente del responsable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Mostrar físico, reserva, disponible y previsto con definiciones separadas.
- **FR-002**: Filtrar por compañía, depósito, ubicación y producto antes de calcular resultados.
- **FR-003**: Usar movimientos y operaciones nativas para recepciones, entregas y transferencias.
- **FR-004**: Conservar pendientes, devoluciones y relaciones con documentos comerciales.
- **FR-005**: Agrupar conteos por ubicación y generar ajustes mediante mecanismos nativos.
- **FR-006**: Conservar responsable, fecha, motivo y trazabilidad del ajuste.

- **FR-007**: Buscar productos y series/lotes por nombre, código o referencia textual; conservar ceros iniciales, compañía y selección, con páginas de hasta30 resultados.
- **FR-008**: Consultar con paginación de30 los movimientos finalizados de una serie/lote: fecha, producto, unidad, cantidad, origen/destino, devolución y documento; incluir los hechos nativos disponibles sin reinterpretar reservas como entregas.
- **FR-009**: Separar historia filtrada y cantidades actuales visibles por ubicación/propietario/paquete; informar fecha de consulta, unidad, alcance y ausencia de permiso sin inventar cero.
- **FR-010**: Abrir documentos y trazabilidad avanzada por sus referencias/permisos nativos; no asignar facturas, cobros ni cantidades comerciales a un lote sin evidencia directa.
- **FR-011**: Crear explícitamente una serie/lote con producto rastreable y número, referencia opcional y compañía deducida; reintentar el mismo alta devuelve su resultado, sin registrar existencias ni cambiar el seguimiento del producto.
- **FR-012**: Configurar reglas de reposición con producto, ubicación y mínimos/máximos; proponer depósito/compañía conocidos, crear reglas ARG en modalidad manual y conservar las modalidades existentes. Guardar o consultar no ejecuta abastecimiento.
- **FR-013**: Presentar físico, previsto, abastecimiento en curso y sugerencia de reposición con sus unidades, compañía, ubicación, momento de consulta y horizonte. Conservar el cálculo de la plataforma y explicar información inaccesible, sin inventar ceros ni sumar unidades distintas.
- **FR-014**: Permitir seleccionar hasta30 reglas por confirmación y elegir cantidades positivas revisables. Mostrar ruta, proveedor o lista de materiales y el efecto esperado antes de ejecutar; conservar el contenido elegido al volver de maestros.
- **FR-015**: Confirmar explícitamente compra o fabricación por las cantidades aceptadas, con validación de permisos y compañía, revisión de cambios y ejecución atómica del conjunto. Considerar documentos nuevos y ampliaciones, fabricación por lotes/componentes y estados nativos resultantes; no registrar una recepción, factura o pago ficticio.
- **FR-016**: Conservar evidencia inmutable de cada confirmación y referencias/cambios de sus documentos originales. Repetir la misma solicitud devuelve el mismo resultado; reutilizar su identidad con otras cantidades se rechaza. Una reposición nueva exige otra revisión.
- **FR-017**: Abrir resultados sólo con acceso a sus documentos y dimensiones. Una capacidad de compra o fabricación ausente debe explicar qué falta; la modularidad no reduce la entrega completa a compras.

### Key Entities

- **Existencia**: producto, ubicación, lote, cantidad, reserva.
- **Movimiento**: origen, destino, cantidad, unidad, lote y relaciones.
- **Conteo**: INV, ubicación, teórico, contado, diferencia y movimientos.
- **Regla de reposición**: producto, compañía, ubicación, límites, modalidad y ruta.
- **Propuesta de reposición**: momento/horizonte, regla, cantidades sugeridas/elegidas y efectos esperados.
- **Confirmación de reposición**: responsable, cantidades aceptadas y referencias a documentos generados o ampliados; no otro saldo de stock.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-005**: Con dos datos principales se puede dar de alta una serie/lote y continuar a su consulta, sin un movimiento físico por esa alta.
- **SC-006**: Cada fila de trazabilidad identifica un único hecho nativo y permite localizar su origen autorizado; todas las cantidades muestran unidad y ámbito.
- **SC-007**: Guardar o consultar una regla de reposición produce cero documentos de compra, fabricación, recepción, facturación o pago.
- **SC-008**: El100% de confirmaciones de reposición muestra cantidades/unidades y efecto previsto, permite localizar sus resultados autorizados y conserva el mismo resultado al reintentar.

- **SC-001**: Completar los tres recorridos de aceptación con ejemplos identificados y sin datos reales.
- **SC-002**: Mantener el orden y significado de controles comunes en el 100% de pantallas entregadas.
- **SC-003**: Resolver cada operación desde una única fuente de información y conservar sus vínculos.
- **SC-004**: Identificar cada excepción y su siguiente acción sin requerir conocimiento técnico del usuario.

## Assumptions

- Usar microempresas y pymes con poco personal como público; permitir roles combinables.
- Conservar funciones avanzadas accesibles por permisos y mostrar complejidad progresivamente.
- Mantener carga mínima con valores configurados; nunca inventar datos desconocidos.
- Preparar QA funcional/visual posterior a la instalación, conforme al flujo acordado.
- Usar sólo datos de ejemplo; mantener servicios externos desactivados hasta su habilitación.
- Clasificar esta entrega como núcleo; conservar alcance definido en el plan maestro.
- Licencias adoptadas: AGPL-3.0 para código original y CC BY-SA 4.0 para documentación/recursos; conservar avisos y licencias de terceros según NOTICE.md.

## Incremento F14 ·2026-11-06

FR-007–011 amplían el núcleo existente. Fuente y QA se acreditan por separado. F15/reposición y
parent016T009 permanecen pendientes hasta completar su entrega propia; no se reduce el plan de22 capacidades.

## Incremento F15 ·2026-11-06

Estado F15: diseño revisado y base técnica en desarrollo; todavía sin instalar. F14 conserva
su entrega instalada. FR-012–017 y US6/US7 cubren configuración, propuesta y confirmación de compra/fabricación.
Se implementan por etapas sin presentar una consulta aislada ni una sola ruta como alcance cumplido.
Las funciones de fabricación son opcionales por instalación; su implementación y composición de
demostración forman parte de la entrega completa. QA y aceptación continúan como fases posteriores.
