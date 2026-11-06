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

## Consulta de variantes1.1

`arg.pyme.variant.matrix` es abstracto, sin persistencia: plantilla y líneas/PTAV nativas definen ejes
y filtros; `product.product.combination_indices` resuelve sólo la página visible. Cada celda distingue
configuración excluida, variante activa visible y variante no determinada. La selección del navegador
contiene IDs explícitos, no un catálogo paralelo, y se revalida antes de acciones. El adaptador opcional
de Stock agrega lecturas actuales por unidad/compañía y permiso, sin saldos ni escrituras nuevas.

## Consulta y explicación F19 · incremento1.2

`arg.pyme.price.consultation` es abstracto: no almacena consultas ni nuevas tarifas. Entradas: variante
nativa, cantidad positiva, instante UTC o fecha de matriz, lista y cliente opcionales. Respuesta:
compañía/unidad/moneda/momento, precio nativo o no determinado, condiciones actuales y traza acotada.
Cada paso identifica lista, regla ganadora y parámetros permitidos. Cadena con base de costo oculta
la traza a no Responsables; no se devuelve costo ni margen restringido. Los valores calculados no se
restauran desde el estado del navegador: cada nueva consulta revalida fuentes/permisos.
La lista manual es estado de selección, no una asignación al cliente. Las condiciones de pago/notas
son opcionales según campos instalados y permisos. Los documentos anteriores no se actualizan.
