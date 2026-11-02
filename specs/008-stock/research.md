# Research: Circuito Stock ARG

Fecha: 2026-11-01. Separar comportamiento nativo comprobado y decisiones de diseño ARG.

## Decisiones

### D01

**Decision**: Conservar stock.quant y movimientos nativos como única fuente de existencias.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D02

**Decision**: El documento ARG de conteo agrupa decisiones y evidencia; sus efectos se registran en movimientos nativos.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D03

**Decision**: Activación de stock con ventas/compras previas exige previsualizar hooks sale_stock/purchase_stock y respaldo recuperable.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

## Fuentes primarias

- [Fuente oficial 1](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_quant.py)
- [Fuente oficial 2](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_move.py)
- [Fuente oficial 3](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_picking.py)
- [Fuente oficial 4](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/sale_stock/__manifest__.py)
- [Fuente oficial 5](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/purchase_stock/__manifest__.py)

Consultar además [investigación general](../001-pyme-argentina/research.md) y [hallazgos nativos](../../docs/tecnica/DECISIONES-ODOO20.md).
Registrar revisión exacta y dependencias antes de instalar un addon. La existencia de un modelo no acredita cobertura Enterprise.
