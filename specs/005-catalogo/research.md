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

## D05 · Explicación nativa F19 ·2026-11-06

Se inspeccionan `_get_product_rule` y `_get_product_price_rule` de la composición fijada. La primera
regla aplicable decide el precio; `compute_price` es fixed/discount/markup. Se inspeccionan las
reglas elegidas sin reproducir su aritmética. La lista del cliente procede de la propiedad nativa
en contexto de compañía; no pasar un cliente ficticio al motor ni duplicar listas por consulta.

La consulta independiente conserva un instante exacto mediante DateTimeInput; la matriz existente
consulta su fecha a00:00UTC. El diálogo conserva ese criterio y la cantidad cargada, aunque se hayan
editado filtros sin aplicar. El token de celda permite señalar ciertos cambios desde la carga; no compara toda la cadena de
reglas base. La traza se recalcula con configuración actual y no constituye un snapshot histórico.
Los impuestos se resuelven en el documento: esta consulta no agrega ni separa impuestos y no promete
un importe neto en toda configuración de catálogo. El costo y sus cadenas requieren Responsable ARG.

Fuentes primarias adicionales: [reglas nativas](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/product/models/product_pricelist_item.py),
[propiedad del cliente](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/product/models/res_partner.py) y
[contexto comercial](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/sale/models/sale_order_line.py).
Las verificaciones de archivos seleccionados no prueban igualdad de todo el core ni QA funcional.
