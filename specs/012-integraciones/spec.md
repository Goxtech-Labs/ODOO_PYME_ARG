# Feature Specification: Integraciones ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Especificado para programación; código propio pendiente.

**Input**: Único módulo para configuración, salud y adaptadores de todos los proveedores externos; posterior al núcleo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configurar proveedor (Priority: P1)

Como administrador necesito habilitar sólo el servicio elegido.

**Why this priority**: Entregar configurar proveedor con el orden común y decisiones mínimas.

**Independent Test**: Crear configuración por compañía y entorno con secreto referenciado fuera de Git.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** crear configuración por compañía y entorno con secreto referenciado fuera de Git.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** deshabilitar por defecto y detectar configuración incompleta sin revelar claves.

### User Story 2 - Ejecutar con control (Priority: P2)

Como operador necesito enviar una operación autorizada sin duplicados.

**Why this priority**: Entregar ejecutar con control con el orden común y decisiones mínimas.

**Independent Test**: Encolar una operación con clave idempotente y registrar resultado sanitizado.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** encolar una operación con clave idempotente y registrar resultado sanitizado.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** resolver timeout como estado incierto y consultar proveedor antes de repetir.

### User Story 3 - Diagnosticar y detener (Priority: P2)

Como responsable necesito ver fallos y detener envíos.

**Why this priority**: Entregar diagnosticar y detener con el orden común y decisiones mínimas.

**Independent Test**: Pausar proveedor y consultar intentos sin contenido sensible.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** pausar proveedor y consultar intentos sin contenido sensible.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** conservar evidencia al rotar credenciales o revocar servicio.

### Edge Cases

- No conservar payload sensible completo en logs.
- Estados draft, queued, processing, succeeded, failed, uncertain y canceled con transiciones explícitas.
- Timeout requiere lookup y conciliación antes de reintentar efectos irreversibles.
- Deshabilitar proveedor conserva jobs e historia. La desinstalación del addon requiere política explícita de conservación/exportación y no equivale a deshabilitar.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Agrupar todos los proveedores dentro del único addon Integraciones ARG.
- **FR-002**: Separar permisos, entorno y credenciales por compañía/proveedor.
- **FR-003**: Definir contrato de adaptadores, outbox e idempotencia por operación.
- **FR-004**: Aplicar límites, reintentos acotados y bloqueo concurrente sin duplicar efectos.
- **FR-005**: Ofrecer estado, última ejecución, error útil y pausa efectiva.
- **FR-006**: No usar pruebas de conexión que emitan facturas o mensajes reales.

### Key Entities

- **Conector**: compañía, proveedor, ambiente, habilitado y referencia de secreto.
- **Operación**: clave, estado, hash de petición, intentos y referencia externa.
- **Adaptador**: prepare, validate, execute, lookup, redact.

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
