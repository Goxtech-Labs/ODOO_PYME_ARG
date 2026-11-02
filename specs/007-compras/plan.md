# Implementation Plan: Circuito Compras ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Pedido a proveedor, entrada, factura recibida y devolución separados, con mínima carga y documentos vinculados.

## Summary

Aplicar los contratos comunes y los recorridos específicos sin duplicar fuentes operativas.
Conservar interfaz simple para personal no especializado y capacidades avanzadas progresivas.

## Technical Context

**Language/Version**: Odoo 20 Community; Python 3.12; OWL/XML/SCSS cuando corresponda.
**Primary Dependencies**: `arg_pyme_base`, `arg_pyme_ui`, `arg_pyme_terceros`, `arg_pyme_catalogo`, `arg_pyme_documentos`, `purchase`.
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

Objetivo técnico: `addons/arg_pyme_compras`.
Rutas propuestas a crear durante implementación:

- `addons/arg_pyme_compras/models/purchase_order.py`
- `addons/arg_pyme_compras/views/purchase_order_views.xml`
- `addons/arg_pyme_compras/models/purchase_receipt.py`
- `addons/arg_pyme_compras/views/purchase_receipt_views.xml`
- `addons/arg_pyme_compras/models/purchase_return.py`
- `addons/arg_pyme_compras/views/purchase_return_views.xml`

**Structure Decision**: Mantener una responsabilidad por addon; conservar origen y trazabilidad nativos.

## Decisiones específicas

- Extender purchase.order y conservar confirmación/aprobación nativas; no crear otra tabla de compras operativas.
- purchase_stock crea transferencias y puede modificar pedidos abiertos al instalarse; tratar activación como migración controlada.
- Permitir factura recibida directa según permisos, identificando que no procede de un pedido.

## Entrega y orden

Completar dependencias del catálogo antes de programar este módulo.
Aplicar las tareas por historia, en secuencia; revisar el contrato antes de cambiar una interfaz compartida.
Registrar manifest, sintaxis, carga de vistas, instalación/upgrade y arranque como controles técnicos.
Actualizar manual, tutoriales por versión y estado de entrega. Realizar QA funcional/visual posteriormente.

## Complexity Tracking

No incorporar motores, servicios ni tablas paralelas para funciones ya provistas por la fuente nativa.
Justificar toda extensión adicional mediante una decisión documentada en esta feature.

Propiedad de stock: addon puente arg_pyme_compras_stock según docs/tecnica/DECISIONES-ODOO20.md. Las rutas de recepción/entrega propuestas aquí se ubican en ese puente; el addon principal no hereda modelos stock ausentes.
