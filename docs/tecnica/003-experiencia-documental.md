# Interfaz ARG · técnica

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Odoo20/OWL4: Component, useProps y standardActionServiceProps; navegación exclusivamente por menuService efectivo.
arg_form extiende FormController y delega guardado/creación/descarte/retorno a callbacks nativos. arg_list conserva renderer y paginación nativos.
Los consumidores deben usar js_class=arg_form/arg_list; no se sustituyen vistas de terceros globalmente.
Temas CSS acotados al backend, controles con texto y foco; no MutationObserver ni clicks simulados.
Soporte: session_info.support_url y entrada del menú de usuario redirigen a /arg/soporte; /arg/ayuda usa ACL de recursos.
El bot se actualiza por función XML @api.model y hook idempotente; base.partner_root e IDs nativos se preservan.
Image/Binary usa BinaryBytes de Odoo20 con PNG propio. Respuestas nativas adaptan literales y enlace de documentación.
Assets se compilan en servidor. Controles de arranque Chromium sólo autentican y cargan página inicial; no recorren procesos de negocio.

UI20.0.1.0.1 incluye SVG originales con texto para controles comunes/áreas. Documentos presenta
estados mediante texto e icono y explica alcance indeterminado tanto en pantalla como PDF.
GET /arg/acerca requiere usuario interno y ofrece autoría, plataforma y licencias sin consultar
configuración privada. La disponibilidad de estas rutas es control técnico, no revisión visual.
