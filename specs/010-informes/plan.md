# Implementation Plan: Circuito Informes ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Informes con hechos, dimensiones, unidades y corte claros para decidir sin conocimientos contables avanzados.

## Summary

Aplicar los contratos comunes y los recorridos específicos sin duplicar fuentes operativas.
Conservar interfaz simple para personal no especializado y capacidades avanzadas progresivas.

## Technical Context

**Language/Version**: Odoo 20 Community; Python 3.12; OWL/XML/SCSS cuando corresponda.
**Primary Dependencies**: `arg_pyme_base`, `arg_pyme_ui`.
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

Objetivo técnico: `addons/arg_pyme_informes`.
Rutas propuestas a crear durante implementación:

- `addons/arg_pyme_informes/report/facts.py`
- `addons/arg_pyme_informes/views/report_menu.xml`
- `addons/arg_pyme_informes/report/dimensions.py`
- `addons/arg_pyme_informes/views/report_filters.xml`
- `addons/arg_pyme_informes/report/export.py`
- `addons/arg_pyme_informes/report/report_templates.xml`

**Structure Decision**: Mantener una responsabilidad por addon; conservar origen y trazabilidad nativos.

## Decisiones específicas

- Reusar account.invoice.report donde su grano coincida; no prometer reportes Enterprise.
- Las aplicaciones de cobro requieren hecho separado de facturación y pagos.
- No crear almacén externo obligatorio; consultas paginadas y vistas SQL cuando justificadas.

## Entrega y orden

Completar dependencias del catálogo antes de programar este módulo.
Aplicar las tareas por historia, en secuencia; revisar el contrato antes de cambiar una interfaz compartida.
Registrar manifest, sintaxis, carga de vistas, instalación/upgrade y arranque como controles técnicos.
Actualizar manual, tutoriales por versión y estado de entrega. Realizar QA funcional/visual posteriormente.

## Complexity Tracking

No incorporar motores, servicios ni tablas paralelas para funciones ya provistas por la fuente nativa.
Justificar toda extensión adicional mediante una decisión documentada en esta feature.

## Diseño concretado para20.0

Consulta transitoria propia arg.pyme.report.query; no almacena hechos ni saldos. Motor abstracto con
adaptadores disponibles según registro y ACL del usuario; no hereda modelos opcionales ni añade sus
módulos a depends. Usa ORM nativo con compañía única, sin sudo ni SQL nuevo. Las consultas de líneas
usan account.move.line directamente para conservar reglas de acceso al origen y moneda documental;
account.invoice.report no se usa donde agregaría conversión/semántica distinta.

La fuente contable y cada documento vinculado verifican lectura de registros y campos antes de mostrar
etiquetas, cantidades o exportar. La consulta tiene dueño y compañía; CSV/PDF vuelven a validar permisos.
Agrupaciones usan IDs para separar nombres duplicados; dinero en moneda única y cantidades por UOM.
Stock a fecha usa quantity_product_uom por extremo interno de compañía, sólo almacenables actuales;
las clasificaciones/unidades/compañías históricas modificadas requieren revisión, no se inventa historia.
Corte y etiquetas comparten la misma zona horaria context tz → user tz → UTC.

Detalle de50filas en navegador; hasta5000registros fuente procesados en servidor para totales/agrupación,
sin truncar. PDF A4 apaisado hasta2000filas; CSV UTF-8 con protección de fórmulas. Cada salida declara
fecha de generación y filtros: vuelve a consultar fuentes vigentes, no guarda una instantánea fiscal.
Deuda es residual actual por vencimiento, nunca residual actual presentado como deuda histórica.
Aplicaciones son conciliaciones vigentes, no dinero. Caja consulta liquidez y excluye transitorios.
