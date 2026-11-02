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
