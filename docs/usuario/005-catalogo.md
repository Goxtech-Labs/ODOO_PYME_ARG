# Catálogo y precios ARG

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Crear un producto o servicio con nombre, tipo, código textual, unidad y precio base. El código conserva ceros iniciales.
Costo y precio son datos distintos con moneda identificada; la ficha avanzada conserva todas las funciones nativas.
Las categorías y los atributos son opcionales. No se exige talle, color, depósito ni lote desde Catálogo.

En Ventas → Precios, elegir hasta cinco listas por consulta. Filtrar por código/nombre, tipo, categoría, venta y compra; paginar de treinta productos. Cada columna indica moneda y cada fila su unidad. Cantidad y fecha controlan la consulta nativa.
Los cambios quedan pendientes al filtrar, paginar u ocultar columnas. Revisar y guardar presenta todos los cambios, incluso los ocultos, con precio anterior/nuevo. Descartar pide confirmación. Salir con cambios ofrece continuar o descartarlos.

La edición simplificada sirve para una unidad, hoy, con precio fijo de variante sin vigencia/cantidad especial, o sin regla. Las reglas avanzadas se consultan y editan en Listas y reglas; no se reemplazan silenciosamente.
El margen mostrado corresponde al precio guardado de consulta, después de convertir costo a la moneda de la columna con la fecha elegida. No es rentabilidad contable ni margen de los precios pendientes.
Si otro usuario cambia catálogo o lista, se rechaza el lote completo: revisar, descartar y recargar antes de intentar de nuevo. No se guarda parcialmente ni se modifica stock.
El responsable puede aplicar precios; el operador consulta. Guía escrita disponible; tutorial YouTube pendiente de publicación.

## Matriz de variantes · incremento en desarrollo

Catálogo1.1.0 y adaptador Stock1.0.6 están instalados técnicamente en aislado; promoción a demo y QA
pendientes. El lock de la demo conserva la entrega pública previa.

Desde la ficha elegí **Variantes**, o Stock → Variantes. Buscá y elegí el producto. Los atributos son
los del catálogo; talle/color son ejemplos opcionales. La consulta propone hasta dos ejes y muestra
los demás como filtros de valor corregibles. Se pueden cambiar o quitar los ejes.

Cada página muestra hasta8 columnas y15 filas. Los valores de filtros se buscan de30 en30. No se
cargan todas las variantes ni se crean combinaciones. Una celda puede indicar exclusión nativa, una
variante visible o una variante no determinada: la ausencia visible puede deberse a permisos, archivo
o una variante dinámica aún no generada. No significa existencia cero.

**Abrir ficha** usa el producto nativo. Con Stock ARG y permiso efectivo, existencia y libre se leen
en la unidad de cada producto para el alcance nativo visible de la compañía actual. Sin permiso se
informa no determinado; sin Stock ARG, no disponible. Servicios y productos no almacenables no
presentan existencias. No se suman unidades distintas ni se cambian cantidades desde esta pantalla.

**Precios** abre la matriz existente filtrada por este producto; conserva sus reglas, moneda, guardado
y controles de concurrencia. No reemplaza tarifas ni copia precios a otro catálogo.

Seleccioná hasta200 variantes para **Preparar etiquetas**. La selección se conserva al filtrar o
paginar y se puede revisar/quitar en su sección. Cambiar producto pide confirmar su descarte. Al
abrir etiquetas se revalidan compañía, permisos, actividad y configuración. El asistente nativo permite
revisar formato, copias y precio antes de imprimir; abrirlo no imprime. Los servicios conservan la
restricción nativa de etiquetas. Modelos ampliados/importación F17/F22 siguen pendientes.
