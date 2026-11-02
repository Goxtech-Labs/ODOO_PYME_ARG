# Implementation Plan: Circuito Administración ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Recibos, órdenes de pago, cajas y cuentas corrientes con imputaciones claras y fuente contable única.

## Summary

Aplicar los contratos comunes y los recorridos específicos sin duplicar fuentes operativas.
Conservar interfaz simple para personal no especializado y capacidades avanzadas progresivas.

## Technical Context

**Language/Version**: Odoo 20 Community; Python 3.12; OWL/XML/SCSS cuando corresponda.
**Primary Dependencies**: `arg_pyme_base`, `arg_pyme_ui`, `arg_pyme_terceros`, `arg_pyme_documentos`, `account`.
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

Objetivo técnico: `addons/arg_pyme_administracion`.
Rutas propuestas a crear durante implementación:

- `addons/arg_pyme_administracion/models/current_account.py`
- `addons/arg_pyme_administracion/views/current_account_views.xml`
- `addons/arg_pyme_administracion/models/treasury_document.py`
- `addons/arg_pyme_administracion/views/treasury_document_views.xml`
- `addons/arg_pyme_administracion/models/cash_report.py`
- `addons/arg_pyme_administracion/views/cash_report_views.xml`

**Structure Decision**: Mantener una responsabilidad por addon; conservar origen y trazabilidad nativos.

## Decisiones específicas

- Un wrapper documental agrupa medios y pagos; account.move.line continúa siendo la fuente del saldo.
- El vínculo invoice_ids puede existir sin conciliación y no acredita cancelación de deuda.
- La primera entrega admite efectivo, transferencia y anticipo registrados; cheques y conciliación bancaria automatizada requieren incremento posterior específico.

## Entrega y orden

Completar dependencias del catálogo antes de programar este módulo.
Aplicar las tareas por historia, en secuencia; revisar el contrato antes de cambiar una interfaz compartida.
Registrar manifest, sintaxis, carga de vistas, instalación/upgrade y arranque como controles técnicos.
Actualizar manual, tutoriales por versión y estado de entrega. Realizar QA funcional/visual posteriormente.

## Complexity Tracking

No incorporar motores, servicios ni tablas paralelas para funciones ya provistas por la fuente nativa.
Justificar toda extensión adicional mediante una decisión documentada en esta feature.

## Ejecución por incrementos

US1 usa account.move.line con campos calculados de presentación, vistas nativas de sólo consulta y
reglas nativas de acceso; no introduce saldo ni tabla alternativa. Incorporar REC/OPA después de entregar
esta dependencia. Conservar todas las tareas de US2/US3, ejes monetarios y auditoría hasta completarlas.
