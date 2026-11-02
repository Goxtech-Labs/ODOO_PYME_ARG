# Implementation Plan: Experiencia y presentación ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Presentar cinco circuitos, carga mínima, orden constante, componentes comunes, identidad ARG y GOXTECHBOT.

## Summary

Aplicar los contratos comunes y los recorridos específicos sin duplicar fuentes operativas.
Conservar interfaz simple para personal no especializado y capacidades avanzadas progresivas.

## Technical Context

**Language/Version**: Odoo 20 Community; Python 3.12; OWL/XML/SCSS cuando corresponda.
**Primary Dependencies**: `arg_pyme_base`, `web`, `mail_bot`.
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

Objetivo técnico: `addons/arg_pyme_ui`.
Rutas propuestas a crear durante implementación:

- `addons/arg_pyme_ui/static/src/navigation/areas.js`
- `addons/arg_pyme_ui/static/src/navigation/areas.xml`
- `addons/arg_pyme_ui/static/src/components/document_actions.js`
- `addons/arg_pyme_ui/static/src/components/document_matrix.xml`
- `addons/arg_pyme_ui/hooks.py`
- `addons/arg_pyme_ui/views/help_support.xml`

**Structure Decision**: Mantener una responsabilidad por addon; conservar origen y trazabilidad nativos.

## Decisiones específicas

- Extender componentes OWL existentes y menuService; evitar clics simulados y MutationObserver global.
- Inventariar OdooBot en nombre, avatar, remitente, onboarding, menciones y traducciones.
- Aplicar identidad GOXTECHBOT mediante hook/migración idempotente sobre registros nativos noupdate.

## Entrega y orden

Completar dependencias del catálogo antes de programar este módulo.
Aplicar las tareas por historia, en secuencia; revisar el contrato antes de cambiar una interfaz compartida.
Registrar manifest, sintaxis, carga de vistas, instalación/upgrade y arranque como controles técnicos.
Actualizar manual, tutoriales por versión y estado de entrega. Realizar QA funcional/visual posteriormente.

## Complexity Tracking

No incorporar motores, servicios ni tablas paralelas para funciones ya provistas por la fuente nativa.
Justificar toda extensión adicional mediante una decisión documentada en esta feature.
