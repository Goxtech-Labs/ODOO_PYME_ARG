# Base ARG · implementación

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Addon original AGPL-3 según licencia adoptada; sin cambios al core. Dependencias base/web.
Odoo20 usa ir.access (operation/domain), res.groups.privilege y campos user_writeable para preferencias.
Identidad inmutable, secuencia única por tipo y compañía, bloqueo de reinicios/formato por edición directa.
Allocator privado verifica acceso al origen/compañía y registra identidad técnica mediante elevación mínima.
Actualiza auditoría del origen para que concurrencia REPEATABLE READ produzca reintento transaccional con snapshot fresco;
la unicidad SQL complementa la serialización. No confundir este diseño revisado con QA de concurrencia ejecutado.
Catálogo de ayuda compartido sin datos de negocio. Soporte configurado globalmente en parámetros; sin secretos de proveedores.
La navegación a documentos verifica modelo y acceso sin sudo. El mixin consumidor llega en Documentos ARG.

Versión20.0.1.0.2: guard privado res.currency._arg_require_conversion exige tasa propia efectiva antes de convertir; ver006-ventas.md.

Base20.0.1.0.3 registra AJU como arg.pyme.inventory.adjustment. La migración sólo corrige
configuración antigua sin identidades; si existen referencias AJU al modelo viejo, aborta y pide
migración explícita. No cambia secuencia ni renumera. El registro sigue siendo una referencia
a documento operativo, no un movimiento físico adicional.

## Web, canal y contactos públicos

Ajustes → Gestión ARG permite editar web del responsable y canal general de YouTube, además
de correo, WhatsApp y tickets. La demo usa los [canales oficiales elegidos](../comunidad/CONTACTO.md).
Ayuda, Soporte y Acerca de muestran los enlaces configurados. El canal general no se presenta
como un tutorial específico compatible; las fichas de video conservan sus estados y versiones.
