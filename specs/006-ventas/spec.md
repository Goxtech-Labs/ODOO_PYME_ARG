# Feature Specification: Circuito Ventas ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Comercial, puente físico y ejes de dinero instalados técnicamente demo; QA funcional/visual y aceptación pendientes.

**Input**: Presupuesto propio PRE, pedido cliente PED independiente, entregas y facturas vinculadas sin duplicar efectos nativos.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Preparar y confirmar presupuesto (Priority: P1)

Como vendedor necesito un presupuesto como documento independiente del pedido de cliente.

**Why this priority**: Entregar preparar y confirmar presupuesto con el orden común y decisiones mínimas.

**Independent Test**: Guardar PRE-000001, confirmarlo y consultar sus líneas/condiciones sin movimientos de stock ni dinero.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** guardar PRE-000001, confirmarlo y consultar sus líneas/condiciones sin movimientos de stock ni dinero.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** bloquear cambios sobre la versión confirmada y permitir una revisión nueva con historia.

### User Story 2 - Generar pedido cliente (Priority: P2)

Como vendedor necesito crear un pedido posterior desde el presupuesto confirmado sin reescribir líneas.

**Why this priority**: Entregar generar pedido cliente con el orden común y decisiones mínimas.

**Independent Test**: Generar PED-000001 separado, enlazar PRE-000001 y conservar ambos documentos consultables.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** generar PED-000001 separado, enlazar PRE-000001 y conservar ambos documentos consultables.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** rechazar generación duplicada concurrente y mostrar el pedido existente.

### User Story 3 - Entregar y facturar (Priority: P2)

Como operador necesito distinguir pendiente de entrega, facturación y cobro.

**Why this priority**: Entregar entregar y facturar con el orden común y decisiones mínimas.

**Independent Test**: Consultar cantidades pedidas, entregadas y facturadas con sus documentos de origen y acceder al cobro de Administración.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** consultar cantidades pedidas, entregadas y facturadas con sus documentos de origen y acceder al cobro de Administración.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** separar faltante cerrado de cantidad cumplida y no crear otra entrega al facturar.

### Edge Cases

- Estados de presupuesto: borrador, emitido, confirmado, rechazado, vencido y cancelado; registrar revisión al cambiar condiciones confirmadas.
- Generar pedido mediante acción explícita; ofrecer confirmar y generar como acción combinada sólo si explica ambos efectos.
- Asignar PRE al presupuesto y PED al pedido; conservar numeración fiscal separada.
- Conservar sale.order como única fuente operativa de pedidos, entregas y facturación.
- Mantener bloqueo idempotente contra doble clic o concurrencia en generación del pedido.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Mantener Presupuesto ARG como registro propio con número y estados independientes.
- **FR-002**: Confirmar presupuesto preservando condiciones aprobadas y sin crear efectos físicos o contables.
- **FR-003**: Generar un pedido nativo distinto desde presupuesto confirmado y vincular sus líneas.
- **FR-004**: Conservar pedido, presupuesto y revisión aprobada sin convertir un documento en el otro.
- **FR-005**: Usar remitos y facturas nativos vinculados por líneas y permitir parciales según política.
- **FR-006**: Separar estados comerciales, físicos, contables, financieros y fiscales.

### Key Entities

- **Presupuesto**: PRE, cliente, moneda, fechas, líneas, condiciones, revisión.
- **Pedido**: PED, arg_quotation_id, arg_quotation_line_id, generation_key, cantidades y condiciones.
- **Derivados**: relaciones nativas de líneas y accesos a Administración.

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
