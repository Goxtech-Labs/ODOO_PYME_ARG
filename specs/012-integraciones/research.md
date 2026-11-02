# Research: Integraciones ARG

Fecha: 2026-11-01. Separar comportamiento nativo comprobado y decisiones de diseño ARG.

## Decisiones

### D01

**Decision**: Un solo addon y adaptadores internos permiten agrupar servicios sin fragmentar la experiencia.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D02

**Decision**: No instalar dependencias opcionales pesadas hasta elegir proveedor; registrar licencias y versiones.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

## Fuentes primarias

- [Fuente oficial 1](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/odoo/addons/base/models/ir_cron.py)

Consultar además [investigación general](../001-pyme-argentina/research.md) y [hallazgos nativos](../../docs/tecnica/DECISIONES-ODOO20.md).
Registrar revisión exacta y dependencias antes de instalar un addon. La existencia de un modelo no acredita cobertura Enterprise.
