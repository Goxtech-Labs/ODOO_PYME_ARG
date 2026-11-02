# Feature Specification: Circuito Compras ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Comercial, puente físico y ejes de dinero instalados técnicamente demo; QA funcional/visual y aceptación pendientes.

**Input**: Pedido a proveedor, entrada, factura recibida y devolución separados, con mínima carga y documentos vinculados.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Pedir al proveedor (Priority: P1)

Como comprador necesito crear un pedido con proveedor, productos y cantidades.

**Why this priority**: Entregar pedir al proveedor con el orden común y decisiones mínimas.

**Independent Test**: Guardar PPC-000001 y confirmar condiciones conocidas sin exigir circuitos departamentales adicionales.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** guardar PPC-000001 y confirmar condiciones conocidas sin exigir circuitos departamentales adicionales.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** mantener aprobación adicional sólo si el responsable la configura y preservar referencia del proveedor.

### User Story 2 - Recibir y registrar factura (Priority: P2)

Como operador necesito entradas y facturas recibidas independientes del pedido.

**Why this priority**: Entregar recibir y registrar factura con el orden común y decisiones mínimas.

**Independent Test**: Recibir parte del pedido mediante ENT y registrar FRC vinculada sin duplicar entrada.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** recibir parte del pedido mediante ENT y registrar FRC vinculada sin duplicar entrada.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** conservar cantidades pendientes y distinguir recepción cerrada de cumplimiento total.

### User Story 3 - Gestionar devolución (Priority: P2)

Como operador necesito devolver mercadería o registrar una nota vinculada sin borrar historia.

**Why this priority**: Entregar gestionar devolución con el orden común y decisiones mínimas.

**Independent Test**: Generar devolución desde entrada y consultar su efecto neto y documentos relacionados.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** generar devolución desde entrada y consultar su efecto neto y documentos relacionados.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** no descontar dos veces una devolución ni confundirla con cancelación del pedido.

### Edge Cases

- Estados nativos de compra: draft, sent, to approve, purchase y cancel; etiquetas ARG sin falsificar estado real.
- Usar product_qty, qty_received, qty_invoiced y qty_to_invoice según política del producto.
- Conservar unidad uom_id de purchase.order.line en la rama Odoo20 verificada.
- Usar relaciones de líneas, no sólo texto origin.
- No interpretar receipt_status full como prueba de todas las cantidades recibidas.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Gestionar pedido proveedor con estados y numeración propios.
- **FR-002**: Aplicar condiciones conocidas y permitir roles combinables en equipos pequeños.
- **FR-003**: Usar entradas y facturas recibidas nativas vinculadas por líneas.
- **FR-004**: Separar recepción física, registro de deuda y pago mediante Administración.
- **FR-005**: Registrar devoluciones y ajustes mediante documentos inversos vinculados.
- **FR-006**: Conservar moneda, impuestos, unidades y referencia original del proveedor.

### Key Entities

- **Pedido proveedor**: PPC, proveedor, partner_ref, moneda, product_qty, uom_id.
- **Entrada**: ENT y purchase_line_id con cantidades efectivas.
- **Factura recibida**: FRC, referencia fiscal proveedor y líneas de compra.

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
