# Feature Specification: Obras, capítulos y costos ARG

**Feature Branch**: `codex-notebook/plan-001`
**Created**: 2026-11-05
**Status**: Diseño para implementación incremental; no instalado.
**Input**: Procesos FactuSOL adaptados a Argentina, simplicidad y fuentes nativas.

## User Scenarios & Testing

### User Story 1 - Cargar lo básico (Priority: P2)

Crear obra con cliente, nombre y fecha; agregar capítulos cuando hagan falta.

**Why this priority**: permite una entrada útil sin módulos adicionales innecesarios.
**Independent Test**: registrar un borrador completo con datos esenciales, sin movimientos ni envíos.
**Acceptance Scenarios**:
1. **Given** datos maestros configurados, **When** ingreso fecha/tercero/concepto, **Then** el sistema deduce lo conocido y conserva mis correcciones.
2. **Given** un registro existente, **When** lo reabro, **Then** no cambia su fecha ni se duplica su identidad.

### User Story 2 - Ejecutar el circuito (Priority: P2)

Presupuesto de obra → capítulos → compras/consumos/horas → avance → facturación por capítulos o hitos → cierre.

**Independent Test**: Obra con dos capítulos: consumir material sólo en uno, registrar horas, comparar previsto/real y facturar un hito sin repetir costo ni consumo.
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
- Material comprado para depósito y material consumido en obra son hechos distintos.

## Requirements

### Functional Requirements

- **FR-001**: Crear obra con cliente, nombre y fecha; agregar capítulos cuando hagan falta.
- **FR-002**: Ofrecer el recorrido explícito: Presupuesto de obra → capítulos → compras/consumos/horas → avance → facturación por capítulos o hitos → cierre.
- **FR-003**: Costos reales desde compras, consumos y horas nativos; distinguir comprometido, devengado y pagado. No sumar dos veces compra y consumo del mismo material.
- **FR-004**: Conservar identidad, relaciones de origen y eventos de corrección sin duplicar efectos.
- **FR-005**: Mostrar pendientes por eje y fuente, sin sumar monedas ni hechos incompatibles.
- **FR-006**: Aplicar fecha de hoy propuesta/carga mínima y permisos efectivos con manual/tutoría versionados.
- **FR-007**: Material comprado para depósito y material consumido en obra son hechos distintos.
- **FR-008**: Costo previsto, real, facturado y pagado no se suman como una misma medida.
- **FR-009**: Cambiar la tarifa vigente no reescribe horas ni presupuestos aceptados.
- **FR-010**: Una obra admite un operador con roles combinados.

### Key Entities

Obra y capítulo; presupuesto versionado; parte de material con movimiento; parte de mano de obra con horas/tarifa histórica; vínculo analítico y certificación/hito comercial.

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
