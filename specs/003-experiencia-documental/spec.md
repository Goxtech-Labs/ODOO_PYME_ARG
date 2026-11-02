# Feature Specification: Experiencia y presentación ARG

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Desarrollado y desplegado en demo; revisión visual parcial realizada, aceptación y escenarios restantes pendientes.

**Input**: Presentar cinco circuitos, carga mínima, orden constante, componentes comunes, identidad ARG y GOXTECHBOT.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Navegar por circuitos (Priority: P1)

Como usuario no especialista necesito encontrar documentos sin recorrer configuración técnica.

**Why this priority**: Entregar navegar por circuitos con el orden común y decisiones mínimas.

**Independent Test**: Abrir Presupuestos, Pedidos, Entradas y Recibos desde sus áreas y conservar filtros al volver.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** abrir Presupuestos, Pedidos, Entradas y Recibos desde sus áreas y conservar filtros al volver.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** mostrar únicamente acciones permitidas y conservar acceso avanzado según el rol.

### User Story 2 - Editar con un patrón común (Priority: P2)

Como operador necesito el mismo orden y botones en documentos y matrices.

**Why this priority**: Entregar editar con un patrón común con el orden común y decisiones mínimas.

**Independent Test**: Recorrer tercero, generales, detalle, totales y acciones mediante teclado.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** recorrer tercero, generales, detalle, totales y acciones mediante teclado.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** conservar cambios pendientes al filtrar y advertir antes de descartarlos.

### User Story 3 - Reconocer ARG y su ayuda (Priority: P2)

Como usuario necesito identidad argentina y ayudas consistentes sin publicidad operativa.

**Why this priority**: Entregar reconocer arg y su ayuda con el orden común y decisiones mínimas.

**Independent Test**: Encontrar tutoriales por módulo, soporte general y GOXTECHBOT en superficies inventariadas.

**Acceptance Scenarios**:

1. **Given** una compañía de ejemplo configurada y un usuario autorizado, **When** realiza el recorrido, **Then** encontrar tutoriales por módulo, soporte general y GOXTECHBOT en superficies inventariadas.
2. **Given** una excepción o datos incompletos, **When** intenta continuar, **Then** conservar identidad de la pyme en sus documentos y atribuciones técnicas correspondientes.

### Edge Cases

- Guardar no confirma entregas, contabilización, cobros ni emisión fiscal.
- Conservar callbacks y validaciones nativas de formularios.
- No ocultar errores mediante sudo o eliminación de grupos.
- Mantener texto e icono además del color; proponer contraste 4,5:1 para texto normal.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Organizar áreas y acciones contextuales mediante el árbol de menús efectivo.
- **FR-002**: Conservar listado, filtros y contexto al abrir o cerrar una ficha.
- **FR-003**: Compartir guardado, descarte, retorno, foco y semántica entre formularios.
- **FR-004**: Mantener matrices alineadas y paginadas con filtros combinables.
- **FR-005**: Aplicar celeste/blanco, branding discreto, claro/oscuro y controles accesibles.
- **FR-006**: Presentar GOXTECHBOT preservando identidad técnica y comportamiento del bot nativo.
- **FR-007**: Ofrecer una cinta por circuito con pestañas estables, comandos con texto e iconos Lucide locales y grupos de documentos/datos; mostrar sólo menús permitidos y conservar Configuración según el rol.
- **FR-008**: Distinguir campos editables, desplegables y valores de lectura mediante bordes, superficie, flecha nativa y foco visibles, en ambos temas, sin cambiar validaciones ni guardar implícitamente.
- **FR-009**: Usar recursos argentinos de industria y gestión en Inicio/acceso, con branding Goxtech secundario, licencias y procedencia conservadas; adaptar cinta y portada al ancho disponible.

### Key Entities

- **Preferencias visuales**: tema, densidad y preferencias.
- **Contexto de navegación**: área, acción, filtros, retorno.
- **Bot**: nombre/avatar/textos vigentes e inventario.

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

## Incremento visual solicitado · 2026-11-02

El titular pidió iconos Lucide, pestañas/cinta inspiradas en Office, campos delimitados y
reconocimiento claro de escritura frente a selección, con bandera, industria y gestión argentinas.
Se amplía esta spec existente; no cambia el orden documental ni se agregan campos obligatorios.

### Escenarios del incremento

1. Con permisos de Ventas, seleccionar la pestaña Compras sólo cambia los comandos disponibles;
   abrir un comando usa la navegación nativa y sus guardas. Las acciones sin permiso no aparecen.
2. Con permiso de configuración, acceder a Tipos documentales, Terceros y Listas avanzadas desde
   su pestaña. Ayuda y soporte siguen disponibles; Odoo avanzado conserva su entrada.
3. En un PRE borrador, distinguir cliente/autocompletar, fecha, texto y cantidades; abrir el
   desplegable real, editar y descartar sin confirmar ni contabilizar. Los valores protegidos
   siguen de lectura; teclado, foco y advertencias conservan la lógica nativa.
4. En tema claro/oscuro y pantalla estrecha, reconocer textos, pestañas e iconos, desplazar o
   contraer la cinta y acceder a las tarjetas. Las imágenes no sustituyen etiquetas accesibles.
5. El acceso conserva formulario, CSRF, autenticación y ayudas nativas, con identidad ARG.

La aceptación del titular se registra separada de la comprobación técnica/visual del agente.
