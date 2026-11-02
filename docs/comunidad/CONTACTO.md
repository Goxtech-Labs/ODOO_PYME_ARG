# Canales oficiales de Odoo Pymes ARG

El responsable eligió los canales públicos de Goxtech para este proyecto el 2 de noviembre de 2026.
Se verificaron en el pie de la [web oficial](https://goxtech.com.ar/).

| Uso | Destino |
| --- | --- |
| Web | [Goxtech](https://goxtech.com.ar/) |
| YouTube | [Goxtech Argentina](https://www.youtube.com/@Goxtech_Arg) |
| WhatsApp, contacto principal | [+54 9 3541 65-1038](https://wa.me/5493541651038) |
| Correo | [gonzalo@goxtech.com.ar](mailto:gonzalo@goxtech.com.ar) |

El canal general no reemplaza los tutoriales versionados por módulo. Las fichas de los videos
ARG todavía pendientes mantienen ese estado hasta que exista contenido revisado para esa tarea.
Abrir un enlace queda a elección del usuario; el sistema no envía consultas automáticamente.

Estos destinos corresponden al proyecto comunitario y su demo. Cada instalación puede editar
web, canal, correo, WhatsApp y tickets desde Ajustes → Gestión ARG. El código no impone una cuenta
Goxtech ni activa integraciones externas. No hay sistema de tickets definido actualmente.

El [perfil público](canales.json) registra los destinos elegidos. Para aplicarlo explícitamente,
usar [configure_public_contacts.py](../../ops/configure_public_contacts.py) dentro de `odoo shell`,
con `ARG_PUBLIC_CONTACTS_JSON` apuntando a la copia de ese JSON elegida por el operador.
El helper valida mediante los campos instalados y cambia sólo los cinco parámetros indicados;
no ejecuta el guardado global de Ajustes ni altera canales de terceros.
