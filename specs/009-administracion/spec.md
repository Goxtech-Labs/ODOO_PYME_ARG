# Feature Specification: Circuito Administración ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Desarrollado e instalado técnicamente demo y entorno aislado; QA funcional/visual y aceptación pendientes.

**Input**: Recibos, órdenes de pago, cajas y cuentas corrientes con imputaciones claras y fuente contable única.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consultar deuda (Priority: P1)

Como responsable necesito ver qué se debe, por documento, vencimiento y moneda.

**Why this priority**: Entregar consultar deuda con el orden común y decisiones mínimas.

**Independent Test**: Consultar facturas publicadas y saldos residuales separados por moneda y compañía.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** consultar facturas publicadas y saldos residuales separados por moneda y compañía.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** excluir borradores y no sumar ARS con USD ni confundir una relación con una conciliación.

### User Story 2 - Cobrar o pagar (Priority: P2)

Como operador necesito registrar importe y medio e imputarlo a documentos.

**Why this priority**: Entregar cobrar o pagar con el orden común y decisiones mínimas.

**Independent Test**: Crear REC u OPA con un medio y aplicar un pago parcial conservando saldo pendiente.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** crear REC u OPA con un medio y aplicar un pago parcial conservando saldo pendiente.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** permitir anticipo sin factura y exigir cuentas transitorias configuradas antes de contabilizar.

### User Story 3 - Revisar caja y revertir (Priority: P2)

Como responsable necesito consultar movimientos y corregir con trazabilidad.

**Why this priority**: Entregar revisar caja y revertir con el orden común y decisiones mínimas.

**Independent Test**: Consultar caja por diario y fecha y revertir una aplicación conservando historial.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** consultar caja por diario y fecha y revertir una aplicación conservando historial.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** impedir borrar evidencia publicada y distinguir caja, banco, deuda y conciliación.

### Edge Cases

- Estados nativos de pago Odoo20: draft, paid, reconciled, canceled y rejected; no usar posted como estado de pago.
- Usar account.payment.register y conciliación nativa; no escribir residuales manualmente.
- REC/OPA confirmado exige efectos contables verificables; separar borrador, confirmado, parcialmente aplicado, aplicado y revertido.
- Separar documento recibo de pago y account.move out_receipt/in_receipt, que no son recibos de cobranza.
- No almacenar tarjetas ni claves bancarias; las referencias de operación no ejecutan transferencias.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Derivar deuda de apuntes contables publicados y sus residuales.
- **FR-002**: Mostrar origen, vencimiento y aplicaciones sin duplicar saldos.
- **FR-003**: Agrupar uno o varios pagos nativos en recibo u orden con secuencia propia.
- **FR-004**: Usar conciliación nativa y conservar imputaciones por documento y moneda.
- **FR-005**: Derivar movimientos de liquidez de apuntes publicados del diario.
- **FR-006**: Registrar reversión y desaplicación mediante acciones nativas y permisos efectivos.

### Key Entities

- **Recibo / orden**: REC/OPA, tercero, fecha, moneda, payment_ids y total.
- **Pago**: payment_type, partner_type, journal_id, payment_method_line_id, amount, date, memo.
- **Imputación**: debit_move_id, credit_move_id, amount y importes en moneda.

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
