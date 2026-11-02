# Research: Base ARG

Fecha: 2026-11-01. Separar comportamiento nativo comprobado y decisiones de diseño ARG.

## Decisiones

### D01

**Decision**: Usar ir.sequence por tipo/compañía y preservar identificadores técnicos de registros nativos.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D02

**Decision**: Mantener registro de ayuda y destinos editables sin depender de API YouTube.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D03

**Decision**: Ofrecer operador, responsable y administrador como perfiles componibles, no departamentos obligatorios.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

## Fuentes primarias

- [Fuente oficial 1](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/odoo/addons/base/models/ir_sequence.py)
- [Fuente oficial 2](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/odoo/addons/base/models/res_users.py)
- [Fuente oficial 3](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/odoo/addons/base/models/res_company.py)

Consultar además [investigación general](../001-pyme-argentina/research.md) y [hallazgos nativos](../../docs/tecnica/DECISIONES-ODOO20.md).
Registrar revisión exacta y dependencias antes de instalar un addon. La existencia de un modelo no acredita cobertura Enterprise.
