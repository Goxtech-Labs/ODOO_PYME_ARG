# Research: Circuito Ventas ARG

Fecha: 2026-11-01. Separar comportamiento nativo comprobado y decisiones de diseño ARG.

## Decisiones

### D01

**Decision**: El usuario exige documentos diferentes: crear arg.pyme.quotation, no dos vistas del mismo sale.order.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D02

**Decision**: Odoo confirma su presupuesto nativo cambiando el mismo sale.order; ARG sólo usa sale.order para el pedido generado.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D03

**Decision**: Mantener referencia del presupuesto por cabecera y línea; preservar snapshot de revisiones como historia, no como sustituto del documento propio.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D04

**Decision**: Instalar puentes stock solamente con previsualización de pedidos abiertos y respaldo, debido a hooks nativos.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

## Fuentes primarias

- [Fuente oficial 1](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/sale/models/sale_order.py)
- [Fuente oficial 2](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/sale/models/sale_order_line.py)
- [Fuente oficial 3](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/sale_stock/models/sale_order_line.py)
- [Fuente oficial 4](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/sale_stock/__init__.py)

Consultar además [investigación general](../001-pyme-argentina/research.md) y [hallazgos nativos](../../docs/tecnica/DECISIONES-ODOO20.md).
Registrar revisión exacta y dependencias antes de instalar un addon. La existencia de un modelo no acredita cobertura Enterprise.
