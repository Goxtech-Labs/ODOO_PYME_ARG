# Implementation Plan: Extensiones por rubro y personalizaciones ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Proceso y contrato para agregar rubros sin imponer reglas sectoriales al núcleo genérico.

## Summary

Aplicar los contratos comunes y los recorridos específicos sin duplicar fuentes operativas.
Conservar interfaz simple para personal no especializado y capacidades avanzadas progresivas.

## Technical Context

**Language/Version**: Markdown, JSON y SVG originales; contratos compatibles con Odoo 20 Community.
**Primary Dependencies**: `nucleo_ARG`.
**Storage**: Archivos versionados; ninguna base nueva ni secretos en el repositorio.
**Testing**: Enlaces, esquema documental, coherencia de estados y revisión de contenido.
**Target Platform**: Repositorio y lector Markdown/navegador.
**Project Type**: Entrega documental; no addon instalable.
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

Objetivo técnico: `docs/rubros`.
Rutas propuestas a crear durante implementación:

- `docs/rubros/plantillas/spec-rubro.md`
- `docs/rubros/plantillas/alcance.md`
- `docs/rubros/plantillas/composicion.md`
- `docs/rubros/plantillas/compatibilidad.md`
- `docs/rubros/plantillas/entrega.md`
- `docs/rubros/plantillas/tutorial.md`

**Structure Decision**: Mantener una responsabilidad por addon; conservar origen y trazabilidad nativos.

## Decisiones específicas

- Definir una plantilla y una regla de composición antes de elegir el primer rubro.
- Mantener núcleo genérico modular; no inventar reglas comerciales de clientes.

## Entrega y orden

Completar dependencias del catálogo antes de programar este módulo.
Aplicar las tareas por historia, en secuencia; revisar el contrato antes de cambiar una interfaz compartida.
Registrar manifest, sintaxis, carga de vistas, instalación/upgrade y arranque como controles técnicos.
Actualizar manual, tutoriales por versión y estado de entrega. Realizar QA funcional/visual posteriormente.

## Complexity Tracking

No incorporar motores, servicios ni tablas paralelas para funciones ya provistas por la fuente nativa.
Justificar toda extensión adicional mediante una decisión documentada en esta feature.
