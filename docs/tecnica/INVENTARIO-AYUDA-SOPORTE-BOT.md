# Superficies de ayuda y bot ARG

Composición Community20 de la demo. Inventario de fuente instalado, no certificación visual.
Revalidar al cambiar la composición; cada nueva superficie requiere revisión propia.

| Superficie | Implementación | Estado de evidencia |
| --- | --- | --- |
| Menú usuario, Ayuda nativa | Registro support y session_info.support_url → /arg/soporte | Fuente y arranque técnico |
| Ayuda de módulo | /arg/ayuda?module=arg_pyme_* y catálogo editable con manual | Fuente, fichas y arranque |
| Bot en contactos/chats | base.partner_root conserva ID; hook actualiza nombre/PNG propios | Fuente, instalación e identidad consultada |
| Respuestas y documentación del bot | mail.bot._get_answer adapta nombre; _get_style_dict usa /arg/ayuda | Fuente; contenido nativo completo para QA posterior |
| Acerca de ARG | Entrada propia arg_about → /arg/acerca, autoría/plataforma/licencias | Fuente y arranque técnico HTTP200 |
| Error técnico | support_url central; abrir soporte no reenvía traceback ni secretos | Fuente; escenarios de error para QA posterior |

En Community20 el archivo nativo webclient/user_menu/user_menu_items.js registra support; no hay
entrada About separada allí. ARG añade la suya sin sustituir atribuciones legales del core.
Los textos/canales se administran centralmente en Base. Se conservan ayudas internas si faltan destinos.
El cambio visible de OdooBot mantiene su comportamiento nativo; no incorpora un servicio externo.

[Base](../../addons/arg_pyme_base/models/help_resource.py), [soporte](../../addons/arg_pyme_base/models/support_config.py),
[controlador](../../addons/arg_pyme_ui/controllers/help_support.py), [sesión](../../addons/arg_pyme_ui/models/ir_http.py),
[bot](../../addons/arg_pyme_ui/models/mail_bot.py), [identidad](../../addons/arg_pyme_ui/models/branding.py),
[entradas](../../addons/arg_pyme_ui/static/src/navigation/areas.js).
