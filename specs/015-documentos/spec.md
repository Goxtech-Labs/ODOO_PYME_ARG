# Feature Specification: Motor documental e impresión ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Desarrollado e instalado técnicamente; QA y aceptación pendientes.

**Input**: Identidad, vínculos y presentación documental común sin reemplazar los modelos operativos nativos.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Identificar documento (Priority: P1)

Como usuario necesito reconocer tipo, número, fecha y estado de cualquier documento.

**Why this priority**: Entregar identificar documento con el orden común y decisiones mínimas.

**Independent Test**: Abrir PRE-000001 y distinguir su número interno de referencias fiscales o externas.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** abrir PRE-000001 y distinguir su número interno de referencias fiscales o externas.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** no reutilizar una secuencia cancelada ni mezclar compañías.

### User Story 2 - Vincular derivados (Priority: P2)

Como operador necesito recorrer origen y derivados por cabecera y línea.

**Why this priority**: Entregar vincular derivados con el orden común y decisiones mínimas.

**Independent Test**: Desde PRE confirmado abrir PED distinto con trazabilidad de cada línea.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** desde PRE confirmado abrir PED distinto con trazabilidad de cada línea.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** impedir un segundo PED por reintento de la misma confirmación.

### User Story 3 - Imprimir (Priority: P2)

Como usuario necesito un PDF simple y consistente.

**Why this priority**: Entregar imprimir con el orden común y decisiones mínimas.

**Independent Test**: Generar PDF con identidad ARG, tercero, detalle, totales y estado correcto.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** generar PDF con identidad ARG, tercero, detalle, totales y estado correcto.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** marcar borrador/ejemplo y no mostrar autorización fiscal inexistente.

### Lectura transversal de parciales

1. **Given** un PED confirmado por 10 unidades, con 4 entregadas y 2 facturadas, **When** se consulta,
   **Then** muestra simultáneamente confirmado, entrega parcial y facturación parcial, con 6 y 8 pendientes respectivamente.
2. **Given** un REC confirmado por100000, con60000 aplicados, **When** se consulta,
   **Then** muestra aplicación parcial y40000 libres, conservando las facturas y conciliaciones que explican el avance.
3. **Given** una factura parcial totalmente cobrada, **When** se consulta el pedido origen,
   **Then** distingue el cobro sobre lo facturado del alcance aún sin facturar del pedido.
4. **Given** una FAC por100000 y un REC en borrador por100000, **When** se consulta la factura,
   **Then** sigue pendiente de cobro; sólo el dinero confirmado y aplicado modifica ese eje.
5. **Given** una FAC por100000 con40000 de dinero confirmado y aplicado, **When** se consulta,
   **Then** muestra cobrado parcialmente,60000 pendientes y el REC que explica el importe.
6. **Given** un pedido de10 unidades con4 entregadas y6 canceladas, **When** se consulta,
   **Then** conserva entrega parcial4/10 y cierre con faltante6; no muestra entrega completa.

Escenarios previstos para QA posterior; no acreditar ejecución por su inclusión documental.
El contrato vinculante está en [estados y pendientes](../../docs/tecnica/ESTADOS-Y-PENDIENTES.md).

### Edge Cases

- Presupuesto y pedido son documentos distintos, no dos vistas o estados del mismo sale.order.
- Los documentos nativos conservan su name técnico cuando sea necesario; arg_number se muestra como identificador interno ARG.
- Confirmar PRE preserva condiciones y no genera PED automáticamente; Generar pedido es la acción explícita posterior e idempotente. Ninguna de las dos registra por sí sola asiento, cobro ni movimiento de stock.
- Códigos estables; nunca renumerar documentos existentes al cambiar configuración.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Asignar código corto e identidad inmutable al primer guardado documental válido.
- **FR-002**: Separar secuencia interna, número fiscal y referencia de tercero.
- **FR-003**: Conservar relaciones de origen y derivados y cantidades netas por línea. Mostrar simultáneamente los ejes aplicables de confirmación, entrega/recepción, facturación y cobro/pago, cada uno pendiente, parcial o completo según su cantidad o importe. REC/OPA muestran además aplicación e importe libre; un documento relacionado en borrador no acredita cumplimiento.
- **FR-004**: Preservar documento origen, revisión e historial tras generar derivados.
- **FR-005**: Proveer plantillas QWeb originales con jerarquía y orden común.
- **FR-006**: Respetar permisos, moneda, unidades y datos históricos al imprimir.

### Key Entities

- **Identidad**: company_id, arg_document_type_id, arg_number y display code.
- **Relación**: quote_id, quotation_line_id, sale_line_id y relaciones nativas.
- **Impresión**: layout, marca, totales y metadatos.

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
