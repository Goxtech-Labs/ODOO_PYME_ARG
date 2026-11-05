# Feature Specification: Punto de venta ARG

**Feature Branch**: `codex-notebook/plan-001`
**Created**: 2026-11-05
**Status**: Diseño para implementación incremental; no instalado.
**Input**: Procesos FactuSOL adaptados a Argentina, simplicidad y fuentes nativas.

## User Scenarios & Testing

### User Story 1 - Cargar lo básico (Priority: P2)

Abrir sesión autorizada, elegir artículos/cantidades y medios; fecha/hora nativas automáticas.

**Why this priority**: permite una entrada útil sin módulos adicionales innecesarios.
**Independent Test**: registrar un borrador completo con datos esenciales, sin movimientos ni envíos.
**Acceptance Scenarios**:
1. **Given** datos maestros configurados, **When** ingreso fecha/tercero/concepto, **Then** el sistema deduce lo conocido y conserva mis correcciones.
2. **Given** un registro existente, **When** lo reabro, **Then** no cambia su fecha ni se duplica su identidad.

### User Story 2 - Ejecutar el circuito (Priority: P2)

Sesión → venta → cobro → ticket/factura según caso → devolución → cierre y conciliación.

**Independent Test**: Pedido POS con dos medios y devolución parcial conserva un único cobro/stock; cierre diferencia efectivo contado de saldo esperado y factura vinculada no duplica venta.
**Acceptance Scenarios**:
1. **Given** un borrador válido, **When** confirmo la acción explícita, **Then** sólo ocurren los efectos de ese paso.
2. **Given** reintento o corrección, **When** repito o revierto, **Then** conservo identidad, origen y evidencia sin doble efecto.

### User Story 3 - Consultar y explicar (Priority: P2)

Consultar estados, cantidades/importes y origen en el circuito y sus informes, por compañía/moneda.
**Independent Test**: explicar el saldo y cada derivado desde sus registros fuente.
**Acceptance Scenarios**:
1. **Given** operaciones parciales, **When** consulto, **Then** distingo pendiente, cumplido y cerrado por cada eje aplicable.
2. **Given** rol restringido, **When** accedo, **Then** sólo obtengo registros/campos permitidos.

### Edge Cases

- Reintentos concurrentes; fecha modificada; mezcla de compañías/monedas; cancelación con efectos ya publicados.
- Datos secundarios ausentes; permiso insuficiente; operación externa pendiente o incierta.
- Un cobro y un movimiento POS se registran una sola vez aunque exista enlace ARG.

## Requirements

### Functional Requirements

- **FR-001**: Abrir sesión autorizada, elegir artículos/cantidades y medios; fecha/hora nativas automáticas.
- **FR-002**: Ofrecer el recorrido explícito: Sesión → venta → cobro → ticket/factura según caso → devolución → cierre y conciliación.
- **FR-003**: Conservar pagos, stock, impuestos y asientos del POS nativo; puentes ARG sólo enlazan y clasifican. No crear REC duplicado por cada pago ya registrado por POS.
- **FR-004**: Conservar identidad, relaciones de origen y eventos de corrección sin duplicar efectos.
- **FR-005**: Mostrar pendientes por eje y fuente, sin sumar monedas ni hechos incompatibles.
- **FR-006**: Aplicar fecha de hoy propuesta/carga mínima y permisos efectivos con manual/tutoría versionados.
- **FR-007**: Un cobro y un movimiento POS se registran una sola vez aunque exista enlace ARG.
- **FR-008**: Un ticket no acredita autorización fiscal.
- **FR-009**: Devolución y devolución de dinero son efectos separados con origen.
- **FR-010**: La cuenta de demo no determina los permisos definitivos de cajero.

### Key Entities

Sesión, pedido/ticket, medios, diferencias de caja, factura vinculada y devolución nativas; relación documental ARG sin segunda contabilización.

## Success Criteria

- **SC-001**: Completar la carga ordinaria usando sólo esenciales y configuración válida.
- **SC-002**: Los reintentos no producen un segundo efecto en los escenarios de aceptación.
- **SC-003**: Cada efecto y saldo mostrado conduce a su fuente y corrección.
- **SC-004**: El recorrido de aceptación conserva compañía, moneda, historia y permisos.

## Assumptions

Fecha de hoy propuesta en una carga nueva según zona del usuario; conservar fechas existentes y de origen.
Carga principal: fecha, tercero, documento y conceptos/artículos; datos secundarios progresivos.
Una persona puede combinar roles; conservar ACL/compañías y guardas nativas. Código original AGPL-3.0-only,
documentación CC BY-SA4.0 y licencias de terceros preservadas. Integraciones externas únicamente en
arg_pyme_integraciones, deshabilitadas inicialmente. No hay operaciones reales ni migración automática
implícitas en este diseño. QA funcional/visual y aceptación se realizan después de la entrega técnica.
