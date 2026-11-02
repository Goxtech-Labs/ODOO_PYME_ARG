# Feature Specification: Producto comunitario para pymes argentinas

**Feature Branch**: `codex-notebook/plan-001`

**Created**: 2026-11-01

**Status**: Núcleo implementado e instalado técnicamente en demo; correcciones de cierre instaladas técnicamente. Publicación, QA funcional/visual y aceptación pendientes.

**Input**: Producto gratuito y comunitario, genérico modular, soberanía de datos, Gestión ARG simplificada,
separación visual y lógica documental inspirada en FactuSOL, capacidad de extensión Odoo,
addons propios desde cero, identidad argentina y branding Goxtech discreto.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Gestionar documentos con carga mínima (Priority: P1)

Como operador de una pyme, necesito encontrar y completar cada documento sin aprender pantallas diferentes.

**Why this priority**: La simplicidad cotidiana define el valor principal del producto.

**Independent Test**: Completar un presupuesto y consultar sus derivados usando únicamente Ventas.

**Acceptance Scenarios**:

1. **Given** un cliente y producto existentes, **When** creo un presupuesto, **Then** selecciono cliente,
producto y cantidad; los valores configurados completan los demás datos ordinarios.
2. **Given** un documento, **When** abro su edición, **Then** encuentro tercero, datos generales,
detalle, totales y acciones en el mismo orden, sin reordenamientos por rubro.
3. **Given** un presupuesto aceptado, **When** genero el pedido, **Then** conservo los datos aprobados,
su origen y la evidencia de la versión aceptada sin volver a escribir sus líneas.
El pedido y el presupuesto son documentos distintos: el presupuesto conserva código PRE y el pedido recibe código PED.
4. **Given** una entrega parcial, **When** consulto el pedido, **Then** distingo entregado y pendiente;
facturar y cobrar conservan estados independientes.
5. **Given** permisos de ventas, **When** busco un presupuesto, **Then** ingreso directamente a su listado;
no necesito navegar por configuración técnica ni por documentos de compras.

### User Story 2 - Activar capacidades según necesidad (Priority: P1)

Como responsable, necesito instalar gestión general y agregar funciones sin adoptar un rubro obligatorio.

**Why this priority**: Permite utilizar una misma base en pymes distintas.

**Independent Test**: Usar Ventas sin Stock y agregar Stock conservando los datos comerciales existentes.

**Acceptance Scenarios**:

1. **Given** una empresa de servicios, **When** activo Ventas, **Then** no necesito completar depósitos
ni números de serie para ofrecer un servicio.
2. **Given** el núcleo instalado, **When** incorporo una extensión por rubro, **Then** se agregan sus
campos y documentos específicos conservando orden, permisos y circuitos comunes.
3. **Given** un usuario habilitado, **When** necesita una operación avanzada, **Then** puede acceder
a las funciones avanzadas disponibles según sus permisos.

### User Story 3 - Conservar el control de los datos (Priority: P1)

Como dueño de la empresa, necesito operar en infraestructura elegida y cambiar de proveedor.

**Why this priority**: La soberanía debe mantenerse durante toda la vida de la instalación.

**Independent Test**: Recuperar una empresa de ejemplo en otra instalación y consultar documentos y adjuntos.

**Acceptance Scenarios**:

1. **Given** una instalación local configurada, **When** no activo integraciones externas,
**Then** puedo gestionar documentos internos sin cuenta ni servicio obligatorio de Goxtech.
2. **Given** un respaldo completo, **When** sigo la guía de restauración,
**Then** recupero documentos, relaciones, archivos adjuntos y permisos en otro equipo compatible.
3. **Given** una integración desactivada, **When** abro su configuración,
**Then** no se envían documentos ni se activan sincronizaciones.
4. **Given** un usuario sin autorización, **When** intenta consultar datos de otra empresa,
**Then** se rechaza el acceso, incluso mediante exportación o enlace directo.

### User Story 4 - Reconocer una interfaz argentina consistente (Priority: P1)

Como usuario, necesito reconocer acciones, documentos y estados sin interpretar estilos diferentes.

**Why this priority**: La consistencia reduce errores y entrenamiento.

**Independent Test**: Identificar acciones y completar una matriz por teclado en dos áreas diferentes.

**Acceptance Scenarios**:

1. **Given** cualquier documento, **When** encuentro Guardar o Descartar,
**Then** conservo texto, icono, ubicación y significado cromático consistentes.
2. **Given** una matriz de precios, **When** filtro o desplazo columnas,
**Then** encabezados y valores permanecen alineados; los cambios pendientes se conservan.
3. **Given** una compañía con marca propia, **When** imprimo su documento,
**Then** su identidad comercial prevalece y la firma Goxtech resulta secundaria.
4. **Given** un campo inválido, **When** intento continuar,
**Then** identifico el campo y la solución mediante texto, sin depender solamente del color.

### User Story 5 - Descubrir, aprender y contribuir (Priority: P2)

Como visitante, necesito comprender el proyecto desde su repositorio y encontrar información pública.

**Why this priority**: La comunidad necesita un punto de entrada confiable.

**Independent Test**: Encontrar alcance, estado, documentación y forma de contribuir desde la portada.

**Acceptance Scenarios**:

1. **Given** la portada del repositorio, **When** la consulto,
**Then** identifico propósito, gratuidad, soberanía, módulos, estado real y enlaces de aprendizaje.
2. **Given** un módulo publicado, **When** abro su documentación,
**Then** encuentro requisitos, instalación, uso, ejemplos, límites y versión compatible.
3. **Given** una propuesta comunitaria, **When** sigo la guía de contribución,
**Then** puedo describir necesidad, reproducción y criterios de aceptación sin compartir datos privados.
4. **Given** la portada, el manifiesto o una presentación del proyecto,
**When** consulto quién lo impulsa, **Then** identifico a Gonzalo Sarubilo, su experiencia declarada
y su aporte; encuentro los servicios profesionales como actividad secundaria y opcional.

### User Story 6 - Incorporar rubros e integraciones después del núcleo (Priority: P3)

Como pyme argentina, necesito agregar capacidades fiscales y sectoriales según mi actividad.

**Why this priority**: Amplía utilidad conservando un núcleo sencillo.

**Independent Test**: Agregar un conector de prueba o una extensión sectorial sin activar conexiones reales.

**Delivery boundary**: Reservar esta historia para después de los cinco circuitos generales.

**Acceptance Scenarios**:

1. **Given** una factura interna, **When** consulto su estado,
**Then** distingo registro interno, autorización fiscal, entrega y cobro.
2. **Given** un conector instalado, **When** lo configuro,
**Then** encuentro su estado y ajustes en Integraciones ARG sin duplicar credenciales.
3. **Given** dos compañías, **When** configuro un servicio,
**Then** su identidad y ambiente no se aplican silenciosamente a la otra.
4. **Given** una pyme sin un rubro específico, **When** utiliza el núcleo,
**Then** no encuentra campos obligatorios propios de una actividad ajena.

### User Story 7 - Identificar documentos e interpretar informes (Priority: P1)

Como responsable, necesito reconocer documentos por códigos cortos y comprender qué mide cada informe.

**Why this priority**: Evita confundir operaciones y duplicar resultados entre circuitos.

**Independent Test**: Seguir pedido, entrega, factura y cobro; comprobar sus referencias y medidas separadas.

**Acceptance Scenarios**:

1. **Given** dos presupuestos guardados, **When** consulto sus identificadores,
**Then** comparten prefijo corto y tienen números correlativos diferentes.
2. **Given** una factura, **When** consulto su identidad,
**Then** distingo código interno e identificación fiscal sin confundir sus estados.
3. **Given** pedido, entrega, factura y cobro relacionados, **When** consulto ventas facturadas,
**Then** computo solamente facturación, descontando notas de crédito.
4. **Given** monedas diferentes, **When** solicito un total,
**Then** separo monedas o identifico la conversión utilizada.
5. **Given** un informe, **When** abro su definición,
**Then** identifico hecho, granularidad, fecha, dimensiones, filtros y tratamiento de anulaciones.

### User Story 8 - Aprender mediante YouTube y reconocer ARG (Priority: P2)

Como dueño u operador de una pyme, necesito descubrir ARG mediante demostraciones y aprender cada circuito.

**Why this priority**: Amplía alcance y facilita adopción sin depender de asistencia contratada.

**Independent Test**: Seguir una demostración de un circuito y encontrar su guía de la misma versión.

**Acceptance Scenarios**:

1. **Given** un módulo del proyecto, **When** consulto menú, manual o presentación,
**Then** reconozco ARG como identidad principal y nomenclatura constante.
2. **Given** un tutorial publicado, **When** consulto su descripción,
**Then** encuentro versión mostrada y enlaces al proyecto y guía correspondientes.
3. **Given** una demostración, **When** sigo sus pasos,
**Then** dispongo de ejemplos identificados sin datos de clientes reales.
4. **Given** una mejora inspirada en otro proyecto, **When** la incorporamos,
**Then** mantenemos identidad ARG y respetamos atribuciones y compatibilidad.
5. **Given** un módulo instalado, **When** abro Ayuda → Tutoriales,
**Then** encuentro sus videos y guía con versión compatible y estado de actualización.
6. **Given** un cambio de pantalla o circuito, **When** revisamos la entrega,
**Then** identificamos tutoriales afectados y los marcamos por revisar hasta confirmar o actualizar su contenido.
7. **Given** un enlace actualizado en el catálogo de ayuda, **When** vuelvo a consultar el módulo,
**Then** encuentro el enlace actualizado sin reinstalarlo; si falta video, encuentro su guía y estado pendiente.

### User Story 9 - Consultar soporte administrado por el responsable de ARG (Priority: P2)

Como operador, necesito acceder al soporte general desde Odoo mediante canales administrados por el responsable.

**Why this priority**: Centraliza asistencia bajo administración del responsable y conserva contexto útil.

**Independent Test**: Configurar soporte general y acceder desde el menú de usuario conservando su destino entre módulos.

**Acceptance Scenarios**:

1. **Given** un centro de soporte configurado por el administrador,
**When** utilizo cualquiera de las entradas de soporte inventariadas,
**Then** accedo al centro ARG administrado por el responsable, con sus canales habilitados.
2. **Given** un cambio de correo, WhatsApp o sistema de tickets,
**When** el administrador actualiza el destino central,
**Then** todos los accesos utilizan ese destino sin modificar cada módulo.
3. **Given** una consulta desde un módulo, **When** preparo el contacto,
**Then** puedo revisar módulo, versión y descripción antes de enviar información.
4. **Given** canales sin configurar, **When** solicito ayuda,
**Then** encuentro manuales y tutoriales disponibles sin un destino de contacto ficticio.
5. **Given** una pantalla que presenta al bot nativo, **When** consulto su identidad vigente,
**Then** encuentro GOXTECHBOT, con avatar y textos coherentes, conservando la identidad ARG del producto.

### User Story 10 - Personalizar y aportar conocimiento en comunidad (Priority: P2)

Como responsable o colaborador, necesito comprender la gestión y adaptar módulos con personas o agentes de IA.

**Why this priority**: Comparte experiencia, permite aprender de nuevos negocios y conserva autonomía tecnológica.

**Independent Test**: Localizar especificación, contratos y ejemplos de un módulo y preparar una propuesta de extensión.

**Acceptance Scenarios**:

1. **Given** un módulo publicado, **When** busco cómo personalizarlo,
**Then** encuentro su spec, contratos, dependencias y ejemplos sin pago obligatorio por acceder al conocimiento.
2. **Given** una necesidad nueva, **When** preparo una propuesta con una persona o agente de IA,
**Then** dispongo de instrucciones y contexto del proyecto para identificar la extensión adecuada.
3. **Given** una instalación propia, **When** no utilizo herramientas de IA,
**Then** la gestión básica mantiene su funcionamiento y mis datos permanecen bajo mi administración.
4. **Given** una experiencia aportada por un usuario, **When** la evaluamos,
**Then** podemos convertirla en documentación, mejora o módulo reutilizable con alcance definido.

### Edge Cases

- Conservar importes pactados cuando cambien tarifas o cotizaciones después del documento.
- Separar descuentos, devoluciones, anticipos y cobros parciales de anulaciones.
- Advertir ediciones concurrentes y conservar cambios pendientes ante filtros o navegación.
- Mantener presupuesto original identificable después de generar derivados o revisiones.
- Evitar duplicar entregas, cobros o autorizaciones ante reintentos.
- Ocultar y proteger funciones no autorizadas; separar seguridad de presentación visual.
- Evitar sumar importes de monedas distintas sin conversión explícita.
- Identificar demo, pruebas fiscales y producción sin mezclar sus documentos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Ofrecer gestión gratuita y comunitaria sin límites comerciales propios de usuarios o documentos.
- **FR-002**: Permitir instalación propia, exportación y restauración completa independiente del proveedor.
- **FR-003**: Separar núcleo, presentación, gestión común, rubros e integraciones instalables.
- **FR-004**: Organizar áreas visibles de Ventas, Compras, Stock, Administración, Informes y Configuración.
- **FR-005**: Separar listados, estados y acciones de cada tipo documental.
- **FR-006**: Mantener tercero → datos generales → detalle → totales → acciones en todos los documentos.
- **FR-007**: Completar valores conocidos y pedir solamente datos necesarios para la operación actual.
- **FR-008**: Conservar carga rápida, búsqueda y navegación por teclado en formularios y matrices.
- **FR-009**: Vincular documentos de origen y destino conservando pendientes y evidencia aprobada.
- **FR-010**: Separar efectos comerciales, físicos, contables, financieros y fiscales.
- **FR-011**: Mantener acceso avanzado sujeto a los permisos efectivos del usuario.
- **FR-012**: Aplicar identidad celeste y blanca con acento solar y firma Goxtech discreta.
- **FR-013**: Unificar botones, iconos, estados, filtros y matrices sin depender solamente del color.
- **FR-014**: Conservar marca de la pyme como identidad principal en sus documentos comerciales.
- **FR-015**: Centralizar ajustes de conectores y explicar activación, estado y datos compartidos.
- **FR-016**: Aislar compañías, permisos y ambientes tanto en pantalla como en accesos alternativos.
- **FR-017**: Publicar portada clara, documentación por módulo y procedimiento comunitario de contribución.
- **FR-018**: Diferenciar funciones planificadas, desarrolladas, instaladas y revisadas.
- **FR-019**: Permitir extensiones sectoriales sin alterar el orden común ni imponer reglas ajenas.
- **FR-020**: Documentar gratuidad del software y costos opcionales de servicios externos por separado.
- **FR-021**: Identificar documentos mediante prefijo corto y secuencia independiente por compañía y tipo.
- **FR-022**: Conservar numeración fiscal separada de la identificación interna.
- **FR-023**: Definir documentos mediante hechos, dimensiones, transiciones y efectos permitidos.
- **FR-024**: Entregar primero cinco circuitos: Ventas, Compras, Stock, Administración e Informes.
- **FR-025**: Definir informes por hecho y granularidad, evitando sumar etapas del mismo circuito.
- **FR-026**: Incorporar conectores y extensiones sectoriales solamente en etapas posteriores.
- **FR-027**: Mantener áreas superiores, acciones contextuales, listados con filtros y fichas con secciones estables.
- **FR-028**: Agrupar servicios externos en un único módulo Integraciones ARG con habilitación independiente por servicio.
- **FR-029**: Usar ARG como identidad principal y nomenclatura del producto, sin renombrar otros proyectos.
- **FR-030**: Preparar aprendizaje y difusión mediante YouTube, enlazando tutoriales, ejemplos y guías versionadas.
- **FR-031**: Ofrecer tutoriales YouTube y manuales vinculados desde cada módulo, con versión y estado identificables.
- **FR-032**: Mantener un catálogo editable de ayuda y revisar tutoriales afectados en cada cambio de módulo.
- **FR-033**: Dirigir todas las entradas de soporte inventariadas al centro ARG administrado por el responsable.
- **FR-034**: Configurar centralmente soporte por correo, WhatsApp o tickets, sin modificar cada módulo ni enviar información automáticamente.
- **FR-035**: Presentar la identidad visible vigente de OdooBot como GOXTECHBOT mediante branding suave, preservando identificadores y relaciones técnicas.
- **FR-036**: Compartir documentación, tutoriales y ejemplos técnicos y de gestión sin pago obligatorio por acceder al conocimiento del proyecto.
- **FR-037**: Permitir personalización por personas o agentes de IA sin imponer herramientas, modelos o suscripciones de IA para utilizar la gestión básica.
- **FR-038**: Documentar especificaciones, contratos, dependencias y ejemplos por módulo para facilitar extensiones y aportes comunitarios.
- **FR-039**: Visibilizar a Gonzalo Sarubilo y su experiencia declarada en portada, manifiesto y presentaciones, manteniendo los servicios profesionales secundarios y opcionales respecto del propósito comunitario.
- **FR-040**: Mantener Presupuesto ARG como documento propio y generar un Pedido de cliente independiente desde el presupuesto confirmado, conservando códigos, vínculos e historia de ambos.
- **FR-041**: Mostrar estado propio y ejes independientes de confirmación/aceptación, entrega/recepción, facturación y cobro/pago/aplicación; admitir pendiente, parcial y completo donde aplique con cantidades/importes, documentos fuente y distinción de faltante cerrado.

### Key Entities

- **Empresa**: identidad comercial y fiscal, moneda, configuración y preferencias.
- **Usuario y rol**: permisos, compañía y acceso simplificado o avanzado.
- **Tercero**: cliente o proveedor, contactos y valores comerciales predeterminados.
- **Producto o servicio**: identificación, precio, impuestos, unidad y necesidades de stock.
- **Documento y línea**: tipo, identidad, estado, tercero, moneda, detalle y totales históricos.
- **Relación documental**: origen, destino, versión, cantidades e importes aplicados y pendientes.
- **Movimiento**: efecto físico, financiero, contable o fiscal asociado al documento correspondiente.
- **Módulo y extensión**: capacidades, dependencias, compatibilidad, documentación y estado.
- **Conector**: servicio, compañía, ambiente, configuración efectiva y estado comprobado.
- **Respaldo**: alcance recuperable, fecha, versión y procedimiento de recuperación.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Completar un presupuesto ordinario con cliente, producto y cantidad como únicas decisiones
obligatorias, cuando todos los demás valores ya estén configurados.
- **SC-002**: Mantener el orden común en el 100% de los tipos documentales entregados.
- **SC-003**: Crear un derivado sin reescribir datos de origen y mostrar su vínculo en ambos sentidos.
- **SC-004**: Recuperar el 100% de documentos y adjuntos del lote de demostración en otra instalación.
- **SC-005**: Completar los recorridos documentales comunes mediante teclado sin bloquear campos obligatorios.
- **SC-006**: Proveer guía funcional, técnica, ejemplos y versión compatible para el 100% de módulos publicados.
- **SC-007**: Distinguir estado comercial, entrega, facturación y cobro en cada recorrido de demostración aplicable.
- **SC-008**: Encontrar propósito, estado, documentación y contribución desde la portada mediante enlaces directos.
- **SC-009**: Obtener identificadores internos únicos bajo concurrencia y conservarlos tras anulación.
- **SC-010**: Conciliar el 100% de medidas del lote de ejemplo con sus documentos fuente.
- **SC-011**: Asociar cada tutorial publicado a una versión, un recorrido reproducible y su guía pública correspondiente.
- **SC-012**: Ofrecer ayuda versionada en el 100% de módulos publicados, indicando explícitamente tutoriales pendientes o por revisar.
- **SC-013**: Resolver el 100% de accesos de soporte inventariados hacia los canales centrales configurados por el responsable.
- **SC-014**: Mostrar GOXTECHBOT en el 100% de superficies vigentes del bot incluidas en el inventario de la composición instalada.
- **SC-015**: Localizar especificación, contratos y ejemplos del 100% de módulos publicados desde su documentación de extensión.

## Assumptions

- Adoptar pymes genéricas como público y rubros opcionales como ampliación posterior.
- Usar infraestructura propia elegida por cada instalación; no incluir alojamiento gratuito garantizado.
- Tomar referencias públicas de FactuSOL como orientación, sin copiar su código, identidad ni assets.
- Mantener datos fiscales completos antes de emitir; carga mínima no elimina datos legalmente necesarios.
- Conservar la gestión interna disponible ante fallos externos; emisión fiscal requiere su servicio correspondiente.
- El encargo posterior amplió la planificación a desarrollar, implementar y desplegar en la demo autorizada, con datos ficticios. Conservar QA funcional/visual como fase posterior y no activar integraciones reales.
- Resolver instalación y publicación web en tareas propias; una portada documental no acredita un sitio desplegado.
- Entregar cinco circuitos antes de conectores y rubros. Identificar facturas internas como tales
hasta incorporar la emisión fiscal correspondiente.
- Implementar proveedores mediante adaptadores internos de Integraciones ARG; agregar módulos especializados
o personalizados por separado según necesidad.
- Mantener canal/URL de YouTube por definir antes de publicar videos; no inventar un canal existente.
- Tomar patrones y soluciones Goxtech como referencia, preservando identidad ARG y revisión de licencias.
- Mantener soporte como acceso general y GOXTECHBOT como excepción explícita de branding suave.
- Permitir elegir homelab, servidor propio, VPS u otra infraestructura compatible, con recuperación portable.
- Priorizar compartir experiencia y aprender de la comunidad como propósito del proyecto.
- Usar la experiencia profesional aportada por Gonzalo Sarubilo sin inferir titulaciones, certificaciones ni antecedentes adicionales.

