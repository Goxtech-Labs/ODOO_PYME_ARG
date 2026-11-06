# Matriz de variantes ARG

Producto/servicio único nativo: plantilla y product.product. Los atributos son opcionales y genéricos;
talle/color son ejemplos, no campos obligatorios. No se crea otro catálogo, stock ni precio.

## Consulta

Elegir plantilla propone los dos primeros atributos que generan variantes como columnas/filas.
Se pueden cambiar o quitar ejes. Los atributos restantes proponen un valor activo visible, mostrado
como filtro corregible. Los valores de cada eje y sus búsquedas se consultan por páginas; no se
devuelve el producto cartesiano completo. Página de hasta8 columnas por15 filas; búsquedas de valores30.
Una plantilla sin atributos conserva una celda de producto y no necesita crear atributos.

El servidor valida plantilla, atributos, valores, compañía actual y permisos. Los valores fijos
pertenecen a la línea de atributo de la plantilla. La consulta usa configuración/exclusiones nativas,
ignora atributos que no generan variantes y sólo busca claves de combinación de la página visible.
No usa el lookup nativo de variante con sudo ni sus fábricas. No genera ni reactiva variantes dinámicas.

Cada celda distingue excluida por configuración, variante activa visible y sin variante activa visible
o aún no generada. Esta última es indeterminada: puede deberse a permisos o configuración, no demuestra
inexistencia ni stock cero. SKU textual, unidad y código de barras proceden del producto nativo.

## Cantidades y acciones

Catálogo funciona sin Stock ARG: cantidades no disponibles. Con Stock ARG y permiso nativo efectivo
se muestran existencia y libre nativas en unidad del producto, compañía actual y alcance de almacenes
nativo, sin filtros de ubicación/fecha/lote/propietario/paquete heredados del llamante. No es una
consulta histórica ni por depósito. Servicios no aplican. Falta de acceso es no determinado, sin sudo.
La matriz no modifica cantidades ni produce movimientos. No totalizar unidades de productos distintos.

La ficha abre el product.product existente con sus permisos normales. Precios abre la matriz existente
filtrada por plantilla, conservando reglas, moneda y controles de edición; no duplica precios.
La selección explícita de hasta200 variantes se conserva al paginar/filtrar y se muestra separada de
la página. Cambiar plantilla pide descartar esa selección. Etiquetas revalida permisos/compañía/actividad
y pertenencia antes de abrir el asistente nativo con las variantes. Formato, copias y precio se revisan
allí; abrirlo no imprime ni ejecuta reportes. Modelos nuevos de etiquetas e importación siguen en F17/F22.

## Entrega

FR-007/008 amplían US3 y parent016T008/F13. F19 conserva pendiente la explicación de condiciones
especiales. Instalación/registro y QA funcional/visual son hitos separados; escenarios se preparan sin
ejecutar recorridos de negocio en desarrollo. No dar por completo el plan de22 capacidades.
