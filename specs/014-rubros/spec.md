# Feature Specification: Extensiones por rubro y personalizaciones ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Especificado para programación; código propio pendiente.

**Input**: Proceso y contrato para agregar rubros sin imponer reglas sectoriales al núcleo genérico.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Definir alcance (Priority: P1)

Como comunidad necesito describir un rubro mediante casos reales anonimizados.

**Why this priority**: Entregar definir alcance con el orden común y decisiones mínimas.

**Independent Test**: Completar plantilla con problema, documentos, campos mínimos y exclusiones.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** completar plantilla con problema, documentos, campos mínimos y exclusiones.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** rechazar supuestos de otro cliente que contradigan la gestión genérica.

### User Story 2 - Extender sin duplicar (Priority: P2)

Como desarrollador necesito agregar campos y operaciones coherentes.

**Why this priority**: Entregar extender sin duplicar con el orden común y decisiones mínimas.

**Independent Test**: Proponer addon arg_pyme_rubro_nombre con extensiones y relaciones al núcleo.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** proponer addon arg_pyme_rubro_nombre con extensiones y relaciones al núcleo.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** resolver conflicto entre reglas de rubros mediante composición explícita.

### User Story 3 - Documentar entrega (Priority: P2)

Como usuario necesito saber qué agrega y cómo aprenderlo.

**Why this priority**: Entregar documentar entrega con el orden común y decisiones mínimas.

**Independent Test**: Encontrar manual, datos de ejemplo, tutorial y notas de compatibilidad por rubro.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** encontrar manual, datos de ejemplo, tutorial y notas de compatibilidad por rubro.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** conservar datos al deshabilitar menús y documentar límites de desinstalación.

### Edge Cases

- Indumentaria, comercio, servicios y otros rubros son candidatos, no funciones prometidas en el núcleo.
- Una regla exclusiva de cliente permanece en su personalización.
- Toda integración externa nueva se registra en Integraciones ARG.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Exigir spec independiente para cada rubro o personalización.
- **FR-002**: Expresar dependencias y compatibilidad sin modificar reglas generales implícitamente.
- **FR-003**: Mantener nombres ARG y contratos documentales comunes.
- **FR-004**: No crear otra contabilidad, otro stock ni otro módulo de proveedores externos.
- **FR-005**: Registrar instalación, QA, aceptación y versión del rubro por separado.
- **FR-006**: Mantener configuración especializada opcional y tutoriales versionados.

### Key Entities

- **Rubro**: casos, documentos, dimensiones, dependencias.
- **Extensión**: campos, métodos, vistas y permisos.
- **Composición**: versiones y módulos compatibles.

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
- Clasificar esta entrega como posterior al núcleo; conservar alcance definido en el plan maestro.
- Licencias adoptadas: AGPL-3.0 para código original y CC BY-SA 4.0 para documentación/recursos; conservar avisos y licencias de terceros según NOTICE.md.
