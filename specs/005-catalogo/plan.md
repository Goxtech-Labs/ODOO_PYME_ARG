# Implementation Plan: Catálogo y precios ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Gestionar productos y servicios genéricos, listas de precios y atributos opcionales mediante fichas y matrices simples.

## Summary

Aplicar los contratos comunes y los recorridos específicos sin duplicar fuentes operativas.
Conservar interfaz simple para personal no especializado y capacidades avanzadas progresivas.

## Technical Context

**Language/Version**: Odoo 20 Community; Python 3.12; OWL/XML/SCSS cuando corresponda.
**Primary Dependencies**: `arg_pyme_base`, `arg_pyme_ui`, `product`.
**Storage**: PostgreSQL 16 y filestore nativos; configuración y secretos fuera del repositorio.
**Testing**: Controles técnicos de instalación/upgrade; escenarios de aceptación reservados para QA posterior.
**Target Platform**: Linux propio/homelab/VPS y navegador; entorno de ejemplo demo.
**Project Type**: Addon Odoo o incremento documental/de proveedor según alcance.
**Performance Goals**: Mantener paginación en servidor y evitar carga completa de catálogos en navegador.
**Constraints**: No modificar core ni exigir Enterprise; no ejecutar operaciones externas reales en ejemplos.
**Scale/Scope**: Micropymes y pymes; roles combinables, 100 líneas de documento como escenario inicial.

## Constitution Check

| Regla | Decisión de diseño |
| --- | --- |
| Gratuidad y soberanía | Código/documentación abiertos; instalación y datos bajo control de la pyme |
| Módulos propios | Extender modelos nativos y justificar modelos nuevos en data-model.md |
| Simplicidad | Datos mínimos, orden común y roles combinables |
| Identidad | ARG como producto; GOXTECHBOT como excepción suave; autoría Gonzalo Sarubilo |
| Etapas | Programar por tareas; diferir QA funcional y registrar instalación por separado |
| Integraciones | Mantener proveedores externos dentro de un único módulo Integraciones ARG |

Revisión antes y después del diseño: compatible por contrato; no acredita funcionamiento instalado.

## Project Structure

### Documentation (this feature)

spec.md, plan.md, research.md, data-model.md, contracts/operaciones.md, quickstart.md, tasks.md y checklists/requirements.md.

### Source Code (repository root)

Objetivo técnico: `addons/arg_pyme_catalogo`.
Rutas propuestas a crear durante implementación:

- `addons/arg_pyme_catalogo/models/product_template.py`
- `addons/arg_pyme_catalogo/views/product_template_views.xml`
- `addons/arg_pyme_catalogo/models/pricelist_matrix.py`
- `addons/arg_pyme_catalogo/views/pricelist_matrix_views.xml`
- `addons/arg_pyme_catalogo/models/product_attributes.py`
- `addons/arg_pyme_catalogo/views/product_attribute_views.xml`

**Structure Decision**: Mantener una responsabilidad por addon; conservar origen y trazabilidad nativos.

## Decisiones específicas

- Reutilizar producto/servicio y precios nativos; verificar campos de tipo y almacenamiento contra la rama fijada.
- Mantener edición masiva acotada con revisión y control de concurrencia.
- Agregar talle/color en módulos especializados posteriores, no como columnas obligatorias del núcleo.

## Incremento de variantes · 2026-11-06

Ampliar Catálogo con un AbstractModel de consulta paginada sobre plantillas/PTAV/productos nativos,
acción OWL y selector de valores paginado. Stock ARG extiende sólo el adaptador de cantidades, sin
dependencia inversa. Enlazar precios ya implementados con filtro explícito por plantilla y asistente
nativo de etiquetas con selección acotada. Sin persistencia ni fábricas nuevas de variantes.
Contrato: [matriz de variantes](contracts/matriz-variantes.md).

Community `product_matrix` en bb238af6f0ddd70d7ff91521c6104472583661d1 declara LGPL-3 y depende de
account. Su `_get_template_matrix` arma todas las combinaciones sin paginación. No incorporar ese
comportamiento ni dependencia para la consulta ARG; reutilizar sólo reglas de configuración y datos
del catálogo nativo. Cinco archivos nativos de product inspeccionados coinciden SHA256 con el runtime consultado el2026-11-06; no se afirma igualdad de todo el core.

## Entrega y orden

Completar dependencias del catálogo antes de programar este módulo.
Aplicar las tareas por historia, en secuencia; revisar el contrato antes de cambiar una interfaz compartida.
Registrar manifest, sintaxis, carga de vistas, instalación/upgrade y arranque como controles técnicos.
Actualizar manual, tutoriales por versión y estado de entrega. Realizar QA funcional/visual posteriormente.

## Complexity Tracking

No incorporar motores, servicios ni tablas paralelas para funciones ya provistas por la fuente nativa.
Justificar toda extensión adicional mediante una decisión documentada en esta feature.
