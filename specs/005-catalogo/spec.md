# Feature Specification: Catálogo y precios ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Base20.0.1.0.5 instalada; ampliación1.1 de variantes instalada técnicamente en aislado y demo; QA pendiente.

**Input**: Gestionar productos y servicios genéricos, listas de precios y atributos opcionales mediante fichas y matrices simples.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Crear producto o servicio (Priority: P1)

Como operador necesito identificar qué vendo o compro con los mínimos datos.

**Why this priority**: Entregar crear producto o servicio con el orden común y decisiones mínimas.

**Independent Test**: Crear un producto de ejemplo con nombre, tipo, unidad y precio sin completar atributos de un rubro ajeno.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** crear un producto de ejemplo con nombre, tipo, unidad y precio sin completar atributos de un rubro ajeno.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** exigir lote o depósito sólo cuando la capacidad y el producto lo requieran.

### User Story 2 - Actualizar precios (Priority: P2)

Como responsable necesito editar listas en una matriz sin perder correspondencia producto/lista.

**Why this priority**: Entregar actualizar precios con el orden común y decisiones mínimas.

**Independent Test**: Filtrar productos y editar precios en columnas alineadas, revisando antes de guardar.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** filtrar productos y editar precios en columnas alineadas, revisando antes de guardar.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** conservar cambios pendientes al filtrar y detectar modificaciones concurrentes.

### User Story 3 - Extender sin imponer rubro (Priority: P2)

Como pyme genérica necesito agregar variantes sólo cuando correspondan.

**Why this priority**: Entregar extender sin imponer rubro con el orden común y decisiones mínimas.

**Independent Test**: Agregar un atributo opcional y conservar el mismo catálogo y sus referencias.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** agregar un atributo opcional y conservar el mismo catálogo y sus referencias.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** evitar generar combinaciones innecesarias o reinterpretar un servicio como existencia física.

### Edge Cases

- No modificar stock físico como efecto de editar catálogo o tarifa.
- Conservar reglas nativas de precio y descuentos configurados.
- No guardar automáticamente al aplicar filtros.
- Evitar enviar todas las imágenes o variantes al navegador.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Mantener productos y servicios con códigos textuales y unidades explícitas.
- **FR-002**: Mostrar precio y datos básicos antes de configuración avanzada.
- **FR-003**: Ofrecer productos por fila y listas por columna con filtros combinables.
- **FR-004**: Aplicar reglas nativas de tarifas y explicitar moneda y vigencia.
- **FR-005**: Mantener atributos y categorías genéricos sin talles obligatorios.
- **FR-006**: Separar costo, precio, margen, moneda y unidades en consulta y edición.
- **FR-007**: Consultar variantes en una matriz paginada por atributos opcionales, con dos ejes elegibles y filtros para los restantes; conservar combinaciones y exclusiones nativas sin generar variantes al consultar.
- **FR-008**: Distinguir combinación excluida, variante activa visible y variante no determinada; consultar cantidades nativas según permisos y abrir fichas, precios y preparación de etiquetas de las variantes elegidas.

- **FR-009**: Consultar precio por cliente opcional, variante, cantidad, fecha/hora y lista; proponer condiciones nativas del cliente y permitir elegir otra lista explícitamente sin alterar su maestro ni documentos.
- **FR-010**: Explicar la regla efectiva y la cadena de listas con moneda/unidad, cantidad mínima, vigencia, tipo de cálculo y ajustes nativos; respetar costos restringidos y ausencia de acceso/tasas, sin otro motor ni escrituras de negocio.

### Key Entities

- **Producto**: SKU, nombre, tipo, unidad, categoría, atributos.
- **Tarifa**: moneda, vigencia, reglas por producto y cantidad.
- **Variante**: atributos opcionales y combinaciones válidas.

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

## Incremento F19 · consulta y condiciones

La consulta propone hoy/ahora según presentación local, cliente opcional, producto y cantidad1; datos
conocidos se proponen sin sobrescribir una lista elegida manualmente. La matriz conserva su criterio
de fecha y sus precios pendientes: explicar una celda consulta el precio persistido, no el buffer.
La explicación no aplica precios a documentos, no reescribe presupuestos ni asigna condiciones.
La edición usa formularios nativos autorizados; una regla de lista puede afectar a todos sus usuarios.

F19 de Catálogo1.2 instalado técnicamente en aislado y demo; controles en
[entrega](../../docs/entregas/005-precio-condiciones.md). QA funcional/visual y aceptación pendientes.
