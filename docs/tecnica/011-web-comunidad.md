# Portada y comunidad · técnica

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Entrega documental Markdown; no añade addon, ACL ni dependencia de hosting. README funciona en
GitHub y por lectura local. docs/site organiza las rutas de entrada; assets originales SVG no
cargan imágenes, scripts ni fuentes de terceros. No se distribuyen capturas FactuSOL.

La fuente editorial única es [catalogo.json](../comunidad/youtube/catalogo.json). El YAML del sitio
es un puntero relativo, no otra copia de las fichas. Cada ficha conserva ID, módulo/tarea, estado,
versión, idioma, revisión, URL y reemplazo. Sin URL real queda planeada. El catálogo editable
`arg.pyme.help.resource` dentro de Odoo es configuración de esa instalación: se actualiza de forma
explícita y no se sobreescribe automáticamente desde el JSON editorial.

Los módulos existentes enlazan manuales escritos; la portada agrupa los recorridos. Conservar
contenido anterior identificado al cambiar versiones. Verificar enlaces locales, IDs únicos,
reemplazos existentes, formatos y avisos de licencia antes de distribuir una entrega.

Código propio AGPL-3.0-only; documentación y recursos originales CC-BY-SA-4.0, según
[NOTICE](../../NOTICE.md). Cada addon incorpora textos y avisos para su distribución independiente.
Spec Kit conserva MIT; Odoo y dependencias mantienen sus licencias. No se cambian atribuciones nativas.

La operación privada, credenciales y respaldos quedan fuera del árbol público. La publicación
remota y GitHub Pages se registran como hitos separados; esta entrega prepara el repositorio y
no activa hosting, YouTube ni mensajes automáticamente.
