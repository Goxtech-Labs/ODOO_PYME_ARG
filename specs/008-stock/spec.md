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

### Edge Cases

- Una transferencia interna es neutra para el total de empresa y cambia saldos por ubicación.
- Distinguir demanda product_uom_qty, cantidad operada quantity y cantidades finalizadas.
- Usar backorders y retornos nativos, conservando enlaces.
- No escribir qty_delivered o qty_received comerciales cuando derivan de movimientos.
- No generar stock por editar tarifas ni contabilizar otra entrada al registrar factura.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Mostrar físico, reserva, disponible y previsto con definiciones separadas.
- **FR-002**: Filtrar por compañía, depósito, ubicación y producto antes de calcular resultados.
- **FR-003**: Usar movimientos y operaciones nativas para recepciones, entregas y transferencias.
- **FR-004**: Conservar pendientes, devoluciones y relaciones con documentos comerciales.
- **FR-005**: Agrupar conteos por ubicación y generar ajustes mediante mecanismos nativos.
- **FR-006**: Conservar responsable, fecha, motivo y trazabilidad del ajuste.

### Key Entities

- **Existencia**: producto, ubicación, lote, cantidad, reserva.
- **Movimiento**: origen, destino, cantidad, unidad, lote y relaciones.
- **Conteo**: INV, ubicación, teórico, contado, diferencia y movimientos.

## Success Criteria *(mandatory)*

### Measurable Outcomes

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
