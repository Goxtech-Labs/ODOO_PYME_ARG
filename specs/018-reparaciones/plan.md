# Implementation Plan: Reparaciones y servicio técnico ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-05 | **Spec**: [spec.md](spec.md)

## Summary

Registrar cliente, equipo y síntoma con fecha de hoy, sin exigir diagnóstico ni técnico al recibir. Consumir/devolver repuestos mediante stock nativo; mano de obra como servicio; facturar desde el documento comercial vinculado sin duplicar pedido ni consumo.
Orden global y dependencias en [expansión argentina](../../docs/PLAN-EXPANSION-ARG.md).

## Technical Context

**Language/Version**: Python3.12, Odoo20 Community, OWL/XML/SCSS compatibles con revisión instalada.
**Primary Dependencies**: arg_pyme_ventas, arg_pyme_stock, arg_pyme_documentos. repair Community inspeccionado; recepción propia sin dependencia de repair, futuros efectos sobre stock/venta nativos; verificar composición exacta.
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
Código propuesto: `addons/arg_pyme_reparaciones/`, con models/, views/, security/, data/ y manual asociado.
Componentes previstos: `models/repair_case.py`, `models/repair_intervention.py`, `models/repair_stock_bridge.py`, `views/repair_views.xml`.

## Decisiones de implementación

- No copiar módulos de otros clientes; evaluar el candidato nativo contra esta composición exacta.
- Mantener operaciones comerciales/físicas/contables en sus motores y extender mediante relaciones.
- Código interno propuesto: REP / PTM propuestos; PRE/PED/REM/FAC existentes; comprobar unicidad con el registro documental antes de incorporarlo.
- Persistencia y transiciones en servidor; botones delegan callbacks nativos y guardas de salida.
- Consumir/devolver repuestos mediante stock nativo; mano de obra como servicio; facturar desde el documento comercial vinculado sin duplicar pedido ni consumo.

## Entrega y dependencias

Cerrar contrato/identidad → US1 carga → US2 efectos → US3 consulta → documentación/composición → instalación
controlada → QA posterior → aceptación. No iniciar todos los módulos simultáneamente.
Respaldo consistente y código fijado antes de cada promoción; no restaurar datos perdiendo escrituras nuevas.

## Complexity Tracking

No hay excepción aprobada a la constitución. Una incompatibilidad de hooks, licencia o API detiene sólo
la promoción del componente afectado y se registra; no se elude con sudo ni con copia de Enterprise.

## Avance de recepción

Primer código opcional20.0.1.0.0: REP, custodia sin inventario propio, diagnóstico y devolución sin
reparar, rol y evidencia. En la fase de fuente estaba sin instalar; el registro se verificó después en aislado.
Decisión de candidato nativo en research.md; no instalar repair
para simular este alcance. El resto de US2/US3 permanece necesario; no cerrar por el subcircuito.

## Ampliación de trabajo1.1

PRE/PED por generadores existentes, autorización propia por PED, partes PTM de servicios manuales,
repuestos exclusivamente por sale_stock y cierre/entrega con ejes nativos. Dependencia explícita
arg_pyme_ventas_stock para enlazar los mismos movimientos comerciales. Archivos adicionales:
repair_commercial.py, repair_sales_bridge.py, repair_intervention.py, repair_stock_bridge.py y
report_adapter.py. Instalación y controles de migración/vistas/registro aislados completados el 2026-11-06.
Contrato [trabajo autorizado](contracts/trabajo-autorizado.md). Correcciones de recepción/diagnóstico,
reportes completos y ejemplos/tutorías continúan; no cerrar018 ni la expansión por esta entrega.

## Fuente de correcciones1.2

repair_correction.py y su wizard implementan rectificación con snapshot, motivo y clave estable;
seguimiento desde custodia terminada prepara REPdraft independiente con vínculo real al anterior.
No reabre custodia ni copia hechos físicos/financieros. Reporte agrega correcciones y ejes existentes,
con degradación de acceso a unknown y conservación de custodia. Mismos nueve estados del caso;
los nuevos hechos extienden su historial. Migración1.2 actualiza ayuda sin reescribir los eventos.
Fuente completa del alcance previsto instalada en aislado; T013 completada y T014 pendiente de promoción.
Ejemplos de borrador/catálogo cargados; ejemplos de circuito/tutoriales, QA y aceptación separados.
[Evidencia actual](../../docs/entregas/EXPANSION-INSTALACION-AISLADA.md). No cerrar el programa completo.
