# Implementation Plan: Circuito Stock ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Consultar existencias y operar entradas, salidas, transferencias, inventarios y ajustes con trazabilidad nativa.

## Summary

Aplicar los contratos comunes y los recorridos específicos sin duplicar fuentes operativas.
Conservar interfaz simple para personal no especializado y capacidades avanzadas progresivas.

## Technical Context

**Language/Version**: Odoo 20 Community; Python 3.12; OWL/XML/SCSS cuando corresponda.
**Primary Dependencies**: `arg_pyme_base`, `arg_pyme_ui`, `arg_pyme_catalogo`, `arg_pyme_documentos`, `stock`.
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

Objetivo técnico: `addons/arg_pyme_stock`.
Rutas propuestas a crear durante implementación:

- `addons/arg_pyme_stock/models/stock_quant.py`
- `addons/arg_pyme_stock/views/stock_matrix_views.xml`
- `addons/arg_pyme_stock/models/stock_picking.py`
- `addons/arg_pyme_stock/views/stock_picking_views.xml`
- `addons/arg_pyme_stock/models/inventory_count.py`
- `addons/arg_pyme_stock/views/inventory_count_views.xml`

**Structure Decision**: Mantener una responsabilidad por addon; conservar origen y trazabilidad nativos.

## Decisiones específicas

- Conservar stock.quant y movimientos nativos como única fuente de existencias.
- El documento ARG de conteo agrupa decisiones y evidencia; sus efectos se registran en movimientos nativos.
- Activación de stock con ventas/compras previas exige previsualizar hooks sale_stock/purchase_stock y respaldo recuperable.

## Entrega y orden

Completar dependencias del catálogo antes de programar este módulo.
Aplicar las tareas por historia, en secuencia; revisar el contrato antes de cambiar una interfaz compartida.
Registrar manifest, sintaxis, carga de vistas, instalación/upgrade y arranque como controles técnicos.
Actualizar manual, tutoriales por versión y estado de entrega. Realizar QA funcional/visual posteriormente.

## Complexity Tracking

No incorporar motores, servicios ni tablas paralelas para funciones ya provistas por la fuente nativa.
Justificar toda extensión adicional mediante una decisión documentada en esta feature.

## Incremento F14 ·2026-11-06

Servicio abstracto models/traceability.py para selectores/páginas/acciones y asistente transitorio
models/lot_create.py para alta mínima. OWL estático traceability.js/xml, DateTimeInput nativo para
filtros opcionales y estado local al volver de maestros. Modelos de stock nativos son las fuentes.
No usar stock.lot.location_id editable: su inverse mueve quants; ni action_lot_open_transfers como
historia completa, porque esa acción sólo muestra entregas. Usar acción nativa de trazabilidad para
la exploración avanzada. [Contrato](contracts/trazabilidad-series-lotes.md).

Interfaz simplificada paginada; stock.move.line conserva hechos y quantity_product_uom en unidad
base. Asistente de alta no invoca ajustes ni validaciones. Concurrencia mediante fila del asistente
y lock técnico de producto existente; no sudo de negocio. Native core conserva validación de lotes.
Versión nueva de Stock por capacidad; no cambiar Catálogo ni los puentes. F15 se diseña por separado.

La extensión de stock.lot en models/lot_create.py toma el mismo lock técnico para altas y cambios
de identidad de todos los orígenes; exige permisos nativos antes del lock y conserva super().
Así la garantía no depende de que todos usen el asistente ARG. Afecta el maestro nativo consumido
por Stock y POS/otros módulos instalados; no cambiar su semántica ni exigir roles ARG globalmente.
Total y quants comparten el dominio nativo de ubicaciones, sin incluir almacenes externos al total.

Comprobación técnica de roles halló que stock.group_production_lot no estaba activo en usuarios
ARG de demo. Patch Stock1.1.1 agrega ese implied_id a Stock ARG, sin activar tracking por producto.
Campos lot_id/lot_name de stock_move y picking están condicionados por ese grupo nativo.
