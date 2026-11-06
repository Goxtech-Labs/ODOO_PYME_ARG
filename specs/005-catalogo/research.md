# Research: Catálogo y precios ARG

Fecha: 2026-11-01. Separar comportamiento nativo comprobado y decisiones de diseño ARG.

## Decisiones

### D01

**Decision**: Reutilizar producto/servicio y precios nativos; verificar campos de tipo y almacenamiento contra la rama fijada.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D02

**Decision**: Mantener edición masiva acotada con revisión y control de concurrencia.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D03

**Decision**: Agregar talle/color en módulos especializados posteriores, no como columnas obligatorias del núcleo.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

## Fuentes primarias

- [Fuente oficial 1](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/product/models/product_template.py)
- [Fuente oficial 2](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/product/models/product_product.py)
- [Fuente oficial 3](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/product/models/product_pricelist.py)

Consultar además [investigación general](../001-pyme-argentina/research.md) y [hallazgos nativos](../../docs/tecnica/DECISIONES-ODOO20.md).
Registrar revisión exacta y dependencias antes de instalar un addon. La existencia de un modelo no acredita cobertura Enterprise.

## D04 · Variantes paginadas ·2026-11-06

Se inspeccionaron cinco archivos product en la revisión fijada y se contrastaron hashes con el runtime.
La regla de configuración/exclusión admite consulta sin fábricas. El lookup nativo de variante usa
sudo y se evita: se buscan claves `combination_indices` sólo de la página visible. `product_matrix`
arma el cartesiano completo y agrega account como dependencia; no se incorpora ese comportamiento.
Se conserva la acción nativa de etiquetas y su rechazo de servicios. Producto/Stock nativos siguen
siendo las únicas fuentes. [Contrato](contracts/matriz-variantes.md).
