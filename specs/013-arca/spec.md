# Feature Specification: Contrato futuro ARCA dentro de Integraciones ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Especificado para programación; código propio pendiente.

**Input**: Preparar adaptador fiscal futuro con homologación separada y trazabilidad; no habilitar emisión real en ejemplos.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configurar emisor (Priority: P1)

Como administrador necesito separar compañía, emisor, punto de venta y ambiente.

**Why this priority**: Entregar configurar emisor con el orden común y decisiones mínimas.

**Independent Test**: Validar configuración de homologación sin usar CUIT o certificados reales del usuario.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** validar configuración de homologación sin usar CUIT o certificados reales del usuario.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** bloquear producción sin configuración y autorización específicas.

### User Story 2 - Autorizar comprobante (Priority: P2)

Como operador necesito conocer el estado fiscal exacto.

**Why this priority**: Entregar autorizar comprobante con el orden común y decisiones mínimas.

**Independent Test**: Preparar solicitud consistente y registrar autorización, rechazo o resultado incierto.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** preparar solicitud consistente y registrar autorización, rechazo o resultado incierto.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** consultar último autorizado ante timeout antes de solicitar otra numeración.

### User Story 3 - Mostrar evidencia (Priority: P2)

Como usuario necesito imprimir el estado correcto y corregir por documento inverso.

**Why this priority**: Entregar mostrar evidencia con el orden común y decisiones mínimas.

**Independent Test**: Distinguir borrador, pendiente, autorizado y rechazado en pantalla e impresión.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** distinguir borrador, pendiente, autorizado y rechazado en pantalla e impresión.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** no imprimir CAE ficticio ni borrar un comprobante autorizado.

### Edge Cases

- La localización l10n_ar Community no incluye por sí sola autorización electrónica.
- Esta spec no acredita compatibilidad fiscal; verificar documentación oficial y homologación al implementar.
- No realizar emisión ni comunicación fiscal real durante desarrollo con datos de ejemplo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Mantener emisor, ambiente y punto de venta separados del código interno.
- **FR-002**: Referenciar certificados y claves protegidas sin incorporarlos al repositorio.
- **FR-003**: Implementar autorización idempotente y recuperación de resultado incierto.
- **FR-004**: Conservar número fiscal, tipo, emisor, punto de venta y evidencia de respuesta.
- **FR-005**: Incluir datos fiscales sólo desde respuesta válida y contrato vigente.
- **FR-006**: Emitir correcciones mediante documentos vinculados y preservar historial.

### Key Entities

- **Emisor**: compañía, CUIT, PV, ambiente, certificado_ref.
- **Solicitud**: idempotencia fiscal, hash, resultado y correlación.
- **Comprobante fiscal**: tipo, número, emisor, autorización y fechas.

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
- Clasificar esta entrega como posterior al núcleo; homologación pendiente; conservar alcance definido en el plan maestro.
- Licencias adoptadas: AGPL-3.0 para código original y CC BY-SA 4.0 para documentación/recursos; conservar avisos y licencias de terceros según NOTICE.md.
