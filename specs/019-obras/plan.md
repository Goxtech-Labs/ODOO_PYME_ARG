# Implementation Plan: Obras, capítulos y costos ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-05 | **Spec**: [spec.md](spec.md)

## Summary

Crear obra con cliente, nombre y fecha; agregar capítulos cuando hagan falta. Costos reales desde compras, consumos y horas nativos; distinguir comprometido, devengado y pagado. No sumar dos veces compra y consumo del mismo material.
Orden global y dependencias en [expansión argentina](../../docs/PLAN-EXPANSION-ARG.md).

## Technical Context

**Language/Version**: Python3.12, Odoo20 Community, OWL/XML/SCSS compatibles con revisión instalada.
**Primary Dependencies**: arg_pyme_compras, arg_pyme_ventas, arg_pyme_stock, arg_pyme_documentos. Nativas: project, analytic y hr_timesheet candidatos; tiempos optativos, sin imponer RRHH completo.
**Storage**: PostgreSQL/filestore nativos; modelos nuevos sólo para hechos sin equivalente.
**Testing**: controles técnicos de sintaxis/manifest/instalación/arranque; quickstart posterior para QA autorizada.
**Target Platform**: LXC/Linux propio y navegador, sin Enterprise obligatorio.
**Project Type**: addon opcional; conserva funcionamiento del núcleo sin instalarlo.
**Performance Goals**: consultas paginadas; selección parcial y concurrencia controlada; medir antes de fijar SLA.
**Constraints**: no core modificado, no ledger paralelo, no envíos/fiscal por instalar.
**Scale/Scope**: micropymes/pymes, roles combinables y gestión documental de carga mínima.

## Constitution Check

Antes y después del diseño: gratuidad/soberanía, identidad ARG, núcleo sin dependencias hacia esta extensión,
fuentes nativas e integraciones centralizadas cumplen el contrato. Versionar composición; no afirmar
disponibilidad/licencia de un candidato sin inspección. QA/aceptación y activación externas son hitos separados.

## Project Structure

Documentación: spec.md, research.md, data-model.md, contracts/operaciones.md, quickstart.md y tasks.md.
Código propuesto: `addons/arg_pyme_obras/`, con models/, views/, security/, data/ y manual asociado.
Componentes previstos: `models/work.py`, `models/work_chapter.py`, `models/material_part.py`, `models/labor_part.py`, `views/work_views.xml`.

## Decisiones de implementación

- No copiar módulos de otros clientes; evaluar el candidato nativo contra esta composición exacta.
- Mantener operaciones comerciales/físicas/contables en sus motores y extender mediante relaciones.
- Código interno propuesto: OBR / PMA / PMO propuestos; comprobar unicidad con el registro documental antes de incorporarlo.
- Persistencia y transiciones en servidor; botones delegan callbacks nativos y guardas de salida.
- Costos reales desde compras, consumos y horas nativos; distinguir comprometido, devengado y pagado. No sumar dos veces compra y consumo del mismo material.

## Entrega y dependencias

Cerrar contrato/identidad → US1 carga → US2 efectos → US3 consulta → documentación/composición → instalación
controlada → QA posterior → aceptación. No iniciar todos los módulos simultáneamente.
Respaldo consistente y código fijado antes de cada promoción; no restaurar datos perdiendo escrituras nuevas.

## Complexity Tracking

No hay excepción aprobada a la constitución. Una incompatibilidad de hooks, licencia o API detiene sólo
la promoción del componente afectado y se registra; no se elude con sudo ni con copia de Enterprise.
