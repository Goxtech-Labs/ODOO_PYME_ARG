# Controles técnicos consolidados — 2026-11-01

Alcance: preparación, instalación/actualización y arranque. No se ejecutaron recorridos de negocio
ni QA visual antes de entrega, conforme al flujo acordado. Instalación no equivale a aceptación.

| Entrega | Evidencia pública | Resultado técnico |
| --- | --- | --- |
| Base | [002](002-base-arg.md) | Tipos/secuencias, compañía, ayuda y soporte instalados |
| Interfaz | [003](003-experiencia-documental.md) | Assets y Home autenticado, sin error de arranque |
| Terceros | [004](004-terceros.md) | Modelos/vistas instalados y maestros ficticios |
| Catálogo | [005](005-catalogo.md) | Productos/listas/matrices instalados |
| Motor documental | [015](015-documentos.md) | Identidad/vínculos e impresión común instalados |
| Ventas | [006](006-ventas.md) | PRE propio y PED separado; vistas instaladas |
| Compras | [007](007-compras.md) | PPC y derivados nativos; vistas instaladas |
| Stock y puentes | [008](008-stock.md) | Instalación técnica y dependencias explícitas |
| Administración | [009](009-administracion.md) | REC/OPA, aplicaciones y caja instalados |
| Informes | [010](010-informes.md) | Once fuentes y salida vacía HTML/CSV/PDF 200 |
| Comunidad | [011](011-web-comunidad.md) | Portada/manuales/licencias preparados; enlaces verificados por entrega |

Instalaciones limpias aisladas: Informes mínimo 31 módulos sin Contabilidad/Stock; servicios 74
módulos sin Stock; Administración con dependencias 86 módulos sin puentes físicos ARG opcionales.
La demo completa usa 91 módulos (79 nativos/dependencias y 12 ARG). En todos los controles técnicos
se mantuvieron cron/correo desactivados y no se crearon operaciones de negocio.

AST Python, XML, JS, manifests/dependencias y Gitleaks se verifican sobre el paquete identificado.
Revisiones independientes de fuente usan sesiones de la misma familia y cuenta; no constituyen
una auditoría exhaustiva ni una prueba funcional de roles, compañías, cálculos o concurrencia.
La evidencia operativa detallada, hashes y capturas se conserva de forma privada por el propietario.

El respaldo inicial fue restaurado aisladamente; los respaldos incrementales de cada entrega
registran por separado integridad y restauración. No se atribuye una restauración a un archivo por
haber verificado sólo su checksum. Ver [release](RELEASE.md) y [QA pendiente](QA.md).

La composición final también fue restaurada desde su propio respaldo completo en un contenedor
nuevo sin red: 91 módulos, 183 hashes de código, 78/78 adjuntos correctos y login local HTTP 200.
Túnel bloqueado, cron/correo y operaciones de negocio en cero. Se dejó apagado; ver release para hash.

## Cierre 0.1.1-dev

[Correcciones contractuales](CIERRE-DE-CONTRATOS.md): nueve addons actualizados,185 hashes
fuente/paquete/runtime coincidentes. AJU realineado sin identidades previas; Inicio/Ayuda/Soporte/
Acerca de arrancan; Informes vacío HTML/CSV/PDF 200. Ocho verificaciones del helper numérico puro,
sin DB ni operaciones. Instalación mínima nueva 31 módulos y perfil servicios 74 sin Stock coherentes
con nuevas versiones. El [mapa de 125 requisitos](COBERTURA-REQUISITOS.md) conserva límites y pendientes.

La composición corregida 0.1.1-dev se restauró desde su propio respaldo:185 fuentes/91 módulos/78 adjuntos correctos, sin red/túnel y copia apagada. Ver RELEASE para hash y límites.
