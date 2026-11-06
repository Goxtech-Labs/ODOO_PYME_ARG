# F19 · Precio y condiciones ARG

## Fuente y captura

Consulta abstracta sin persistencia sobre product.product, product.pricelist/item y res.partner.
Fecha/hora propuesta actual → cliente opcional → variante/cantidad1 → precio. Lista nativa del cliente
propuesta y corregible; una elección manual se conserva al cambiar de cliente hasta pedir usar su
lista. Selectores paginan30 y no descargan maestros enteros. Una plantilla con varias variantes no
se interpreta como un SKU; la elección conserva la variante y unidad efectivas.

La consulta independiente usa datetime nativo UTC, presentado/editado con el widget local de Odoo.
Al explicar una celda existente se conserva la fecha de su matriz (00:00 UTC de esa fecha), cantidad
y lista: no presentar ese valor como vigente ahora ni como precio pendiente de edición. Conservar
fechas/hora explícitas; borrarlas produce validación, no reemplazo silencioso.

## Cálculo y explicación

Reutilizar _cell/_get_product_price_rule y controles de tasas efectivas; no calcular otra tarifa.
Mostrar precio unitario de lista consultado, moneda, unidad, momento exacto de evaluación y
lista. La consulta no agrega ni separa impuestos; éstos se resuelven en el documento según su configuración nativa. El motor nativo decide la primera regla aplicable por su precedencia; no reordenar condiciones.
Explicar tipo fixed/discount/markup, producto/plantilla/categoría/global, mínimo, unidad de regla,
vigencia y redondeo/recargos/límites disponibles. Cadena nativa de otras listas, sin buscar reglas de
otros productos ni copiar precios. La traza es acotada a100 pasos; si excede el límite, señalar traza
parcial sin inventar detalles ni modificar el precio calculado por Odoo.

No devolver costos, márgenes ni parámetros que permitan inferir una base de costo a usuarios sin
rol Responsable ARG. Si una cadena usa costo, su explicación se restringe completa para ese rol,
aunque la venta calculada siga visible por sus permisos normales. Denegación de acceso a reglas o
condiciones se informa como no determinado/restringido; no usar sudo. Falta de tasa efectiva no es0.
Una base nativa de cálculo extendida no contemplada se informa como extensión, sin inventar fórmula.

## Cliente y edición

Lista desde property_product_pricelist nativa, revalidada activa/visible en compañía actual. Nota ARG
y condición de pago sólo si el modelo/campo existe y el usuario puede leerlo; no agregar dependencia
a Contabilidad o Terceros ARG. Diferenciar no disponible, sin condición específica y no determinado.
La consulta no asigna listas ni condiciones. Fichas/reglas se abren con sus acciones/permisos nativos,
y sólo Responsable ARG accede al comando de edición de reglas. Aclarar que la lista puede ser usada
por más clientes y que editarla no reescribe documentos anteriores. Proponer inicio actual sólo al
crear una condición desde esa acción, sin tocar fechas de reglas existentes.

## Seguridad y entrega

Usuario interno/operador, compañía actual, contexto limpio y permisos nativos en cada entrada.
IDs/cantidad/momento validados; no fábrica de variante, escrituras, impuestos, emisión ni pagos.
Conservar matriz y cambios pendientes al abrir explicación en diálogo. Consulta independiente puede
retornar a maestros sin perder sus selecciones; volver a consultar revalida las referencias.

Versionar Catálogo por la nueva capacidad. Fuente, instalación/upgrade, ejemplos, QA y aceptación
son hitos separados. Parent016T008 depende también del cierre de este alcance; conservar F17/F22 y
todo el resto de22 capacidades. No ejecutar recorridos funcionales en esta fase.

## Vigencia de la explicación

La explicación siempre se recalcula con configuración actual para fecha/cantidad cargadas; no
constituye un snapshot histórico de reglas. La comparación usa el token de celda existente
(producto/plantilla/lista/regla superior/unidad/fecha/moneda/precio); no garantiza detectar una
modificación de listas base que mantenga ese token. Informar esa distinción, conservar el buffer
y no presentar la ausencia del aviso como igualdad de todas las condiciones anteriores.
