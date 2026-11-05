# Implementation Plan: Expansión argentina coordinada

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-05 | **Spec**: [spec.md](spec.md)

## Summary

Implementar F01–F22 de [PLAN-EXPANSION-ARG.md](../../docs/PLAN-EXPANSION-ARG.md), por etapas E0–E7.
Esta feature coordina; cada addon nuevo tiene spec/plan/tareas 017–024. Los incrementos del núcleo
siguen en sus módulos originales. No instalar un módulo coordinador ni duplicar tareas de los hijos.

## Technical Context

**Language/Version**: Odoo20 Community/Python3.12/PostgreSQL16; revisión/composición real a releer.
**Primary Dependencies**: doce addons ARG existentes; opcionales sólo al promover cada extensión.
**Storage**: contabilidad/stock nativos y eventos de dominio; filestore para evidencia/documentos.
**Testing**: sintaxis/manifest/vistas e instalación/arranque durante entrega; QA funcional/visual posterior.
**Target Platform**: LXC Linux, homelab/VPS, navegador; conectores optativos.
**Project Type**: programa modular, no monolito nuevo.
**Performance Goals**: paginación/consulta parcial y bloqueos por operación; medir sin SLA inventado.
**Constraints**: no core editado, no Enterprise obligatorio, no dependencias núcleo→rubro, no doble libro.
**Scale/Scope**: micropymes/pymes con roles combinados,22 capacidades y8 nuevos addons de gestión.

## Constitution Check

Revisión previa y posterior:1.4.0 conserva soberanía/gratuidad; procesos locales y carga mínima explícitos;
PRE/PED y efectos separados; proveedores en addon único; módulos opcionales sin ciclo; licencias originales
y de terceros preservadas. Sin excepción al contrato. Aplicación en runtime todavía debe demostrarse.

## Project Structure

- docs/PLAN-EXPANSION-ARG.md: alcance22 capacidades, etapas y decisiones del titular.
- specs/016-expansion-argentina/: coordinación, fuentes, contratos, pruebas posteriores y tareas.
- specs/017-cartera-valores/ a specs/024-punto-venta/: diseño/tareas de cada nuevo addon.
- addons/arg_pyme_{base,ui,terceros,catalogo,ventas,compras,stock,administracion,informes,documentos}: incrementos del núcleo.
- addons/arg_pyme_integraciones: único destino de conectores; contratos012/013 preservados.
- Nuevos addons: valores, reparaciones, obras, fabricacion, comisiones, servicios, disenador, pos.

## Decisiones técnicas y secuencia

E0 inventario/contratos → E1 carga y bases → E2 valores/REC-OPA → E3 reparaciones → E4 obras/fabricación
→ E5 comisiones/servicios → E6 POS/diseñador → E7 canales. E2 puede desarrollarse tras E0 sin esperar
todo E1 si conserva los mismos contratos y archivos; no promover sin composición completa del incremento.
No paralelizar escrituras de motores compartidos. Research delegada sólo lectura; revisión del diff
final es independiente de implementación, con límites de misma familia/cuenta declarados.

Cartera: revisar treasury_document, treasury_native, money_application y protecciones nativas como un
contrato único antes de habilitar cheques. Stock: hooks de quants/moves afectan repair/mrp/POS.
Comercial: guardas de PED deben admitir generadores internos autorizados sin flags falsificables.
Integraciones: outbox/lookup/idempotencia, secretos externos, capacidades de proveedor explícitas.

## Entrega

Fijar composición/hash, hacer respaldo consistente y actualizaciones explícitas; no -u all ni rollback
con pérdida de datos. Desplegar incrementos autorizados y registrar QA pendiente. Ejemplos sin efectos
operativos en demo compartida; fixtures que mueven/contabilizan sólo en entorno aislado y etapa acordada.
Importación de datos reales y activación de canales son tareas separadas.

## Complexity Tracking

No se autoriza nuevo ledger, duplicación de menú ni un addon por proveedor. Las dependencias opcionales
se revisan por entrega. La lista de candidatos no acredita código/licencia compatible ni instalación.
