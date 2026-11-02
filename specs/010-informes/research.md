# Research: Circuito Informes ARG

Fecha: 2026-11-01. Separar comportamiento nativo comprobado y decisiones de diseño ARG.

## Decisiones

### D01

**Decision**: Reusar account.invoice.report donde su grano coincida; no prometer reportes Enterprise.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D02

**Decision**: Las aplicaciones de cobro requieren hecho separado de facturación y pagos.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D03

**Decision**: No crear almacén externo obligatorio; consultas paginadas y vistas SQL cuando justificadas.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

## Fuentes primarias

- [Fuente oficial 1](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/account/report/account_invoice_report.py)
- [Fuente oficial 2](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/account/models/account_move_line.py)
- [Fuente oficial 3](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/stock/models/stock_move.py)

Consultar además [investigación general](../001-pyme-argentina/research.md) y [hallazgos nativos](../../docs/tecnica/DECISIONES-ODOO20.md).
Registrar revisión exacta y dependencias antes de instalar un addon. La existencia de un modelo no acredita cobertura Enterprise.

## Evidencia del runtime instalado20.0.20261101

- stock.move.line usa uom_id/quantity_product_uom; stock nativo sólo modifica quants si product.is_storable.
  Reconstrucción usa quantity_product_uom y product.uom_id; no sumar una docena con unidades sin normalizar.
- ir.access CSV20 usa model_id técnico, operation/domain. ir.actions.report no tiene report_file.
- odoo.http ya no exporta content_disposition; descarga usa nombre de archivo fijo y cabecera attachment.
- router20 reconoce /odoo/<modelo con punto>/<id>, usado para navegación a fuente con permisos nativos.
- context_timestamp prioriza context tz; filtros UTC y metadatos usan la misma zona efectiva.
- Fuentes primarias instaladas: addons/stock/models/stock_move_line.py, stock/models/product.py,
  web/static/src/core/browser/router.js y modelos account/purchase capturados por hash de paquete.
