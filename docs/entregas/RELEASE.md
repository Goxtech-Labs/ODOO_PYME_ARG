# Odoo Pymes ARG — 0.1.1-dev

Fecha del corte técnico:2026-11-01. Núcleo genérico desarrollado e instalado técnicamente en demo.
Código y documentación publicados por decisión del titular; el
[PR #1](https://github.com/Goxtech-Labs/ODOO_PYME_ARG/pull/1) registra su integración a main.
QA funcional/visual y aceptación pendientes; no se presenta como versión productiva validada.
Publicar el código no acredita aceptación funcional ni constituye un tag de release.

[Composición](../../composition/versions.lock.json):91 módulos,79 nativos/dependencias y12 addons ARG.
Paquete de 185 archivos desplegado: SHA256 `b4501c7bb1befdc6fac6c77596271bae6ceb9f7320fad60fcee013902affbb2c`.
Versiones en fuente, paquete y runtime coinciden. La procedencia del paquete Odoo y el SHA de
investigación son referencias distintas. Ver [controles](CONTROLES-TECNICOS.md) y
[correcciones de cierre](CIERRE-DE-CONTRATOS.md).

## Contenido

Base, Interfaz, Terceros, Catálogo, Documentos, Ventas, Compras, Stock, Administración, Informes y
dos puentes físicos. Cinco circuitos genéricos con documentos propios, código corto, estados y
pendientes independientes. PRE conserva identidad distinta del PED que genera; stock y contabilidad
nativos son las fuentes de efecto. Informes no mezcla etapas ni inventa atribuciones monetarias.

Manuales funcionales/técnicos, ejemplos ficticios, quince specs con contratos/tareas, guías de
instalación, backup, exportación y personalización; portada y comunidad. [Cobertura de 125 requisitos](COBERTURA-REQUISITOS.md)
identifica fuente, evidencia y límites de resultado sin sustituir QA por presencia de archivos.

AGPL-3.0-only para código original y CC-BY-SA-4.0 para documentación/recursos originales.
[NOTICE](../../NOTICE.md) conserva alcance, atribuciones y excepciones. Cada addon incorpora sus avisos.
Para empaquetar, [package_release.py](../../ops/package_release.py) genera tar determinista, SHA por archivo,
controles sintácticos y Gitleaks redactado. Conservar recibos junto al respaldo privado.
No distribuir dumps, configuración protegida, filestore ni credenciales en el Git público.

## Instalación y verificación técnica

Actualización exacta de nueve addons afectados en aislado y demo; sin actualización global.
La [guía](../site/INSTALACION.md) incluye instalación nueva y actualización desde 0.1.0-dev.
Instalación mínima limpia 31 módulos sin Contabilidad/Stock; perfil de servicios 74 sin Stock actualizado.
Home/Ayuda/Soporte/Acerca de HTTP 200 sin errores JS; Informes vacío HTML/CSV/PDF 200.
Ocho verificaciones del helper numérico puro, sin DB ni operaciones de negocio.
Cron/correo desactivados; sólo maestros ficticios y filtros transitorios, cero documentos/asientos/pagos/stock.
Estos controles no prueban los recorridos funcionales ni todos los roles/compañías.

## Recuperación de esta composición

Respaldo completo de1401399991bytes, con Odoo detenido, integridad zstd y SHA256
`4cb85cbcc4ecd7d2220dbd110411bb10354002aa873aa8a16f96ac1c70ffbcc4`. Restaurado en un contenedor nuevo sin interfaz de red y con el túnel bloqueado.
Antes del primer arranque de Odoo se normalizó la URL de la copia a loopback y se desactivaron cron/correo.
Se recuperaron 91 módulos, los 185 archivos de código del paquete y 78/78 adjuntos con checksum correcto;
AJU referencia el modelo correcto y el login local responde HTTP 200. Se dejó el contenedor apagado.
La demo no contiene documentos de negocio: su recuperación funcional no se prueba por un conteo de cero.
El respaldo de 0.1.0-dev también fue restaurado, como hito histórico diferente.

## Pendientes separados

La publicación y su integración a main se siguen mediante el PR enlazado arriba.
La publicación de una versión estable es un hito posterior. GitHub Pages no está activado por esta entrega.
Manuales escritos disponibles; videos/canal real, destinos de soporte y contacto privado de seguridad
se configuran cuando sean aportados. No se inventan URLs ni se envían mensajes.
Integraciones, ARCA y rubros son incrementos posteriores, sin activación ni emisión fiscal en el núcleo.

[QA posterior](QA.md): permisos/ACL, múltiples compañías, teclado/temas, parciales/revisiones,
concurrencia, reversión, cálculos y recuperación con documentos, según quickstarts.
Registrar resultados y aceptación con el usuario después de la instalación autorizada.
