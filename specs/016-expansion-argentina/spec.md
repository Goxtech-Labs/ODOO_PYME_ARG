# Feature Specification: Expansión argentina desde procesos FactuSOL

**Feature Branch**: `codex-notebook/plan-001`
**Created**: 2026-11-05
**Status**: Coordinación del programa de implementación; no es otro addon ni una entrega ya instalada.
**Input**: Incorporar todos los procesos identificados, argentinizados, con carga básica práctica para equipos pequeños.

## User Scenarios & Testing

### User Story 1 - Trabajar con lo básico (Priority: P1)

Como operador necesito hoy propuesto, destinatario, documento y conceptos/artículos, con secundarios fuera del recorrido ordinario.
**Independent Test**: abrir/cargar/reabrir PRE/PED/PPC/FAC/REC/OPA conservando fecha elegida y valores configurados.
**Acceptance Scenarios**:
1. **Given** configuración válida, **When** abro documento nuevo, **Then** hoy está propuesto y puedo corregirlo.
2. **Given** fecha histórica o de origen, **When** reabro/derivo, **Then** se conserva según contrato, sin sustitución silenciosa.
3. **Given** una sola persona habilitada, **When** completa el circuito, **Then** no exige otro departamento ni datos secundarios innecesarios.

### User Story 2 - Administrar a la argentina (Priority: P1)

Como responsable necesito REC con varios medios para cobrar facturas, OPA/lotes/transferencias y cartera de valores trazable.
**Independent Test**: factura120000 con efectivo20000 y cheque100000 diferencia deuda aplicada, caja, cartera y acreditación bancaria.
**Acceptance Scenarios**:
1. **Given** REC con cheque aceptado, **When** aplico a factura, **Then** muestro deuda aplicada sin afirmar acreditación bancaria.
2. **Given** endoso/depósito/descuento/rechazo, **When** registro su hecho, **Then** preservo identidad, exposición y contrapartida sin duplicar dinero.
3. **Given** lote parcialmente ejecutado, **When** consulto, **Then** los pendientes siguen por instrucción y moneda.

### User Story 3 - Agregar operaciones por rubro (Priority: P2)

Como pyme necesito reparaciones, obras, fabricación, comisiones o servicios opcionales sin imponerlos al comercio genérico.
**Independent Test**: instalar sólo la extensión elegida mantiene el núcleo y sus fuentes sin ciclo de dependencia.
**Acceptance Scenarios**:
1. **Given** reparación, **When** recibo equipo del cliente, **Then** no aumenta stock propio.
2. **Given** obra/fabricación, **When** registro consumo, **Then** el efecto nativo ocurre una vez con origen.
3. **Given** servicio/comisión, **When** repito período o liquidación, **Then** no duplica documentos ni importes.

### User Story 4 - Completar herramientas y canales (Priority: P3)

Como usuario necesito variantes, trazabilidad, reposición, riesgo, etiquetas, POS, diseños e integraciones simples.
**Independent Test**: cada fila de cobertura tiene módulo, tareas y límites, conservando libros y permisos nativos.
**Acceptance Scenarios**:
1. **Given** POS existente, **When** enlazo ticket, **Then** no genero un REC/asiento/stock duplicado.
2. **Given** canal deshabilitado, **When** instalo o abro una pantalla, **Then** no envía mensajes ni pedidos externos.
3. **Given** diseño personalizado, **When** imprimo, **Then** mantiene hechos/importes y no ejecuta código arbitrario.

### Edge Cases

Fechas históricas, atributos obligatorios por rubro, roles combinados/restringidos, mezcla de monedas,
rechazos después de endoso, instrumentos propios/terceros, concurrencia, eventos inciertos, devoluciones
parciales, cambios de tarifas/costos, doble contabilización POS y preservación de documentos publicados.

## Requirements

### Functional Requirements

- **FR-001**: Cubrir F01–F22 del plan con dependencia y entrega verificables, sin reducir el objetivo a finanzas.
- **FR-002**: Usar fecha hoy por contexto en nuevas cargas y conservar fechas existentes/origen/correcciones.
- **FR-003**: Priorizar destinatario, documento y conceptos/artículos; completar conocidos y relegar secundarios.
- **FR-004**: REC reúne medios para cobrar facturas; conservar parciales, múltiples facturas y cobros a cuenta.
- **FR-005**: Separar instrumento/tenencia, aplicación a deuda, liquidez y responsabilidad, con eventos y fuente única.
- **FR-006**: Ofrecer OPA/lotes/transferencias argentinos; distinguir pagaré jurídico de orden de pago.
- **FR-007**: Incorporar especializaciones por módulos opcionales con fuentes nativas e identidad ARG.
- **FR-008**: Centralizar todos los proveedores externos en Integraciones ARG, inactivos al instalar.
- **FR-009**: Conservar trazabilidad de parciales/correcciones, idempotencia, permisos y compañía/moneda.
- **FR-010**: Entregar manual, ejemplos, tutorial versionado y estados de código/instalación/QA/aceptación separados.
- **FR-011**: Preservar licencias, soberanía, gratuidad y composición reproducible sin core modificado.
- **FR-012**: Toda adaptación explica proceso de referencia, decisión argentina y fuente de efecto.

### Key Entities

Capacidad F01–F22, módulo/composición, contrato documental, fuente nativa, instrumento/evento, entrega
versionada y evidencia técnica; entidades operativas en las specs independientes 017–024 y existentes.

## Success Criteria

- **SC-001**: Las22 capacidades tienen responsable documental y tareas identificadas, sin funciones omitidas.
- **SC-002**: La carga ordinaria de cada documento se realiza con esenciales/configuración válida.
- **SC-003**: Todos los ejemplos de recepción/transmisión/liquidación explican deuda y dinero por separado.
- **SC-004**: Reintentos, parciales y correcciones preservan un solo efecto y su origen.
- **SC-005**: Ningún canal externo se activa por instalación ni se atribuye QA a sintaxis/HTTP200.

## Assumptions

Interfaz y núcleo existentes son punto de partida, no se reconstruyen desde cero. Se desarrollan los
addons originales, no se copian reglas de otros clientes. No se porta normativa española. Candidatos
nativos se comprueban por versión/licencia antes de implementar; reglas de banco se versionan.
El titular confirmó el REC argentino con medios para cobrar facturas. Pagaré formal queda previsto
como instrumento opcional; uso cotidiano de remesas/pagarés se ofrece como OPA/lotes/transferencias.
