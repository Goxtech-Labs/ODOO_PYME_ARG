# Canales Goxtech · 0.1.2-dev

El titular eligió sus canales públicos de Goxtech para Odoo Pymes ARG el 2 de noviembre de 2026.
Los destinos están en el [perfil público](../comunidad/canales.json) y la
[guía de contacto](../comunidad/CONTACTO.md). Se verificaron en el pie de la web oficial.

Base ARG 20.0.1.0.4 incorpora web y canal de YouTube editables. Interfaz ARG 20.0.1.0.2 los muestra
en Ayuda, Soporte y Acerca de. WhatsApp es el contacto principal y correo el alternativo.
El canal general se presenta separado de los videos compatibles de cada tarea, que siguen pendientes.
Los campos no tienen valores Goxtech obligatorios: cada operador configura sus propios destinos.

## Instalación y controles técnicos

Paquete de 185 archivos, SHA256 `9465b28581d1d6e082234da2db3a185ec367f4a3c99980332269d9c3a9df6a31`.
Actualización explícita de Base e Interfaz en aislado y demo, conservando los otros diez addons ARG.
91 módulos instalados; fuentes de ambos entornos coinciden con todos los hashes del paquete.
El helper de configuración valida mediante el transient de Ajustes y escribe sólo cinco parámetros
públicos: web, canal YouTube, WhatsApp, correo y canal principal. No ejecuta el guardado global.

Ayuda, Soporte y Acerca de responden HTTP 200 con web y canal correctos; Soporte incluye el enlace
WhatsApp y `mailto:` esperados. No se abrieron conversaciones, enviaron correos ni publicaron videos.
La demo conserva Odoo y túnel activos; el aislado conserva el túnel inactivo.
Cero documentos, asientos, pagos, movimientos de stock, cron y servidores de correo activos.
Estos son controles de instalación/configuración/renderizado, no QA funcional/visual de los circuitos.

Revisión estática independiente de seis archivos de addon, helper y perfil: sin bloqueantes.
Se corrigió aceptación de puertos inválidos en URLs. Misma familia de modelo y cuenta; no auditoría exhaustiva.

## Recuperación

Antes de esta actualización se creó un snapshot y un respaldo completo con Odoo detenido:
1401408859 bytes, SHA256 `37b75f76f9513dbb18a17f786cf1b98e3db04b0452a8e1d2fc45a833cd837335`.
Integridad zstd verificada. Este respaldo previo no se restauró; la composición anterior sí tiene
una [restauración aislada registrada](RELEASE-0.1.1-dev.md). No se atribuye esa restauración al nuevo paquete.
Una reversión debe considerar cambios posteriores en la base; no restaurar automáticamente perdiendo escrituras.

QA funcional/visual y aceptación continúan pendientes con el usuario. Integraciones, ARCA y rubros son posteriores.
