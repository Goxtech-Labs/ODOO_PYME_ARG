# Tasks: ODOO PYMES ARG

**Input**: spec.md, plan.md, research.md, data-model.md y contracts/.

**Estado**: núcleo genérico implementado e instalado técnicamente; documentación y licencias preparadas. Los checks de implementación acreditan código/instalación, no QA ni aceptación. Evidencia consolidada: docs/entregas/CONTROLES-TECNICOS.md.
**Tests**: Preparar criterios ahora; conservar QA funcional/visual como fase posterior.
**Organization**: Agrupar por historias; respetar desarrollo módulo por módulo.

## Phase 1: Setup

**Goal / Independent Test**: Resolver licencia, composición y runtime antes de implementar.

- [x] T001 Resolver licencia de addons originales y registrar decisión en docs/tecnica/DECISIONES-ODOO20.md; agregar LICENSE después de esa elección. (FR-001 FR-020)
- [x] T002 Fijar revisión Community y dependencias compatibles en composition/versions.lock.json. (FR-003)
- [x] T003 Preparar instalación aislada y configuración sin secretos en docs/tecnica/ENTORNO-DEMO.md. (FR-002 FR-016)

## Phase 2: Foundational

**Goal / Independent Test**: Definir Base ARG antes de desarrollar módulos consumidores.

- [x] T004 Crear spec independiente de Base ARG en specs/002-base-arg/spec.md y generar su plan y tareas. (FR-003 FR-021)
- [x] T005 Implementar compañías, preferencias y registro documental común en addons/arg_pyme_base/models/. (FR-003 FR-021 FR-023)
- [x] T006 Definir roles y reglas por compañía en addons/arg_pyme_base/security/ir.access.csv. (FR-011 FR-016)

- [x] T007 Implementar tipo/secuencia en addons/arg_pyme_base/models/document_type.py: "Prefijo de 2 a 4 letras ASCII; contador mínimo de seis dígitos"; conservar unicidad de (company_id, tipo_documental, serie_interna, numero_interno). (FR-021 FR-022 SC-009)
- [x] T008 Documentar concurrencia, primer guardado, anulaciones y continuidad entre ejercicios en docs/tecnica/DICCIONARIO-DOCUMENTAL.md. (FR-021 SC-009)

## Phase 3: User Story 2 Modularidad (P1)

**Goal / Independent Test**: Usar servicios sin Stock y agregar capacidades conservando datos.

- [x] T009 [US2] Declarar dependencias opcionales y límites de cada addon en docs/CATALOGO-MODULOS.md. (FR-003 FR-019)
- [x] T010 [US2] Implementar navegación por capacidades instaladas y acceso avanzado según permisos en addons/arg_pyme_base/views/menu_views.xml. (FR-004 FR-011)
- [x] T011 [US2] Definir puentes independientes para ventas-stock y compras-stock en docs/tecnica/DECISIONES-ODOO20.md. (FR-003 FR-009)
- [x] T012 [US2] Preparar perfil de demostración de servicios sin depósitos en docs/ejemplos/servicios.md. (FR-007 FR-019)

## Phase 4: User Story 4 Identidad y experiencia (P1)

**Goal / Independent Test**: Reconocer botones, campos y matrices en dos áreas mediante el mismo patrón.

- [x] T013 [US4] Crear spec de experiencia común en specs/003-experiencia-documental/spec.md, incluyendo áreas, cinta, listado, filtros y ficha. (FR-006 FR-008 FR-012 FR-013 FR-027)
- [x] T014 [US4] Implementar tokens celeste/blanco, claro/oscuro y foco en addons/arg_pyme_ui/static/src/scss/tokens.scss. (FR-012 FR-013)
- [x] T015 [US4] Implementar acciones Guardar, Guardar y nuevo, Guardar y cerrar, Descartar y Volver preservando validaciones nativas en addons/arg_pyme_ui/static/src/components/document_actions/. (FR-006 FR-013)
- [x] T016 [US4] Implementar matriz común con teclado, filtros, alineación y conservación de cambios en addons/arg_pyme_ui/static/src/components/document_matrix/. (FR-008 FR-013)
- [x] T017 [US4] Documentar marca principal de la pyme y firma Goxtech secundaria en docs/usuario/personalizacion-visual.md. (FR-014)

## Phase 5: User Story 1 Cinco circuitos documentales (P1)

**Goal / Independent Test**: Completar documentos con datos conocidos, conservar origen y mostrar pendientes separados.

- [x] T018 [US1] Especificar terceros y datos mínimos en specs/004-terceros/spec.md; implementar ficha con roles combinables en addons/arg_pyme_terceros/views/res_partner_views.xml. (FR-005 FR-007)
- [x] T019 [US1] Especificar catálogo en specs/005-catalogo/spec.md; conservar "SKU textual; conservar ceros iniciales; unidad y tipo explícitos" en addons/arg_pyme_catalogo/models/product.py. (FR-007 FR-008)
- [x] T020 [US1] Especificar Ventas en specs/006-ventas/spec.md, resolviendo presupuesto original, versiones, pedido, parciales, facturas y devoluciones antes del código. (FR-005 FR-009 FR-010 FR-023)
- [x] T021 [US1] Implementar documentos comerciales, valores predeterminados y trazabilidad en addons/arg_pyme_ventas/models/ y addons/arg_pyme_ventas/views/. (FR-005 FR-006 FR-007 FR-009)
- [x] T022 [US1] Especificar Compras en specs/007-compras/spec.md y desarrollar pedidos, entradas y facturas recibidas mediante addons/arg_pyme_compras/. (FR-005 FR-009 FR-010 FR-024)
- [x] T023 [US1] Especificar Stock en specs/008-stock/spec.md y desarrollar movimientos, inventario y ajustes en addons/arg_pyme_stock/; aplicar "Cambiar existencias sólo por movimientos validados". (FR-010 FR-023 FR-024)
- [x] T024 [US1] Especificar Administración en specs/009-administracion/spec.md y desarrollar recibos, pagos, caja e imputaciones en addons/arg_pyme_administracion/. (FR-005 FR-009 FR-010 FR-024)
- [x] T025 [US1] Implementar puentes sobre registros nativos únicos en addons/arg_pyme_ventas_stock/ y addons/arg_pyme_compras_stock/, después de sus módulos consumidores. (FR-009 FR-010)
- [x] T026 [US1] Implementar PDFs y acciones documentales con marca de compañía en addons/arg_pyme_documentos/report/; separar factura interna de identificación fiscal. (FR-014 FR-022)

## Phase 6: User Story 7 Códigos y hechos (P1)

**Goal / Independent Test**: Conciliar códigos e indicadores con sus documentos sin duplicar etapas.

- [x] T027 [US7] Especificar Informes en specs/010-informes/spec.md, con hecho, granularidad, dimensiones, fecha, moneda, signo y filtros por indicador. (FR-023 FR-025 SC-010)
- [x] T028 [US7] Implementar consultas y navegación al origen en addons/arg_pyme_informes/, con puentes solamente a circuitos instalados. (FR-024 FR-025)
- [x] T029 [US7] Preparar lote conciliable y resultados esperados sin datos reales en docs/ejemplos/hechos-dimensiones.md. (FR-025 SC-010)

## Phase 7: User Story 3 Soberanía (P1)

**Goal / Independent Test**: Recuperar documentos y adjuntos de ejemplo en otra instalación.

- [x] T030 [US3] Documentar respaldo consistente de base, filestore, configuración y versiones en docs/tecnica/OPERACION-Y-RECUPERACION.md. (FR-002 SC-004)
- [x] T031 [US3] Documentar exportación abierta con relaciones, monedas y adjuntos en docs/tecnica/exportacion.md. (FR-002)
- [x] T032 [US3] Documentar instalación propia sin cuenta Goxtech obligatoria y gestión local sin conectores en docs/tecnica/OPERACION-Y-RECUPERACION.md. (FR-001 FR-002 FR-020)
- [x] T033 [US3] Documentar permisos por compañía y política de datos compartidos en docs/tecnica/PERMISOS-Y-DATOS-MINIMOS.md. (FR-015 FR-016)

## Phase 8: User Story 5 Comunidad y portada (P2)

**Goal / Independent Test**: Encontrar propósito, estado, manuales y participación desde README.

- [x] T034 [US5] Preparar publicación de portada y assets originales revisando enlaces y estado real en README.md y docs/assets/banner.svg. (FR-012 FR-017 FR-018)
- [x] T035 [US5] Redactar participación, conducta y reporte privado de vulnerabilidades en CONTRIBUTING.md, CODE_OF_CONDUCT.md y SECURITY.md. (FR-017)
- [x] T036 [US5] Definir web documental reutilizando portada e identidad en specs/011-web-comunidad/spec.md, sin activar hosting automáticamente. (FR-017)
- [x] T037 [US5] Crear manuales funcionales y técnicos por módulo y matriz de estados en docs/usuario/, docs/tecnica/ y docs/ESTADO-MODULOS.md. (FR-017 FR-018 SC-006)

- [x] T038 [US5] Aplicar autoría visible de Gonzalo Sarubilo y su experiencia declarada en README.md, docs/GONZALO-SARUBILO.md, docs/MANIFIESTO.md y docs/ALCANCE-YOUTUBE.md; mantener consultoría y servicios opcionales en un espacio secundario. (FR-039)

## Phase 9: User Story 8 Identidad ARG y YouTube (P2)

**Goal / Independent Test**: Reconocer identidad ARG y seguir un tutorial hasta su guía y ejemplos de la misma versión.

- [x] T039 [US8] Aplicar nombres visibles ARG y namespace arg_pyme_* en docs/CATALOGO-MODULOS.md y la composición de addons nuevos; limitar cambios a este proyecto. (FR-029)
- [x] T040 [US8] Definir canal, audiencia, serie y recorridos de demostración en docs/comunidad/youtube/PLAN-EDITORIAL.md, siguiendo docs/ALCANCE-YOUTUBE.md. (FR-030)
- [x] T041 [US8] Preparar plantilla de tutorial con versión, guion, ejemplos y enlaces en docs/comunidad/youtube/PLANTILLA-TUTORIAL.md. (FR-030 SC-011)
- [x] T042 [US8] Preparar primer guion y miniatura original ARG, marcando estado real y datos de ejemplo, en docs/comunidad/youtube/001-presentacion.md y docs/assets/youtube/001-portada.svg; reservar publicación para su encargo específico. (FR-017 FR-029 FR-030 SC-011)

- [x] T043 [US8] Implementar catálogo editable de tutoriales y guías por módulo, tarea y versión en addons/arg_pyme_base/models/help_resource.py y acceso contextual en addons/arg_pyme_ui/views/help_tutorials.xml; permitir actualizar URLs sin reinstalar. (FR-031 FR-032 SC-012)
- [x] T044 [US8] Documentar revisión de tutoriales afectados, versiones compatibles, sustituciones y disponibilidad en docs/comunidad/youtube/MANTENIMIENTO.md y plantilla de entrega en docs/entregas/PLANTILLA-RELEASE.md. (FR-032 SC-011 SC-012)

## Phase 10: User Story 9 Soporte general y GOXTECHBOT (P2)

**Goal / Independent Test**: Configurar soporte general una vez, comprobar sus accesos inventariados y reconocer GOXTECHBOT.

- [x] T045 [US9] Inventariar entradas de asistencia y superficies vigentes del bot nativo en docs/tecnica/INVENTARIO-AYUDA-SOPORTE-BOT.md para la composición instalada. (FR-033 FR-035 SC-013 SC-014)
- [x] T046 [US9] Implementar configuración central de canales administrados por el responsable en addons/arg_pyme_base/models/support_config.py, con correo, WhatsApp y URL de tickets habilitables y sin envíos automáticos. (FR-034)
- [x] T047 [US9] Implementar acceso general Soporte ARG y redirección de entradas inventariadas al destino central en addons/arg_pyme_ui/views/help_support.xml y addons/arg_pyme_ui/static/src/components/support/; conservar ayuda interna si faltan canales. (FR-033 FR-034 SC-013)
- [x] T048 [US9] Aplicar GOXTECHBOT a nombre mostrado, avatar y textos vigentes del bot inventariado en addons/arg_pyme_ui/data/bot_identity.xml y addons/arg_pyme_ui/static/img/goxtechbot.svg; preservar identificadores y relaciones nativas. (FR-035 SC-014)

## Phase 11: User Story 10 Conocimiento y personalización (P2)

**Goal / Independent Test**: Encontrar conocimiento abierto de un módulo y preparar una propuesta de extensión con personas o agentes.

- [x] T049 [US10] Documentar acceso abierto a guías, tutoriales y ejemplos, recepción de experiencias y devolución de mejoras a la comunidad en docs/comunidad/CONOCIMIENTO-COMPARTIDO.md. (FR-036 FR-038)
- [x] T050 [US10] Preparar guía de personalización para personas y agentes de IA en docs/tecnica/PERSONALIZACION.md y mantener AGENTS.md enlazado a specs, contratos y ejemplos por módulo; conservar libertad de herramientas y funcionamiento sin IA obligatoria. (FR-037 FR-038 SC-015)

## Phase 12: User Story 6 Ampliaciones posteriores (P3)

**Goal / Independent Test**: Reservar estas tareas hasta completar los cinco circuitos generales.

- [x] T051 [US6] Especificar el único módulo Integraciones ARG en specs/012-integraciones/spec.md; organizar proveedores como adaptadores internos de addons/arg_pyme_integraciones/. (FR-015 FR-026 FR-028)
- [x] T052 [US6] Especificar el servicio ARCA dentro del módulo único en specs/013-arca/spec.md, con identidad fiscal, homologación y reintentos, sin emitir comprobantes reales. (FR-022 FR-026 FR-028)
- [ ] T053 [US6] Crear primera spec sectorial según necesidad confirmada en specs/014-rubros/spec.md; conservar orden común y dependencias declaradas. (FR-019 FR-026)

## Phase 13: Polish y entrega

**Goal / Independent Test**: Separar controles técnicos, revisión posterior, aceptación y publicación.

- [x] T054 Registrar instalación y arranque por módulo con versiones en docs/entregas/CONTROLES-TECNICOS.md. (FR-018)
- [ ] T055 Realizar QA funcional/visual posterior con el usuario usando quickstart; registrar límites, resultados y aceptación en docs/entregas/QA.md. (FR-006 FR-008 FR-009 FR-016 SC-001 SC-002 SC-003 SC-004 SC-005 SC-007 SC-009 SC-010)
- [x] T056 Preparar release con documentación, licencias, composición y estado real en CHANGELOG.md y docs/entregas/RELEASE.md. (FR-001 FR-017 FR-018 FR-020)

## Dependencies & Execution Order

Completar Setup y Foundational antes de código consumidor. Desarrollar un módulo por vez.
Aplicar US2 → US4 → US1 → US7 para completar los cinco circuitos; documentar US3 durante sus entregas.
Preparar US5, US8, US9 y US10 desde el inicio; publicar solamente una revisión concreta preparada.
Diferir US6 hasta completar el núcleo. No exigir US6 para liberar la gestión básica.
Integrar ventas-stock después de Ventas y Stock; integrar compras-stock después de Compras y Stock.
Completar secuencias en Foundational antes de la primera persistencia documental de US1.
Realizar controles técnicos por módulo; ejecutar QA funcional/visual después de su instalación autorizada.

## Parallel Examples

La secuencia de módulos prevalece. Las siguientes son posibilidades documentales, no un lanzamiento paralelo.
| Historia | Trabajo independiente después de fijar contratos |
| --- | --- |
| US1 | Manual de Ventas y ejemplos de Compras, después de fijar sus specs |
| US2 | Documentación de composición y ejemplo de servicios sin Stock |
| US3 | Guía de exportación y guía de recuperación |
| US4 | Guía de marca y diccionario de iconos, después del contrato visual |
| US5 | Guía de contribución y preparación de portada |
| US6 | Investigación de servicios y relevamiento sectorial, después del núcleo |
| US7 | Diccionario de hechos y ejemplos conciliables, después de definir granularidades |
| US8 | Guion de presentación y guía de estilo de miniaturas, después de definir identidad y serie |
| US9 | Inventario de accesos de asistencia y diseño de avatar, tras definir alcance y composición |
| US10 | Guía de personalización y proceso de aportes, después de fijar contratos de módulo |

- [x] T057 [US1] Implementar PRE como arg.pyme.quotation y generar PED separado e idempotente desde PRE confirmado, con relaciones de cabecera/línea y contrato docs/tecnica/CONTRATO-PRESUPUESTO-PEDIDO.md. (FR-040)

## Implementation Strategy

Iniciar con la spec de Base ARG; continuar experiencia visual, maestros y presupuesto sencillo como primer MVP operativo.
Completar después los cinco circuitos básicos y sus puentes. Mantener integraciones y rubros como etapa siguiente.
Generar plan y tareas detalladas en cada spec independiente antes de implementar su addon.
No interpretar este backlog como módulos ya creados o instalados. Mantener documentación con cada entrega.

- [x] T058 [US1] Aplicar contrato docs/tecnica/ESTADOS-Y-PENDIENTES.md a cada documento, matrices e informes; conservar origen y trazabilidad de parciales y revisiones sin duplicar compromisos. (FR-041)

## Conciliación con la implementación final

Los paths de componentes se concretaron en document_actions.js/document_matrix.xml dentro de
addons/arg_pyme_ui/static/src/components/, sin subcarpetas homónimas. Soporte y bot están en
views/help_support.xml, controllers/help_support.py, models/mail_bot.py y data/branding.xml.
El maestro de productos se implementa en models/product_template.py. Tipo/secuencia y asignación
común se concretan en Base models/document_identity.py, no en el document_type.py inicialmente previsto. Los roles operativos usan
permisos nativos más ACL/reglas propias; no se creó otro sistema de identidades. Consultar manual
técnico y entrega de cada módulo para los paths finales. Estos ajustes de organización no amplían
los circuitos ni duplican fuentes.

T040: audiencia, presentador, serie y recorridos preparados; URL real del canal sigue pendiente.
T053: primera necesidad sectorial no confirmada; queda para la fase posterior al núcleo.
T055: QA funcional/visual y aceptación posteriores, según preferencia expresa del usuario.
La publicación remota, videos y contactos reales no se presuponen por marcar tareas documentales.
