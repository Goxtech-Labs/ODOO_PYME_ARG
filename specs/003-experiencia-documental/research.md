# Research: Experiencia y presentación ARG

Fecha: 2026-11-01. Separar comportamiento nativo comprobado y decisiones de diseño ARG.

## Decisiones

### D01

**Decision**: Extender componentes OWL existentes y menuService; evitar clics simulados y MutationObserver global.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D02

**Decision**: Inventariar OdooBot en nombre, avatar, remitente, onboarding, menciones y traducciones.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D03

**Decision**: Aplicar identidad GOXTECHBOT mediante hook/migración idempotente sobre registros nativos noupdate.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

## Fuentes primarias

- [Fuente oficial 1](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/web/static/src/views/form/form_controller.js)
- [Fuente oficial 2](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/mail_bot/models/mail_bot.py)
- [Fuente oficial 3](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/mail/data/res_partner_data.xml)

Consultar además [investigación general](../001-pyme-argentina/research.md) y [hallazgos nativos](../../docs/tecnica/DECISIONES-ODOO20.md).
Registrar revisión exacta y dependencias antes de instalar un addon. La existencia de un modelo no acredita cobertura Enterprise.
