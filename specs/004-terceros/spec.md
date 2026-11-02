# Feature Specification: Terceros ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Desarrollado e instalado técnicamente; QA y aceptación pendientes.

**Input**: Gestionar clientes y proveedores con una ficha por identidad, alta rápida y datos fiscales/comerciales progresivos.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Alta mínima (Priority: P1)

Como operador necesito dar de alta un tercero con datos disponibles y completar lo demás cuando corresponda.

**Why this priority**: Entregar alta mínima con el orden común y decisiones mínimas.

**Independent Test**: Guardar un contacto de ejemplo con nombre y rol y continuar el documento.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** guardar un contacto de ejemplo con nombre y rol y continuar el documento.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** permitir borrador sin datos fiscales desconocidos y señalar requisitos antes de la operación que los necesita.

### User Story 2 - Combinar roles (Priority: P2)

Como responsable necesito que un mismo tercero pueda ser cliente y proveedor sin duplicar sus datos.

**Why this priority**: Entregar combinar roles con el orden común y decisiones mínimas.

**Independent Test**: Agregar rol proveedor a un cliente y conservar identidad, contactos e historia.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** agregar rol proveedor a un cliente y conservar identidad, contactos e historia.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** advertir posibles duplicados sin fusionar automáticamente identidades diferentes.

### User Story 3 - Aplicar condiciones (Priority: P2)

Como operador necesito condiciones predeterminadas sin volver a escribirlas en cada documento.

**Why this priority**: Entregar aplicar condiciones con el orden común y decisiones mínimas.

**Independent Test**: Aplicar moneda, tarifa, plazo y dirección conocidas al crear un documento.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** aplicar moneda, tarifa, plazo y dirección conocidas al crear un documento.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** conservar corrección explícita del usuario y no completar con datos inventados.

### Edge Cases

- No fusionar registros por coincidencia parcial de nombre.
- Validar formato de CUIT separado de verificación remota de padrón.
- No activar consultas externas al guardar una ficha.
- Permitir importar ejemplos con clave estable y conservar ceros iniciales en códigos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Permitir alta rápida con nombre y rol y ampliar información en la misma ficha.
- **FR-002**: Separar datos necesarios para borrador, contacto, entrega y facturación.
- **FR-003**: Mantener roles combinables sobre una sola identidad.
- **FR-004**: Buscar por nombre, código y datos identificatorios disponibles con permisos efectivos.
- **FR-005**: Organizar identificación, contacto, condiciones e información adicional en orden estable.
- **FR-006**: Transmitir valores predeterminados por compañía sin reescribir documentos históricos.

### Key Entities

- **Tercero**: name, is_company, parent_id, direcciones, contactos, vat, país.
- **Roles**: roles de gestión y vínculos nativos disponibles.
- **Condiciones**: tarifa, plazo, moneda, contactos y domicilios.

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
