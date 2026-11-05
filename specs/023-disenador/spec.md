# Feature Specification: Diseñador documental e informes ARG

**Feature Branch**: `codex-notebook/plan-001`
**Created**: 2026-11-05
**Status**: Diseño para implementación incremental; no instalado.
**Input**: Procesos FactuSOL adaptados a Argentina, simplicidad y fuentes nativas.

## User Scenarios & Testing

### User Story 1 - Cargar lo básico (Priority: P3)

Elegir documento y plantilla; cambiar logo, campos visibles, textos y disposición mediante controles acotados.

**Why this priority**: permite una entrada útil sin módulos adicionales innecesarios.
**Independent Test**: registrar un borrador completo con datos esenciales, sin movimientos ni envíos.
**Acceptance Scenarios**:
1. **Given** datos maestros configurados, **When** ingreso fecha/tercero/concepto, **Then** el sistema deduce lo conocido y conserva mis correcciones.
2. **Given** un registro existente, **When** lo reabro, **Then** no cambia su fecha ni se duplica su identidad.

### User Story 2 - Ejecutar el circuito (Priority: P3)

Plantilla borrador → vista previa con ejemplos → revisión → activar versión → imprimir/exportar con versión trazable.

**Independent Test**: Activar una plantilla con logo y notas, imprimir documento existente conservando totales; un usuario sin permiso no activa y un campo no permitido es rechazado.
**Acceptance Scenarios**:
1. **Given** un borrador válido, **When** confirmo la acción explícita, **Then** sólo ocurren los efectos de ese paso.
2. **Given** reintento o corrección, **When** repito o revierto, **Then** conservo identidad, origen y evidencia sin doble efecto.

### User Story 3 - Consultar y explicar (Priority: P2)

Consultar estados, cantidades/importes y origen en el circuito y sus informes, por compañía/moneda.
**Independent Test**: explicar el saldo y cada derivado desde sus registros fuente.
**Acceptance Scenarios**:
1. **Given** operaciones parciales, **When** consulto, **Then** distingo pendiente, cumplido y cerrado por cada eje aplicable.
2. **Given** rol restringido, **When** accedo, **Then** sólo obtengo registros/campos permitidos.

### Edge Cases

- Reintentos concurrentes; fecha modificada; mezcla de compañías/monedas; cancelación con efectos ya publicados.
- Datos secundarios ausentes; permiso insuficiente; operación externa pendiente o incierta.
- La activación no reescribe documentos ni sus condiciones históricas.

## Requirements

### Functional Requirements

- **FR-001**: Elegir documento y plantilla; cambiar logo, campos visibles, textos y disposición mediante controles acotados.
- **FR-002**: Ofrecer el recorrido explícito: Plantilla borrador → vista previa con ejemplos → revisión → activar versión → imprimir/exportar con versión trazable.
- **FR-003**: Diseñar presentación sin recalcular importes, cambiar hechos, ocultar requisitos fiscales necesarios ni ejecutar código arbitrario.
- **FR-004**: Conservar identidad, relaciones de origen y eventos de corrección sin duplicar efectos.
- **FR-005**: Mostrar pendientes por eje y fuente, sin sumar monedas ni hechos incompatibles.
- **FR-006**: Aplicar fecha de hoy propuesta/carga mínima y permisos efectivos con manual/tutoría versionados.
- **FR-007**: La activación no reescribe documentos ni sus condiciones históricas.
- **FR-008**: No aceptar Python/XML/QWeb arbitrario de un usuario de diseño.
- **FR-009**: Importes y textos se escapan y las firmas/marcas respetan licencias y compañía.
- **FR-010**: Un reporte mantiene grano, filtros y monedas aunque cambie su disposición.

### Key Entities

Plantilla por compañía/tipo; versión inmutable activada; bloques y campos permitidos; vista previa; referencia de plantilla usada al emitir.

## Success Criteria

- **SC-001**: Completar la carga ordinaria usando sólo esenciales y configuración válida.
- **SC-002**: Los reintentos no producen un segundo efecto en los escenarios de aceptación.
- **SC-003**: Cada efecto y saldo mostrado conduce a su fuente y corrección.
- **SC-004**: El recorrido de aceptación conserva compañía, moneda, historia y permisos.

## Assumptions

Fecha de hoy propuesta en una carga nueva según zona del usuario; conservar fechas existentes y de origen.
Carga principal: fecha, tercero, documento y conceptos/artículos; datos secundarios progresivos.
Una persona puede combinar roles; conservar ACL/compañías y guardas nativas. Código original AGPL-3.0-only,
documentación CC BY-SA4.0 y licencias de terceros preservadas. Integraciones externas únicamente en
arg_pyme_integraciones, deshabilitadas inicialmente. No hay operaciones reales ni migración automática
implícitas en este diseño. QA funcional/visual y aceptación se realizan después de la entrega técnica.
