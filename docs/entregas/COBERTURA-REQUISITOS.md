# Cobertura de requisitos y límites de verificación

Comprobación de cierre del núcleo. Cada fila apunta a fuente o contrato inspeccionado; no declara
aceptación funcional. Instalación, disponibilidad, comprobaciones técnicas y QA son hitos distintos.
Los resultados de instalación y sus hashes se registran en [controles](CONTROLES-TECNICOS.md) y
[cierre contractual](CIERRE-DE-CONTRATOS.md). La publicación remota sigue pendiente de decisión.

## Producto general

| Requisito | Evidencia inspeccionada | Estado y límite |
| --- | --- | --- |
| FR-001 | [NOTICE.md](../../NOTICE.md)<br>[docs/MANIFIESTO.md](../MANIFIESTO.md) | Código/documentación presentes y licencias adoptadas; difusión pública pendiente. |
| FR-002 | [docs/tecnica/OPERACION-Y-RECUPERACION.md](../tecnica/OPERACION-Y-RECUPERACION.md)<br>[docs/tecnica/exportacion.md](../tecnica/exportacion.md) | Instalación/exportación documentadas; demo restaurada técnicamente. Restauración con documentos de negocio para QA posterior. |
| FR-003 | [docs/CATALOGO-MODULOS.md](../CATALOGO-MODULOS.md)<br>[composition/versions.lock.json](../../composition/versions.lock.json) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-004 | [addons/arg_pyme_base/views/menu_views.xml](../../addons/arg_pyme_base/views/menu_views.xml)<br>[addons/arg_pyme_ui/static/src/navigation/areas.js](../../addons/arg_pyme_ui/static/src/navigation/areas.js) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-005 | [docs/tecnica/DICCIONARIO-DOCUMENTAL.md](../tecnica/DICCIONARIO-DOCUMENTAL.md)<br>[addons/arg_pyme_ventas/views/sale_order_views.xml](../../addons/arg_pyme_ventas/views/sale_order_views.xml) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-006 | [addons/arg_pyme_ventas/views/quotation_views.xml](../../addons/arg_pyme_ventas/views/quotation_views.xml)<br>[addons/arg_pyme_compras/views/purchase_order_views.xml](../../addons/arg_pyme_compras/views/purchase_order_views.xml) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-007 | [addons/arg_pyme_terceros/models/res_partner.py](../../addons/arg_pyme_terceros/models/res_partner.py)<br>[addons/arg_pyme_ventas/models/quotation.py](../../addons/arg_pyme_ventas/models/quotation.py) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-008 | [addons/arg_pyme_ui/static/src/components/document_actions.js](../../addons/arg_pyme_ui/static/src/components/document_actions.js)<br>[addons/arg_pyme_catalogo/static/src/matrix.js](../../addons/arg_pyme_catalogo/static/src/matrix.js) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-009 | [addons/arg_pyme_documentos/models/document_links.py](../../addons/arg_pyme_documentos/models/document_links.py) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-010 | [addons/arg_pyme_ventas/models/sale_order.py](../../addons/arg_pyme_ventas/models/sale_order.py)<br>[addons/arg_pyme_stock/models/stock_picking.py](../../addons/arg_pyme_stock/models/stock_picking.py)<br>[addons/arg_pyme_administracion/models/treasury_document.py](../../addons/arg_pyme_administracion/models/treasury_document.py) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-011 | [addons/arg_pyme_ui/static/src/navigation/areas.js](../../addons/arg_pyme_ui/static/src/navigation/areas.js) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-012 | [addons/arg_pyme_ui/static/src/scss/tokens.scss](../../addons/arg_pyme_ui/static/src/scss/tokens.scss)<br>[docs/assets/banner.svg](../assets/banner.svg) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-013 | [addons/arg_pyme_ui/static/src/components/document_matrix.xml](../../addons/arg_pyme_ui/static/src/components/document_matrix.xml)<br>[addons/arg_pyme_documentos/static/src/document_widgets.xml](../../addons/arg_pyme_documentos/static/src/document_widgets.xml) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-014 | [addons/arg_pyme_documentos/report/document_templates.xml](../../addons/arg_pyme_documentos/report/document_templates.xml) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-015 | [specs/012-integraciones/spec.md](../../specs/012-integraciones/spec.md) | Contrato de etapa posterior; addon de integraciones/rubro no implementado en el núcleo. |
| FR-016 | [addons/arg_pyme_base/security/ir.access.csv](../../addons/arg_pyme_base/security/ir.access.csv)<br>[addons/arg_pyme_informes/security/ir.access.csv](../../addons/arg_pyme_informes/security/ir.access.csv) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-017 | [README.md](../../README.md)<br>[docs/site/README.md](../site/README.md)<br>[CONTRIBUTING.md](../../CONTRIBUTING.md) | Portada/manuales preparados localmente; publicación GitHub pendiente. |
| FR-018 | [docs/ESTADO-MODULOS.md](../ESTADO-MODULOS.md)<br>[docs/entregas/RELEASE.md](RELEASE.md) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-019 | [specs/014-rubros/spec.md](../../specs/014-rubros/spec.md) | Contrato de etapa posterior; addon de integraciones/rubro no implementado en el núcleo. |
| FR-020 | [docs/MANIFIESTO.md](../MANIFIESTO.md)<br>[NOTICE.md](../../NOTICE.md) | Código/documentación presentes y licencias adoptadas; difusión pública pendiente. |
| FR-021 | [addons/arg_pyme_base/models/document_identity.py](../../addons/arg_pyme_base/models/document_identity.py) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-022 | [addons/arg_pyme_documentos/models/document_mixin.py](../../addons/arg_pyme_documentos/models/document_mixin.py)<br>[addons/arg_pyme_ventas/models/account_move.py](../../addons/arg_pyme_ventas/models/account_move.py) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-023 | [docs/tecnica/HECHOS-Y-DIMENSIONES.md](../tecnica/HECHOS-Y-DIMENSIONES.md)<br>[docs/tecnica/ESTADOS-Y-PENDIENTES.md](../tecnica/ESTADOS-Y-PENDIENTES.md) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-024 | [composition/versions.lock.json](../../composition/versions.lock.json)<br>[docs/entregas/CONTROLES-TECNICOS.md](CONTROLES-TECNICOS.md) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-025 | [addons/arg_pyme_informes/report/facts.py](../../addons/arg_pyme_informes/report/facts.py)<br>[addons/arg_pyme_informes/report/dimensions.py](../../addons/arg_pyme_informes/report/dimensions.py) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-026 | [docs/PLAN-MAESTRO.md](../PLAN-MAESTRO.md) | Límite aplicado: cinco circuitos antes de integraciones y rubros. |
| FR-027 | [addons/arg_pyme_ui/static/src/navigation/areas.xml](../../addons/arg_pyme_ui/static/src/navigation/areas.xml)<br>[addons/arg_pyme_ventas/views/quotation_views.xml](../../addons/arg_pyme_ventas/views/quotation_views.xml) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-028 | [specs/012-integraciones/plan.md](../../specs/012-integraciones/plan.md) | Contrato de etapa posterior; addon de integraciones/rubro no implementado en el núcleo. |
| FR-029 | [docs/ALCANCE-YOUTUBE.md](../ALCANCE-YOUTUBE.md)<br>[addons/arg_pyme_ui/static/src/navigation/areas.xml](../../addons/arg_pyme_ui/static/src/navigation/areas.xml) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-030 | [docs/comunidad/youtube/PLAN-EDITORIAL.md](../comunidad/youtube/PLAN-EDITORIAL.md)<br>[docs/comunidad/youtube/001-presentacion.md](../comunidad/youtube/001-presentacion.md) | Guion, miniatura, serie y ejemplos preparados; canal/video real pendientes. |
| FR-031 | [addons/arg_pyme_base/models/help_resource.py](../../addons/arg_pyme_base/models/help_resource.py)<br>[docs/comunidad/youtube/catalogo.json](../comunidad/youtube/catalogo.json) | Catálogo editable implementado; guías escritas; videos reales pendientes. |
| FR-032 | [addons/arg_pyme_base/models/help_resource.py](../../addons/arg_pyme_base/models/help_resource.py)<br>[docs/comunidad/youtube/MANTENIMIENTO.md](../comunidad/youtube/MANTENIMIENTO.md) | Catálogo editable implementado; guías escritas; videos reales pendientes. |
| FR-033 | [addons/arg_pyme_ui/models/ir_http.py](../../addons/arg_pyme_ui/models/ir_http.py)<br>[addons/arg_pyme_ui/controllers/help_support.py](../../addons/arg_pyme_ui/controllers/help_support.py)<br>[docs/tecnica/INVENTARIO-AYUDA-SOPORTE-BOT.md](../tecnica/INVENTARIO-AYUDA-SOPORTE-BOT.md) | Centro y configuración implementados; sin destinos reales configurados; cobertura funcional posterior. |
| FR-034 | [addons/arg_pyme_base/models/support_config.py](../../addons/arg_pyme_base/models/support_config.py)<br>[addons/arg_pyme_ui/controllers/help_support.py](../../addons/arg_pyme_ui/controllers/help_support.py) | Centro y configuración implementados; sin destinos reales configurados; cobertura funcional posterior. |
| FR-035 | [addons/arg_pyme_ui/models/branding.py](../../addons/arg_pyme_ui/models/branding.py)<br>[addons/arg_pyme_ui/models/mail_bot.py](../../addons/arg_pyme_ui/models/mail_bot.py) | Identidad y adaptación presentes; fuente nativa inventariada; revisión visual de superficies pendiente. |
| FR-036 | [docs/comunidad/CONOCIMIENTO-COMPARTIDO.md](../comunidad/CONOCIMIENTO-COMPARTIDO.md) | Código/documentación presentes y licencias adoptadas; difusión pública pendiente. |
| FR-037 | [docs/tecnica/PERSONALIZACION.md](../tecnica/PERSONALIZACION.md)<br>[AGENTS.md](../../AGENTS.md) | Código/documentación presentes y licencias adoptadas; difusión pública pendiente. |
| FR-038 | [specs/index.json](../../specs/index.json)<br>[docs/INDICE.md](../INDICE.md) | Código/documentación presentes y licencias adoptadas; difusión pública pendiente. |
| FR-039 | [docs/GONZALO-SARUBILO.md](../GONZALO-SARUBILO.md)<br>[addons/arg_pyme_ui/views/help_support.xml](../../addons/arg_pyme_ui/views/help_support.xml) | Código/documentación presentes y licencias adoptadas; difusión pública pendiente. |
| FR-040 | [addons/arg_pyme_ventas/models/quotation.py](../../addons/arg_pyme_ventas/models/quotation.py)<br>[addons/arg_pyme_ventas/models/sale_order.py](../../addons/arg_pyme_ventas/models/sale_order.py) | Implementación presente; controles técnicos; QA funcional/visual posterior. |
| FR-041 | [addons/arg_pyme_documentos/models/document_mixin.py](../../addons/arg_pyme_documentos/models/document_mixin.py)<br>[docs/entregas/CIERRE-DE-CONTRATOS.md](CIERRE-DE-CONTRATOS.md) | Implementación presente; controles técnicos; QA funcional/visual posterior. |

## Requisitos de cada feature

Las numeraciones FR se interpretan dentro de cada spec. Cada feature tiene seis requisitos.
«Fuente preparada» significa que el código/artefacto correspondiente existe y fue inspeccionado;
los escenarios de resultado y aceptación no se ejecutaron anticipadamente.

### 002-base-arg

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Asignar códigos internos por compañía y tipo al primer guardado. | [addons/arg_pyme_base/models/document_identity.py](../../addons/arg_pyme_base/models/document_identity.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-002 — Separar identificadores operativos de referencias fiscales y de terceros. | [addons/arg_pyme_base/models/document_identity.py](../../addons/arg_pyme_base/models/document_identity.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-003 — Ofrecer roles operativos combinables y configuración por compañía. | [addons/arg_pyme_base/security/roles.xml](../../addons/arg_pyme_base/security/roles.xml)<br>[addons/arg_pyme_base/models/res_company.py](../../addons/arg_pyme_base/models/res_company.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-004 — Aplicar permisos en servidor y conservar una administración avanzada accesible. | [addons/arg_pyme_base/security/ir.access.csv](../../addons/arg_pyme_base/security/ir.access.csv) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-005 — Mantener catálogo editable de tutoriales con versiones compatibles y revisión. | [addons/arg_pyme_base/models/help_resource.py](../../addons/arg_pyme_base/models/help_resource.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-006 — Configurar soporte general por correo, WhatsApp o tickets sin envíos automáticos. | [addons/arg_pyme_base/models/support_config.py](../../addons/arg_pyme_base/models/support_config.py) | Fuente preparada; instalación técnica registrada; QA posterior. |

### 003-experiencia-documental

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Organizar áreas y acciones contextuales mediante el árbol de menús efectivo. | [addons/arg_pyme_ui/static/src/navigation/areas.js](../../addons/arg_pyme_ui/static/src/navigation/areas.js) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-002 — Conservar listado, filtros y contexto al abrir o cerrar una ficha. | [addons/arg_pyme_ui/static/src/components/document_actions.js](../../addons/arg_pyme_ui/static/src/components/document_actions.js) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-003 — Compartir guardado, descarte, retorno, foco y semántica entre formularios. | [addons/arg_pyme_ui/static/src/components/document_matrix.xml](../../addons/arg_pyme_ui/static/src/components/document_matrix.xml) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-004 — Mantener matrices alineadas y paginadas con filtros combinables. | [addons/arg_pyme_ui/static/src/components/document_actions.js](../../addons/arg_pyme_ui/static/src/components/document_actions.js)<br>[addons/arg_pyme_catalogo/static/src/matrix.js](../../addons/arg_pyme_catalogo/static/src/matrix.js) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-005 — Aplicar celeste/blanco, branding discreto, claro/oscuro y controles accesibles. | [addons/arg_pyme_ui/static/src/scss/tokens.scss](../../addons/arg_pyme_ui/static/src/scss/tokens.scss) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-006 — Presentar GOXTECHBOT preservando identidad técnica y comportamiento del bot nativo. | [addons/arg_pyme_ui/models/branding.py](../../addons/arg_pyme_ui/models/branding.py)<br>[addons/arg_pyme_ui/models/mail_bot.py](../../addons/arg_pyme_ui/models/mail_bot.py) | Fuente preparada; instalación técnica registrada; QA posterior. |

### 004-terceros

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Permitir alta rápida con nombre y rol y ampliar información en la misma ficha. | [addons/arg_pyme_terceros/views/res_partner_views.xml](../../addons/arg_pyme_terceros/views/res_partner_views.xml) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-002 — Separar datos necesarios para borrador, contacto, entrega y facturación. | [addons/arg_pyme_terceros/views/res_partner_views.xml](../../addons/arg_pyme_terceros/views/res_partner_views.xml) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-003 — Mantener roles combinables sobre una sola identidad. | [addons/arg_pyme_terceros/models/res_partner.py](../../addons/arg_pyme_terceros/models/res_partner.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-004 — Buscar por nombre, código y datos identificatorios disponibles con permisos efectivos. | [addons/arg_pyme_terceros/views/res_partner_views.xml](../../addons/arg_pyme_terceros/views/res_partner_views.xml) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-005 — Organizar identificación, contacto, condiciones e información adicional en orden estable. | [addons/arg_pyme_terceros/views/res_partner_views.xml](../../addons/arg_pyme_terceros/views/res_partner_views.xml) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-006 — Transmitir valores predeterminados por compañía sin reescribir documentos históricos. | [addons/arg_pyme_terceros/models/res_partner.py](../../addons/arg_pyme_terceros/models/res_partner.py) | Fuente preparada; instalación técnica registrada; QA posterior. |

### 005-catalogo

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Mantener productos y servicios con códigos textuales y unidades explícitas. | [addons/arg_pyme_catalogo/models/product_template.py](../../addons/arg_pyme_catalogo/models/product_template.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-002 — Mostrar precio y datos básicos antes de configuración avanzada. | [addons/arg_pyme_catalogo/views/product_template_views.xml](../../addons/arg_pyme_catalogo/views/product_template_views.xml) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-003 — Ofrecer productos por fila y listas por columna con filtros combinables. | [addons/arg_pyme_catalogo/models/pricelist_matrix.py](../../addons/arg_pyme_catalogo/models/pricelist_matrix.py)<br>[addons/arg_pyme_catalogo/static/src/matrix.xml](../../addons/arg_pyme_catalogo/static/src/matrix.xml) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-004 — Aplicar reglas nativas de tarifas y explicitar moneda y vigencia. | [addons/arg_pyme_catalogo/models/pricelist_matrix.py](../../addons/arg_pyme_catalogo/models/pricelist_matrix.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-005 — Mantener atributos y categorías genéricos sin talles obligatorios. | [addons/arg_pyme_catalogo/models/product_attributes.py](../../addons/arg_pyme_catalogo/models/product_attributes.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-006 — Separar costo, precio, margen, moneda y unidades en consulta y edición. | [addons/arg_pyme_catalogo/models/pricelist_matrix.py](../../addons/arg_pyme_catalogo/models/pricelist_matrix.py) | Fuente preparada; instalación técnica registrada; QA posterior. |

### 006-ventas

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Mantener Presupuesto ARG como registro propio con número y estados independientes. | [addons/arg_pyme_ventas/models/quotation.py](../../addons/arg_pyme_ventas/models/quotation.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-002 — Confirmar presupuesto preservando condiciones aprobadas y sin crear efectos físicos o contables. | [addons/arg_pyme_ventas/models/quotation.py](../../addons/arg_pyme_ventas/models/quotation.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-003 — Generar un pedido nativo distinto desde presupuesto confirmado y vincular sus líneas. | [addons/arg_pyme_ventas/models/sale_order.py](../../addons/arg_pyme_ventas/models/sale_order.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-004 — Conservar pedido, presupuesto y revisión aprobada sin convertir un documento en el otro. | [addons/arg_pyme_ventas/models/quotation.py](../../addons/arg_pyme_ventas/models/quotation.py)<br>[addons/arg_pyme_ventas/models/sale_order.py](../../addons/arg_pyme_ventas/models/sale_order.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-005 — Usar remitos y facturas nativos vinculados por líneas y permitir parciales según política. | [addons/arg_pyme_ventas_stock/models/bridge.py](../../addons/arg_pyme_ventas_stock/models/bridge.py)<br>[addons/arg_pyme_ventas/models/account_move.py](../../addons/arg_pyme_ventas/models/account_move.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-006 — Separar estados comerciales, físicos, contables, financieros y fiscales. | [addons/arg_pyme_ventas/models/sale_order.py](../../addons/arg_pyme_ventas/models/sale_order.py)<br>[addons/arg_pyme_administracion/models/money_application.py](../../addons/arg_pyme_administracion/models/money_application.py) | Fuente preparada; instalación técnica registrada; QA posterior. |

### 007-compras

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Gestionar pedido proveedor con estados y numeración propios. | [addons/arg_pyme_compras/models/purchase_order.py](../../addons/arg_pyme_compras/models/purchase_order.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-002 — Aplicar condiciones conocidas y permitir roles combinables en equipos pequeños. | [addons/arg_pyme_compras/models/purchase_order.py](../../addons/arg_pyme_compras/models/purchase_order.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-003 — Usar entradas y facturas recibidas nativas vinculadas por líneas. | [addons/arg_pyme_compras_stock/models/bridge.py](../../addons/arg_pyme_compras_stock/models/bridge.py)<br>[addons/arg_pyme_compras/models/account_move.py](../../addons/arg_pyme_compras/models/account_move.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-004 — Separar recepción física, registro de deuda y pago mediante Administración. | [addons/arg_pyme_compras/models/purchase_order.py](../../addons/arg_pyme_compras/models/purchase_order.py)<br>[addons/arg_pyme_administracion/models/treasury_document.py](../../addons/arg_pyme_administracion/models/treasury_document.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-005 — Registrar devoluciones y ajustes mediante documentos inversos vinculados. | [addons/arg_pyme_compras/models/account_move.py](../../addons/arg_pyme_compras/models/account_move.py)<br>[addons/arg_pyme_stock/models/stock_picking.py](../../addons/arg_pyme_stock/models/stock_picking.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-006 — Conservar moneda, impuestos, unidades y referencia original del proveedor. | [addons/arg_pyme_compras/models/purchase_order.py](../../addons/arg_pyme_compras/models/purchase_order.py) | Fuente preparada; instalación técnica registrada; QA posterior. |

### 008-stock

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Mostrar físico, reserva, disponible y previsto con definiciones separadas. | [addons/arg_pyme_stock/models/stock_quant.py](../../addons/arg_pyme_stock/models/stock_quant.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-002 — Filtrar por compañía, depósito, ubicación y producto antes de calcular resultados. | [addons/arg_pyme_stock/models/stock_quant.py](../../addons/arg_pyme_stock/models/stock_quant.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-003 — Usar movimientos y operaciones nativas para recepciones, entregas y transferencias. | [addons/arg_pyme_stock/models/stock_picking.py](../../addons/arg_pyme_stock/models/stock_picking.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-004 — Conservar pendientes, devoluciones y relaciones con documentos comerciales. | [addons/arg_pyme_stock/models/stock_picking.py](../../addons/arg_pyme_stock/models/stock_picking.py)<br>[addons/arg_pyme_ventas_stock/models/bridge.py](../../addons/arg_pyme_ventas_stock/models/bridge.py)<br>[addons/arg_pyme_compras_stock/models/bridge.py](../../addons/arg_pyme_compras_stock/models/bridge.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-005 — Agrupar conteos por ubicación y generar ajustes mediante mecanismos nativos. | [addons/arg_pyme_stock/models/inventory_count.py](../../addons/arg_pyme_stock/models/inventory_count.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-006 — Conservar responsable, fecha, motivo y trazabilidad del ajuste. | [addons/arg_pyme_stock/models/inventory_count.py](../../addons/arg_pyme_stock/models/inventory_count.py)<br>[addons/arg_pyme_base/migrations/20.0.1.0.3/post-migrate.py](../../addons/arg_pyme_base/migrations/20.0.1.0.3/post-migrate.py) | Fuente preparada; instalación técnica registrada; QA posterior. |

### 009-administracion

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Derivar deuda de apuntes contables publicados y sus residuales. | [addons/arg_pyme_administracion/models/current_account.py](../../addons/arg_pyme_administracion/models/current_account.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-002 — Mostrar origen, vencimiento y aplicaciones sin duplicar saldos. | [addons/arg_pyme_administracion/models/current_account.py](../../addons/arg_pyme_administracion/models/current_account.py)<br>[addons/arg_pyme_administracion/models/money_application.py](../../addons/arg_pyme_administracion/models/money_application.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-003 — Agrupar uno o varios pagos nativos en recibo u orden con secuencia propia. | [addons/arg_pyme_administracion/models/treasury_document.py](../../addons/arg_pyme_administracion/models/treasury_document.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-004 — Usar conciliación nativa y conservar imputaciones por documento y moneda. | [addons/arg_pyme_administracion/models/treasury_native.py](../../addons/arg_pyme_administracion/models/treasury_native.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-005 — Derivar movimientos de liquidez de apuntes publicados del diario. | [addons/arg_pyme_administracion/models/cash_report.py](../../addons/arg_pyme_administracion/models/cash_report.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-006 — Registrar reversión y desaplicación mediante acciones nativas y permisos efectivos. | [addons/arg_pyme_administracion/models/treasury_native.py](../../addons/arg_pyme_administracion/models/treasury_native.py)<br>[addons/arg_pyme_administracion/models/treasury_audit_event.py](../../addons/arg_pyme_administracion/models/treasury_audit_event.py) | Fuente preparada; instalación técnica registrada; QA posterior. |

### 010-informes

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Definir grano, fuente, fecha, moneda y signo por medida. | [addons/arg_pyme_informes/report/facts.py](../../addons/arg_pyme_informes/report/facts.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-002 — Separar hechos de operación, contabilidad y caja en consultas y etiquetas. | [addons/arg_pyme_informes/report/facts.py](../../addons/arg_pyme_informes/report/facts.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-003 — Usar dimensiones compartidas y navegación a fuente autorizada. | [addons/arg_pyme_informes/report/facts.py](../../addons/arg_pyme_informes/report/facts.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-004 — Aplicar filtros en servidor y mostrar corte y criterio de cada total. | [addons/arg_pyme_informes/report/facts.py](../../addons/arg_pyme_informes/report/facts.py)<br>[addons/arg_pyme_informes/report/dimensions.py](../../addons/arg_pyme_informes/report/dimensions.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-005 — Ofrecer salida abierta y documento legible con metadatos de corte. | [addons/arg_pyme_informes/report/export.py](../../addons/arg_pyme_informes/report/export.py)<br>[addons/arg_pyme_informes/report/report_templates.xml](../../addons/arg_pyme_informes/report/report_templates.xml) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-006 — Conservar importes y cantidades sin sumar monedas o unidades incompatibles. | [addons/arg_pyme_informes/report/dimensions.py](../../addons/arg_pyme_informes/report/dimensions.py)<br>[addons/arg_pyme_informes/report/number_format.py](../../addons/arg_pyme_informes/report/number_format.py) | Fuente preparada; instalación técnica registrada; QA posterior. |

### 011-web-comunidad

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Presentar ARG y soberanía con branding Goxtech discreto. | [docs/site/README.md](../site/README.md) | Documentación preparada; publicación/aceptación pendientes. |
| FR-002 — Mostrar estados de desarrollo y experiencia de Gonzalo Sarubilo como aporte declarado. | [docs/GONZALO-SARUBILO.md](../GONZALO-SARUBILO.md) | Documentación preparada; publicación/aceptación pendientes. |
| FR-003 — Centralizar catálogo versionado de tutoriales y revisiones. | [docs/comunidad/youtube/catalogo.json](../comunidad/youtube/catalogo.json)<br>[docs/site/tutoriales/catalogo.yml](../site/tutoriales/catalogo.yml) | Documentación preparada; publicación/aceptación pendientes. |
| FR-004 — Vincular documentos a cada módulo y conservar contenido anterior identificado. | [docs/site/MANUALES.md](../site/MANUALES.md) | Documentación preparada; publicación/aceptación pendientes. |
| FR-005 — Documentar flujo de contribución y reconocimiento comunitario. | [CONTRIBUTING.md](../../CONTRIBUTING.md)<br>[docs/site/comunidad/PROPUESTA.md](../site/comunidad/PROPUESTA.md) | Documentación preparada; publicación/aceptación pendientes. |
| FR-006 — Mantener servicios profesionales opcionales y secundarios al objetivo. | [docs/MANIFIESTO.md](../MANIFIESTO.md) | Documentación preparada; publicación/aceptación pendientes. |

### 012-integraciones

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Agrupar todos los proveedores dentro del único addon Integraciones ARG. | [specs/012-integraciones/spec.md](../../specs/012-integraciones/spec.md)<br>[specs/012-integraciones/plan.md](../../specs/012-integraciones/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-002 — Separar permisos, entorno y credenciales por compañía/proveedor. | [specs/012-integraciones/spec.md](../../specs/012-integraciones/spec.md)<br>[specs/012-integraciones/plan.md](../../specs/012-integraciones/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-003 — Definir contrato de adaptadores, outbox e idempotencia por operación. | [specs/012-integraciones/spec.md](../../specs/012-integraciones/spec.md)<br>[specs/012-integraciones/plan.md](../../specs/012-integraciones/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-004 — Aplicar límites, reintentos acotados y bloqueo concurrente sin duplicar efectos. | [specs/012-integraciones/spec.md](../../specs/012-integraciones/spec.md)<br>[specs/012-integraciones/plan.md](../../specs/012-integraciones/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-005 — Ofrecer estado, última ejecución, error útil y pausa efectiva. | [specs/012-integraciones/spec.md](../../specs/012-integraciones/spec.md)<br>[specs/012-integraciones/plan.md](../../specs/012-integraciones/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-006 — No usar pruebas de conexión que emitan facturas o mensajes reales. | [specs/012-integraciones/spec.md](../../specs/012-integraciones/spec.md)<br>[specs/012-integraciones/plan.md](../../specs/012-integraciones/plan.md) | Etapa posterior, especificada; código y activación no entregados. |

### 013-arca

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Mantener emisor, ambiente y punto de venta separados del código interno. | [specs/013-arca/spec.md](../../specs/013-arca/spec.md)<br>[specs/013-arca/plan.md](../../specs/013-arca/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-002 — Referenciar certificados y claves protegidas sin incorporarlos al repositorio. | [specs/013-arca/spec.md](../../specs/013-arca/spec.md)<br>[specs/013-arca/plan.md](../../specs/013-arca/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-003 — Implementar autorización idempotente y recuperación de resultado incierto. | [specs/013-arca/spec.md](../../specs/013-arca/spec.md)<br>[specs/013-arca/plan.md](../../specs/013-arca/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-004 — Conservar número fiscal, tipo, emisor, punto de venta y evidencia de respuesta. | [specs/013-arca/spec.md](../../specs/013-arca/spec.md)<br>[specs/013-arca/plan.md](../../specs/013-arca/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-005 — Incluir datos fiscales sólo desde respuesta válida y contrato vigente. | [specs/013-arca/spec.md](../../specs/013-arca/spec.md)<br>[specs/013-arca/plan.md](../../specs/013-arca/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-006 — Emitir correcciones mediante documentos vinculados y preservar historial. | [specs/013-arca/spec.md](../../specs/013-arca/spec.md)<br>[specs/013-arca/plan.md](../../specs/013-arca/plan.md) | Etapa posterior, especificada; código y activación no entregados. |

### 014-rubros

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Exigir spec independiente para cada rubro o personalización. | [specs/014-rubros/spec.md](../../specs/014-rubros/spec.md)<br>[specs/014-rubros/plan.md](../../specs/014-rubros/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-002 — Expresar dependencias y compatibilidad sin modificar reglas generales implícitamente. | [specs/014-rubros/spec.md](../../specs/014-rubros/spec.md)<br>[specs/014-rubros/plan.md](../../specs/014-rubros/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-003 — Mantener nombres ARG y contratos documentales comunes. | [specs/014-rubros/spec.md](../../specs/014-rubros/spec.md)<br>[specs/014-rubros/plan.md](../../specs/014-rubros/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-004 — No crear otra contabilidad, otro stock ni otro módulo de proveedores externos. | [specs/014-rubros/spec.md](../../specs/014-rubros/spec.md)<br>[specs/014-rubros/plan.md](../../specs/014-rubros/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-005 — Registrar instalación, QA, aceptación y versión del rubro por separado. | [specs/014-rubros/spec.md](../../specs/014-rubros/spec.md)<br>[specs/014-rubros/plan.md](../../specs/014-rubros/plan.md) | Etapa posterior, especificada; código y activación no entregados. |
| FR-006 — Mantener configuración especializada opcional y tutoriales versionados. | [specs/014-rubros/spec.md](../../specs/014-rubros/spec.md)<br>[specs/014-rubros/plan.md](../../specs/014-rubros/plan.md) | Etapa posterior, especificada; código y activación no entregados. |

### 015-documentos

| Requisito | Fuente o contrato | Estado |
| --- | --- | --- |
| FR-001 — Asignar código corto e identidad inmutable al primer guardado documental válido. | [addons/arg_pyme_documentos/models/document_mixin.py](../../addons/arg_pyme_documentos/models/document_mixin.py)<br>[addons/arg_pyme_base/models/document_identity.py](../../addons/arg_pyme_base/models/document_identity.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-002 — Separar secuencia interna, número fiscal y referencia de tercero. | [addons/arg_pyme_documentos/models/document_mixin.py](../../addons/arg_pyme_documentos/models/document_mixin.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-003 — Conservar relaciones de origen y derivados y cantidades netas por línea. Mostrar simultáneamente los ejes aplicables de confirmación, entrega/recepción, facturación y cobro/pago, cada uno pendiente, parcial o completo según su cantidad o importe. REC/OPA muestran además aplicación e importe libre; un documento relacionado en borrador no acredita cumplimiento. | [addons/arg_pyme_documentos/models/document_links.py](../../addons/arg_pyme_documentos/models/document_links.py)<br>[addons/arg_pyme_documentos/models/document_mixin.py](../../addons/arg_pyme_documentos/models/document_mixin.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-004 — Preservar documento origen, revisión e historial tras generar derivados. | [addons/arg_pyme_documentos/models/document_links.py](../../addons/arg_pyme_documentos/models/document_links.py)<br>[addons/arg_pyme_ventas/models/quotation.py](../../addons/arg_pyme_ventas/models/quotation.py) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-005 — Proveer plantillas QWeb originales con jerarquía y orden común. | [addons/arg_pyme_documentos/report/document_templates.xml](../../addons/arg_pyme_documentos/report/document_templates.xml) | Fuente preparada; instalación técnica registrada; QA posterior. |
| FR-006 — Respetar permisos, moneda, unidades y datos históricos al imprimir. | [addons/arg_pyme_documentos/report/document_report.py](../../addons/arg_pyme_documentos/report/document_report.py) | Fuente preparada; instalación técnica registrada; QA posterior. |

## Criterios de resultado

| Criterio general | Evidencia y fase pendiente |
| --- | --- |
| SC-001 | Carga mínima definida e implementada; recorrido de presupuesto para QA posterior. |
| SC-002 | Orden común en fuente; revisión de todas las fichas renderizadas pendiente. |
| SC-003 | Generación/vínculos en fuente; recorrido con derivados para QA posterior. |
| SC-004 | Restauración técnica de demo y adjuntos registrada. La demo no contiene documentos de negocio; no se prueba su recuperación por un conteo de cero. |
| SC-005 | Callbacks/listas nativas y guardas de matriz presentes; recorrido de teclado pendiente. |
| SC-006 | Manuales funcionales/técnicos preparados y vinculados a composición; publicación remota pendiente. |
| SC-007 | Ejes y calidad de dato en fuente; parciales/reversiones con documentos para QA posterior. |
| SC-008 | Enlaces y contenido local comprobados; portada pública de GitHub aún sin actualizar. |
| SC-009 | Secuencias y unicidades declaradas; concurrencia real pendiente de QA. |
| SC-010 | Lote conciliable escrito; no se crearon operaciones ni se concilió un lote ejecutado. |
| SC-011 | Fichas editoriales versionadas; no hay tutorial publicado aún. |
| SC-012 | Ayuda editable y manuales implementados; enlaces reales de video pendientes. |
| SC-013 | Accesos inventariados y redirección en fuente; canales reales y recorrido de todos los accesos pendientes. |
| SC-014 | Nombre/avatar/textos adaptados por fuente e inventario; legibilidad y superficies en QA posterior. |
| SC-015 | Specs/contratos/ejemplos locales vinculados desde personalización e índice; disponibilidad pública pendiente. |

## Conclusión de alcance

La evidencia técnica acredita la entrega de código instalado con ejemplos, no el cumplimiento
funcional de cada escenario. Las correcciones de cierre resuelven incumplimientos concretos de
fuente antes de continuar. Quedan separados publicación remota, configuración de canales reales,
QA/aceptación e incrementos futuros. El conocimiento de estos pendientes no redefine los requisitos.
