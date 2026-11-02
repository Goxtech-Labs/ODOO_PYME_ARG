# Feature Specification: Portada y documentación pública ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Documentación implementada; publicación remota, QA y aceptación pendientes.

**Input**: Portada de repositorio como entrada al proyecto, documentación navegable, identidad argentina y participación comunitaria.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Conocer el proyecto (Priority: P1)

Como visitante necesito entender propósito, estado y cómo instalar.

**Why this priority**: Entregar conocer el proyecto con el orden común y decisiones mínimas.

**Independent Test**: Abrir README y encontrar propósito, cinco circuitos, autoría y enlaces de inicio.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** abrir README y encontrar propósito, cinco circuitos, autoría y enlaces de inicio.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** no presentar una especificación como función instalada ni prometer soporte contratado.

### User Story 2 - Aprender por módulo (Priority: P2)

Como usuario necesito manual y tutorial compatibles.

**Why this priority**: Entregar aprender por módulo con el orden común y decisiones mínimas.

**Independent Test**: Encontrar manual y ficha de video por módulo, versión y estado.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** encontrar manual y ficha de video por módulo, versión y estado.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** ofrecer manual cuando no exista video vigente y no inventar canal o URL.

### User Story 3 - Participar (Priority: P2)

Como colaborador necesito reglas, límites y tareas accesibles.

**Why this priority**: Entregar participar con el orden común y decisiones mínimas.

**Independent Test**: Encontrar CONTRIBUTING, roadmap y plantilla de propuesta con referencia a spec.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** encontrar CONTRIBUTING, roadmap y plantilla de propuesta con referencia a spec.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** evitar secretos, datos de clientes y material FactuSOL en aportes públicos.

### Edge Cases

- El repositorio conserva documentación original y fuentes públicas con atribución.
- El sitio GitHub Pages es opcional posterior; README funciona sin desplegar otro servicio.
- No publicar credenciales, dumps, filestore ni referencias privadas de infraestructura.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Presentar ARG y soberanía con branding Goxtech discreto.
- **FR-002**: Mostrar estados de desarrollo y experiencia de Gonzalo Sarubilo como aporte declarado.
- **FR-003**: Centralizar catálogo versionado de tutoriales y revisiones.
- **FR-004**: Vincular documentos a cada módulo y conservar contenido anterior identificado.
- **FR-005**: Documentar flujo de contribución y reconocimiento comunitario.
- **FR-006**: Mantener servicios profesionales opcionales y secundarios al objetivo.

### Key Entities

- **Página**: README, manifiesto, identidad y mapa.
- **Tutorial**: módulo, versión, URL, fecha de revisión, reemplazo.
- **Aporte**: spec, cambio propuesto, evidencia, autor.

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
- Clasificar esta entrega como documentación comunitaria; conservar alcance definido en el plan maestro.
- Licencias adoptadas: AGPL-3.0 para código original y CC BY-SA 4.0 para documentación/recursos; conservar avisos y licencias de terceros según NOTICE.md.
