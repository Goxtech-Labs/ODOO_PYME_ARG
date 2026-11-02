# Feature Specification: Base ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Desarrollado y desplegado en demo; QA funcional/visual y aceptación pendientes.

**Input**: Configurar compañía, roles combinables, tipos/secuencias internas, ayuda por módulo y soporte general para micropymes.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Identificar documentos (Priority: P1)

Como operador necesito reconocer cada documento con código corto sin cargar números manualmente.

**Why this priority**: Entregar identificar documentos con el orden común y decisiones mínimas.

**Independent Test**: Asignar PRE-000001 y PED-000001 desde secuencias independientes y conservar ambos códigos.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** asignar PRE-000001 y PED-000001 desde secuencias independientes y conservar ambos códigos.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** rechazar una colisión, conservar números anulados y permitir crecimiento por encima de seis dígitos.

### User Story 2 - Configurar roles y preferencias (Priority: P2)

Como responsable necesito combinar funciones en pocas personas sin crear departamentos artificiales.

**Why this priority**: Entregar configurar roles y preferencias con el orden común y decisiones mínimas.

**Independent Test**: Asignar a una persona Ventas, Compras y Administración según permisos expresos.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** asignar a una persona Ventas, Compras y Administración según permisos expresos.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** rechazar acceso a otra compañía o acción fuera de permisos efectivos.

### User Story 3 - Ayuda y soporte central (Priority: P2)

Como usuario necesito tutoriales de mi módulo y un único soporte general administrado por el responsable.

**Why this priority**: Entregar ayuda y soporte central con el orden común y decisiones mínimas.

**Independent Test**: Actualizar un enlace YouTube central sin reinstalar el módulo y encontrarlo desde su ayuda.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** actualizar un enlace YouTube central sin reinstalar el módulo y encontrarlo desde su ayuda.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** mostrar guía escrita y estado pendiente cuando falte un video o canal de contacto.

### Edge Cases

- No reutilizar códigos anulados ni reiniciar por ejercicio implícitamente.
- Conservar código interno separado del número fiscal y del proveedor.
- Mantener compañía, zona horaria e idioma explícitos.
- Compartir configuración única de soporte; capturar contexto opcional sin exigirlo al usuario.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Asignar códigos internos por compañía y tipo al primer guardado.
- **FR-002**: Separar identificadores operativos de referencias fiscales y de terceros.
- **FR-003**: Ofrecer roles operativos combinables y configuración por compañía.
- **FR-004**: Aplicar permisos en servidor y conservar una administración avanzada accesible.
- **FR-005**: Mantener catálogo editable de tutoriales con versiones compatibles y revisión.
- **FR-006**: Configurar soporte general por correo, WhatsApp o tickets sin envíos automáticos.

### Key Entities

- **Tipo documental**: code, name, model, compañía, secuencia.
- **Referencia**: tipo, compañía, número, registro origen, código mostrado.
- **Ayuda**: módulo, tarea, URL, versión, guía, estado, revisión, sustituto.
- **Soporte**: URL general, canal principal, correo, WhatsApp, tickets.

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
