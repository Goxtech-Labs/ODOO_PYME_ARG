# Data model: Catálogo y precios ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Producto | `product.template/product.product` | SKU, nombre, tipo, unidad, categoría, atributos | SKU textual con ceros iniciales conservados |
| Tarifa | `product.pricelist/product.pricelist.item` | moneda, vigencia, reglas por producto y cantidad | No sumar ni mostrar precios de monedas diferentes sin identificación |
| Variante | `product.attribute y valores nativos` | atributos opcionales y combinaciones válidas | No imponer dimensiones de un rubro al núcleo |

## Estados, efectos y seguridad

- No modificar stock físico como efecto de editar catálogo o tarifa.
- Conservar reglas nativas de precio y descuentos configurados.
- No guardar automáticamente al aplicar filtros.
- Evitar enviar todas las imágenes o variantes al navegador.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.

## Registro técnico de precios

arg.pyme.price.change.batch guarda la clave/hash del lote y el antes/después de cada celda para idempotencia y auditoría; no constituye otra tarifa ni fuente de existencias. Único compañía/usuario/operación, inmutable y sin creación directa de usuarios.
