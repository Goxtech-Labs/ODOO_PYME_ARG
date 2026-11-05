# Implementation Plan: Cartera de valores y tesorería argentina

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-05 | **Spec**: [spec.md](spec.md)

## Summary

Recibir un cheque o registrar uno propio, identificarlo una sola vez y usarlo como medio de REC/OPA. Separar nominal disponible, aplicación de deuda, dinero acreditado/debitado y exposición por recurso. REC/OPA con varios medios usa cuentas transitorias de valores y conciliación nativa, nunca residuales escritos a mano.
Orden global y dependencias en [expansión argentina](../../docs/PLAN-EXPANSION-ARG.md).

## Technical Context

**Language/Version**: Python3.12, Odoo20 Community, OWL/XML/SCSS compatibles con revisión instalada.
**Primary Dependencies**: arg_pyme_administracion, arg_pyme_documentos; account Community transitivo. Adaptador de Informes posterior. l10n_ar_check y account_batch_payment ausentes de esta composición, sin dependencia Enterprise.
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
Código propuesto: `addons/arg_pyme_valores/`, con models/, views/, security/, data/ y manual asociado.
Componentes previstos: `models/value_instrument.py`, `models/value_event.py`, `models/treasury_value.py`, `models/payment_batch.py`, `models/bank_transfer.py`, `models/promissory_note.py`, `views/value_views.xml`.

## Decisiones de implementación

- No copiar módulos de otros clientes; evaluar el candidato nativo contra esta composición exacta.
- Mantener operaciones comerciales/físicas/contables en sus motores y extender mediante relaciones.
- Código interno propuesto: CHQ / VMO / LOP / TRB / PAG propuestos; REC y OPA existentes se conservan; comprobar unicidad con el registro documental antes de incorporarlo.
- Persistencia y transiciones en servidor; botones delegan callbacks nativos y guardas de salida.
- Separar nominal disponible, aplicación de deuda, dinero acreditado/debitado y exposición por recurso. REC/OPA con varios medios usa cuentas transitorias de valores y conciliación nativa, nunca residuales escritos a mano.

## Entrega y dependencias

Cerrar contrato/identidad → US1 carga → US2 efectos → US3 consulta → documentación/composición → instalación
controlada → QA posterior → aceptación. No iniciar todos los módulos simultáneamente.
Respaldo consistente y código fijado antes de cada promoción; no restaurar datos perdiendo escrituras nuevas.

## Complexity Tracking

No hay excepción aprobada a la constitución. Una incompatibilidad de hooks, licencia o API detiene sólo
la promoción del componente afectado y se registra; no se elude con sudo ni con copia de Enterprise.

Contrato financiero específico: [cartera argentina](contracts/cartera-argentina.md). Debe regir modelos,
transiciones, clasificación de money_application y configuración de cuentas antes de admitir cheques.

Incremento de registro instalado técnicamente en aislado, versión20.0.1.0.0. No equivale al MVP de
cartera: US2/US3 y la conexión a REC/OPA siguen abiertas. La composición pública de la demo sigue
fijada por versions.lock.json; el candidato aislado se registra aparte para no atribuirle despliegue live.

## Incremento REC de cheques en papel

Valores20.0.1.1.0, Administración20.0.1.1.3: recepción por REC, depósito sin dinero,
acreditación completa con reclasificación nativa y rechazo previo que conserva otros medios.
[Entrega](../../docs/entregas/017-rec-cheques.md). Código e instalación aislada, sin QA de negocio.
La implementación completa de US2/US3 y promoción del módulo siguen abiertas. No considerar este
circuito restringido una sustitución del alcance ECHEQ/OPA/transmisiones/descuento/parciales.
