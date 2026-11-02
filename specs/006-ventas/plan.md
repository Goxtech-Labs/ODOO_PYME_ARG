# Implementation Plan: Circuito Ventas ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Presupuesto propio PRE, pedido cliente PED independiente, entregas y facturas vinculadas sin duplicar efectos nativos.

## Summary

Aplicar los contratos comunes y los recorridos específicos sin duplicar fuentes operativas.
Conservar interfaz simple para personal no especializado y capacidades avanzadas progresivas.

## Technical Context

**Language/Version**: Odoo 20 Community; Python 3.12; OWL/XML/SCSS cuando corresponda.
**Primary Dependencies**: `arg_pyme_base`, `arg_pyme_ui`, `arg_pyme_terceros`, `arg_pyme_catalogo`, `arg_pyme_documentos`, `sale_management`.
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

Objetivo técnico: `addons/arg_pyme_ventas`.
Rutas propuestas a crear durante implementación:

- `addons/arg_pyme_ventas/models/quotation.py`
- `addons/arg_pyme_ventas/views/quotation_views.xml`
- `addons/arg_pyme_ventas/models/sale_order.py`
- `addons/arg_pyme_ventas/views/sale_order_views.xml`
- `addons/arg_pyme_ventas/models/account_move.py`
- `addons/arg_pyme_ventas/views/sale_document_links.xml`

**Structure Decision**: Mantener una responsabilidad por addon; conservar origen y trazabilidad nativos.

## Decisiones específicas

- El usuario exige documentos diferentes: crear arg.pyme.quotation, no dos vistas del mismo sale.order.
- Odoo confirma su presupuesto nativo cambiando el mismo sale.order; ARG sólo usa sale.order para el pedido generado.
- Mantener referencia del presupuesto por cabecera y línea; preservar snapshot de revisiones como historia, no como sustituto del documento propio.
- Instalar puentes stock solamente con previsualización de pedidos abiertos y respaldo, debido a hooks nativos.

## Entrega y orden

Completar dependencias del catálogo antes de programar este módulo.
Aplicar las tareas por historia, en secuencia; revisar el contrato antes de cambiar una interfaz compartida.
Registrar manifest, sintaxis, carga de vistas, instalación/upgrade y arranque como controles técnicos.
Actualizar manual, tutoriales por versión y estado de entrega. Realizar QA funcional/visual posteriormente.

## Complexity Tracking

No incorporar motores, servicios ni tablas paralelas para funciones ya provistas por la fuente nativa.
Justificar toda extensión adicional mediante una decisión documentada en esta feature.

Propiedad de stock: addon puente arg_pyme_ventas_stock según docs/tecnica/DECISIONES-ODOO20.md. Las rutas de recepción/entrega propuestas aquí se ubican en ese puente; el addon principal no hereda modelos stock ausentes.
