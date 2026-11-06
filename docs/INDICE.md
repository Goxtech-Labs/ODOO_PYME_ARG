# Mapa de documentación y programación

Documentación preparada para programar módulo por módulo. La instalación demo es Community nativa;
Base, Interfaz, maestros, Motor documental y los cinco circuitos ARG están desarrollados e instalados; QA posterior pendiente. Las specs012–014 conservan los contratos de integraciones/rubros; su desarrollo se ordena ahora por el plan016 de expansión.

## Comenzar

- [Propósito](MANIFIESTO.md) y [autor](GONZALO-SARUBILO.md).
- [Plan maestro](PLAN-MAESTRO.md), [constitución](../.specify/memory/constitution.md) y [spec general](../specs/001-pyme-argentina/spec.md).
- [Diseño visual](DISENO-VISUAL.md) y [maqueta original](assets/maqueta-documental.svg).
- [Diccionario documental](tecnica/DICCIONARIO-DOCUMENTAL.md) y [PRE/PED separados](tecnica/CONTRATO-PRESUPUESTO-PEDIDO.md).
- [Hechos/dimensiones](tecnica/HECHOS-Y-DIMENSIONES.md), [roles/datos mínimos](tecnica/PERMISOS-Y-DATOS-MINIMOS.md).
- [Decisiones Odoo20](tecnica/DECISIONES-ODOO20.md), [entorno demo](tecnica/ENTORNO-DEMO.md) y [operación/recuperación](tecnica/OPERACION-Y-RECUPERACION.md).
- [Ejemplos](ejemplos/DATOS-DE-EJEMPLO.md), [personalización/IA](tecnica/PERSONALIZACION.md) y [contribuciones](../CONTRIBUTING.md).
- [YouTube](comunidad/youtube/PLAN-EDITORIAL.md), [plantilla](comunidad/youtube/PLANTILLA-TUTORIAL.md) y [mantenimiento](comunidad/youtube/MANTENIMIENTO.md).

## Orden de implementación

La numeración de features identifica documentos; el orden real es la tabla siguiente.
Cada feature contiene spec, plan, research, data-model, contratos, quickstart, tareas y checklist.

| Paso | Especificación | Destino | Estado |
| --- | --- | --- | --- |
| 01 | [Base ARG](../specs/002-base-arg/spec.md) · [tareas](../specs/002-base-arg/tasks.md) | `addons/arg_pyme_base` | desarrollado e instalado; QA pendiente |
| 02 | [Experiencia y presentación ARG](../specs/003-experiencia-documental/spec.md) · [tareas](../specs/003-experiencia-documental/tasks.md) | `addons/arg_pyme_ui` | desarrollado e instalado; QA pendiente |
| 03 | [Terceros ARG](../specs/004-terceros/spec.md) · [tareas](../specs/004-terceros/tasks.md) | `addons/arg_pyme_terceros` | desarrollado e instalado; QA pendiente |
| 04 | [Catálogo y precios ARG](../specs/005-catalogo/spec.md) · [tareas](../specs/005-catalogo/tasks.md) | `addons/arg_pyme_catalogo` | desarrollado e instalado; QA pendiente |
| 05 | [Motor documental e impresión ARG](../specs/015-documentos/spec.md) · [tareas](../specs/015-documentos/tasks.md) | `addons/arg_pyme_documentos` | desarrollado e instalado; QA pendiente |
| 06 | [Circuito Ventas ARG](../specs/006-ventas/spec.md) · [tareas](../specs/006-ventas/tasks.md) | `addons/arg_pyme_ventas` | comercial, puente físico y dinero aplicado instalados; QA pendiente |
| 07 | [Circuito Compras ARG](../specs/007-compras/spec.md) · [tareas](../specs/007-compras/tasks.md) | `addons/arg_pyme_compras` | comercial, puente físico y dinero aplicado instalados; QA pendiente |
| 08 | [Circuito Stock ARG](../specs/008-stock/spec.md) · [tareas](../specs/008-stock/tasks.md) | `addons/arg_pyme_stock` | núcleo y puentes desplegados; QA pendiente |
| 09 | [Circuito Administración ARG](../specs/009-administracion/spec.md) · [tareas](../specs/009-administracion/tasks.md) | `addons/arg_pyme_administracion` | cuentas, recibos/pagos/aplicaciones/caja instalados; QA pendiente |
| 10 | [Circuito Informes ARG](../specs/010-informes/spec.md) · [tareas](../specs/010-informes/tasks.md) | `addons/arg_pyme_informes` | desarrollado e instalado; QA pendiente |
| 11 | [Portada y documentación pública ARG](../specs/011-web-comunidad/spec.md) · [tareas](../specs/011-web-comunidad/tasks.md) | `docs/site` | documentación publicada en main; mantenimiento continuo |
| 12 | [Integraciones ARG](../specs/012-integraciones/spec.md) · [tareas](../specs/012-integraciones/tasks.md) | `addons/arg_pyme_integraciones` | posterior al núcleo; código pendiente |
| 13 | [Contrato futuro ARCA dentro de Integraciones ARG](../specs/013-arca/spec.md) · [tareas](../specs/013-arca/tasks.md) | `addons/arg_pyme_integraciones` | posterior al núcleo; homologación pendiente; código pendiente |
| 14 | [Extensiones por rubro y personalizaciones ARG](../specs/014-rubros/spec.md) · [tareas](../specs/014-rubros/tasks.md) | `docs/rubros` | posterior al núcleo; código pendiente |


Última feature entregada: specs/011-web-comunidad/tasks.md. Preparación global en docs/entregas/RELEASE.md. No ejecutar todas las features juntas.
Las tareas del plan general son resumen de producto: usar las de cada módulo para implementar y enlazar avance, sin duplicar trabajo.
Los checks documentales prueban estructura y trazabilidad, no funcionamiento ni aceptación.

## Hitos

1. Base/UI/maestros/documentos: composición, carga mínima y PRE/PED con contratos fijados.
2. Ventas: presupuesto propio y pedido nativo distinto, antes de entregas y facturación.
3. Completar cinco circuitos; instalación técnica por entrega y QA posterior con ejemplos.
4. Manuales/tutoriales actualizados, licencia definitiva y publicación de la composición aceptada.
5. Integraciones centralizadas y rubros mediante nuevas entregas específicas.

Canal YouTube y destinos de soporte quedan por configurar antes de activarlos. Licencias adoptadas en NOTICE.md.
No bloquean la programación del núcleo: la UI ofrece manual y estado no configurado, sin URL ficticia.

- [Estados y pendientes parciales](tecnica/ESTADOS-Y-PENDIENTES.md): regla transversal incorporada a todos los circuitos. [Guía de lectura y ejemplos](usuario/ESTADOS-DOCUMENTALES.md).

- [Guía de gestión ARG](usuario/GUIA-GESTION.md) y [registro de instalación](entregas/INSTALACION-DEMO.md).

Guías de Ventas: [usuario](usuario/006-ventas.md), [técnica](tecnica/006-ventas.md), [entrega parcial](entregas/006-ventas.md).

Guías de Compras: [usuario](usuario/007-compras.md), [técnica](tecnica/007-compras.md), [entrega parcial](entregas/007-compras.md).

Guías Stock: [usuario](usuario/008-stock.md), [técnica](tecnica/008-stock.md), [entrega](entregas/008-stock.md).

Guías Administración: [usuario](usuario/009-administracion.md), [técnica](tecnica/009-administracion.md), [entrega](entregas/009-administracion.md).

Guías Informes: [usuario](usuario/010-informes.md), [técnica](tecnica/010-informes.md), [entrega](entregas/010-informes.md).

Portada y comunidad: [sitio documental](site/README.md), [usuario](usuario/011-web-comunidad.md), [técnica](tecnica/011-web-comunidad.md), [entrega](entregas/011-web-comunidad.md).

Cierre: [correcciones contractuales](entregas/CIERRE-DE-CONTRATOS.md) y [cobertura de requisitos](entregas/COBERTURA-REQUISITOS.md).

## Expansión argentina

[Plan completo](PLAN-EXPANSION-ARG.md):22 capacidades, etapas E0–E7 y specs016–024. Principios
de carga básica y recibo argentino confirmados. Implementación/instalación/QA se registran por entrega.

Valores ARG: [manual inicial](usuario/017-cartera-valores.md),
[entrega REC/cheques](entregas/017-rec-cheques.md) y [tareas financieras pendientes](../specs/017-cartera-valores/tasks.md).
REC con cheques en papel está instalado sólo en aislado; no modifica recibos ni saldos de la demo.

[OPA, reservas y cheques propios1.2](entregas/017-opa-cheques.md): código preparado,
autenticación e instalación pendientes; no habilitado aún en demo.
