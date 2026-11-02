# Feature Specification: Circuito Informes ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Desarrollado e instalado técnicamente demo y entorno aislado; QA funcional/visual y aceptación pendientes.

**Input**: Informes con hechos, dimensiones, unidades y corte claros para decidir sin conocimientos contables avanzados.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Leer hechos separados (Priority: P1)

Como responsable necesito distinguir ventas, entregas, cobros, compras y existencias.

**Why this priority**: Entregar leer hechos separados con el orden común y decisiones mínimas.

**Independent Test**: Consultar facturación neta por fecha, tercero y producto con grano línea de factura.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** consultar facturación neta por fecha, tercero y producto con grano línea de factura.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** no sumar presupuesto con factura ni presentar cobro como venta.

### User Story 2 - Filtrar y explicar (Priority: P2)

Como usuario necesito partir de pocos filtros y abrir el documento de origen.

**Why this priority**: Entregar filtrar y explicar con el orden común y decisiones mínimas.

**Independent Test**: Filtrar compañía, período y moneda y abrir las líneas que componen un total.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** filtrar compañía, período y moneda y abrir las líneas que componen un total.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** rechazar comparación sin moneda homogénea y respetar acceso al documento original.

### User Story 3 - Exportar e imprimir (Priority: P2)

Como responsable necesito sacar un informe utilizable fuera del sistema.

**Why this priority**: Entregar exportar e imprimir con el orden común y decisiones mínimas.

**Independent Test**: Exportar CSV UTF-8 y PDF con filtros, moneda, fecha y totales consistentes.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** exportar CSV UTF-8 y PDF con filtros, moneda, fecha y totales consistentes.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** proteger contra fórmulas en CSV y no exportar columnas restringidas.

### Edge Cases

- Comparar total de detalle y agrupado por igual corte y moneda.
- Notas de crédito y devoluciones tienen signo explícito y vínculo al original.
- Stock actual y stock a fecha son consultas diferentes; el histórico se deriva de movimientos.
- No depender de account_reports Enterprise; usar modelos/reportes Community. Habilitar cada informe sólo si su modelo fuente está instalado; Informes no obliga a instalar todos los circuitos.
- Aplicar precisión de moneda/unidad, sin redondear cada agrupación de forma inconsistente.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Definir grano, fuente, fecha, moneda y signo por medida.
- **FR-002**: Separar hechos de operación, contabilidad y caja en consultas y etiquetas.
- **FR-003**: Usar dimensiones compartidas y navegación a fuente autorizada.
- **FR-004**: Aplicar filtros en servidor y mostrar corte y criterio de cada total.
- **FR-005**: Ofrecer salida abierta y documento legible con metadatos de corte.
- **FR-006**: Conservar importes y cantidades sin sumar monedas o unidades incompatibles.

### Key Entities

- **Hecho facturación**: línea publicada, signo, cantidad, neto, moneda, fecha contable.
- **Hecho caja y deuda**: liquidez y residuales separados de aplicaciones.
- **Dimensiones**: compañía, tercero, producto, moneda, depósito, fecha.

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
