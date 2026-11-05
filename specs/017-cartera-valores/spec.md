# Feature Specification: Cartera de valores y tesorería argentina

**Feature Branch**: `codex-notebook/plan-001`
**Created**: 2026-11-05
**Status**: Diseño para implementación incremental; no instalado.
**Input**: Procesos FactuSOL adaptados a Argentina, simplicidad y fuentes nativas.

## User Scenarios & Testing

### User Story 1 - Cargar lo básico (Priority: P1)

Recibir un cheque o registrar uno propio, identificarlo una sola vez y usarlo como medio de REC/OPA.

**Why this priority**: permite una entrada útil sin módulos adicionales innecesarios.
**Independent Test**: registrar un borrador completo con datos esenciales, sin movimientos ni envíos.
**Acceptance Scenarios**:
1. **Given** datos maestros configurados, **When** ingreso fecha/tercero/concepto, **Then** el sistema deduce lo conocido y conserva mis correcciones.
2. **Given** un registro existente, **When** lo reabro, **Then** no cambia su fecha ni se duplica su identidad.

### User Story 2 - Ejecutar el circuito (Priority: P1)

Recepción → cartera → endoso/entrega, depósito o negociación → liquidación o rechazo; propio → emisión registrada → entrega → débito o devolución.

**Independent Test**: Factura de120000ARS: REC con20000 efectivo y100000 cheque aplica120000 a deuda; efectivo20000, cartera100000 y banco acreditado0. Depositar no genera otro cobro; acreditar reclasifica. Un rechazo revierte/reclama sólo el valor vinculado, preservando efectivo e historia.
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
- El nominal es positivo, en la moneda del instrumento, y no cambia después del primer evento confirmado.

## Requirements

### Functional Requirements

- **FR-001**: Recibir un cheque o registrar uno propio, identificarlo una sola vez y usarlo como medio de REC/OPA.
- **FR-002**: Ofrecer el recorrido explícito: Recepción → cartera → endoso/entrega, depósito o negociación → liquidación o rechazo; propio → emisión registrada → entrega → débito o devolución.
- **FR-003**: Separar nominal disponible, aplicación de deuda, dinero acreditado/debitado y exposición por recurso. REC/OPA multim medio usa cuentas transitorias de valores y conciliación nativa, nunca residuales escritos a mano.
- **FR-004**: Conservar identidad, relaciones de origen y eventos de corrección sin duplicar efectos.
- **FR-005**: Mostrar pendientes por eje y fuente, sin sumar monedas ni hechos incompatibles.
- **FR-006**: Aplicar fecha de hoy propuesta/carga mínima y permisos efectivos con manual/tutoría versionados.
- **FR-007**: El nominal es positivo, en la moneda del instrumento, y no cambia después del primer evento confirmado.
- **FR-008**: Un instrumento no puede estar reservado o comprometido simultáneamente por dos salidas.
- **FR-009**: Transmitir el título no fracciona su identidad; imputar su importe a varias facturas es otra operación.
- **FR-010**: El nominal en cartera no es dinero bancario disponible ni se vuelve a cobrar al liquidarlo.
- **FR-011**: Evento confirmado es inmutable; reversión explícita enlazada conserva historia y revisa su efecto contable.
- **FR-012**: La integración bancaria no se ejecuta desde un formulario de cartera ni se infiere de una referencia manual.

### Key Entities

Instrumento: compañía, origen propio/tercero, soporte papel/ECHEQ, clase común/diferido, moneda, nominal, banco/cuenta libradora, número/identificador, librador, tercero entregante, beneficiario y fechas. Evento: operación, actor, fecha, instrumento, origen/destino, evidencia, estado externo y efecto nativo. Lote de pagos/transferencia: instrucciones y ejecuciones vinculadas. Pagaré: instrumento distinto con vencimiento y rol propio/tercero.

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
