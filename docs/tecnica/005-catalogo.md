# Catálogo ARG — implementación

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

arg_pyme_catalogo 20.0.1.0.5 depende de Base/UI/product. Productos, categorías, atributos, listas y reglas son modelos nativos.
Matriz arg.pyme.pricelist.matrix abstracta con options/page/apply: ACL y compañía efectivas en servidor, sin sudo de negocio. Paginación30, cinco columnas, metadata hasta200listas/categorías. No se envían imágenes ni catálogo completo.
Odoo20 utiliza compute_price fixed/discount/markup. Se llama _get_product_price_rule con unidad/cantidad/fecha; sólo se editan reglas fijas de variante sin fechas, unidad especial o cantidad mínima. No se eliminan ni sustituyen reglas avanzadas.

Tokens comparan versiones de producto, plantilla, lista, regla, unidad, fecha, moneda y precio. Aplicar actualiza auditoría de listas/productos/plantillas de forma ordenada para serializar transacciones REPEATABLE READ; el retry HTTP obtiene un snapshot nuevo. Los hooks de reglas nativas también actualizan la auditoría de la lista antes de escribir. Comparar tokens contra versiones anteriores a los propios marcadores de serialización. Validar todo antes de escribir cualquier precio.
arg.pyme.price.change.batch conserva usuario/compañía/clave/hash/celdas anteriores/nuevas; inmutable, único por compañía/usuario/operación. Sudo acotado al registro técnico después de autorizar los registros nativos. Reintentar la misma clave y payload devuelve el lote previo; un payload diferente se rechaza. No duplica inventario ni contabilidad.

OWL4 mantiene cambios pendientes fuera de resultados paginados; guardado explícito y aviso de salida. Clave estable de guardado mientras el payload permanezca igual. Edición simple sólo hoy y cantidad1.
Hooks no modifican datos de otros clientes. La única lista inicial adicional se crea cuando existen fixtures arg_demo y conserva moneda real de la compañía.
QA de recorridos, concurrencia, roles, multiempresa y visual se prepara en quickstart, pendiente de ejecución posterior.

OWL4 t-model requiere señales con set; la matriz usa eventos explícitos sobre proxy para controles de consulta.

Versión20.0.1.0.3: valida tasas de reglas/listas base y extras efectivos de reglas fijas. Sin tasa efectiva muestra Sin cotización efectiva y no admite edición de ese resultado; margen desconocido no se inventa.

## Incremento1.1.0 de variantes · instalado en aislado

`arg.pyme.variant.matrix` es un AbstractModel, sin otra tabla de productos/cantidades. Sus métodos
públicos comprueban usuario interno/rol Catálogo y ámbito actual de compañía, limpiando filtros
heredados. `templates`/`values` paginan30; `page` consulta8×15 y busca únicamente las claves
`combination_indices` válidas de esa página. La configuración usa exclusiones nativas, ignorando
atributos no generadores de variante. No usa fábricas ni el lookup de variante con sudo.

Los atributos restantes se fijan a un valor activo visible, mostrado y corregible. Selección y
acciones revalidan producto/plantilla, compañía, actividad y configuración. `labels` abre la acción
nativa de `product.product`; no ejecuta reportes. `prices` reutiliza la API existente con filtro
`template_id`, validado también en el servidor. El filtro no altera la firma ni la edición existente.

Stock ARG1.0.6 extiende sólo `_arg_quantities`: capacidad ARG más permiso nativo, lecturas actuales
y compañía limpia. `AccessError` conserva no determinado; no sudo ni stock ficticio. La ausencia
del módulo no impide consultar Catálogo. Cantidades se expresan por unidad sin totales entre variantes.

Cinco archivos nativos de product inspeccionados coinciden SHA256 con la instalación consultada
el2026-11-06; no se afirma igualdad de todo el core. La interfaz usa OWL de esa composición y
Lucide local de UI ARG, con sus licencias conservadas. AST/XML/JS son controles estáticos; el registro,
assets, instalación y QA deben constar por separado. [Contrato](../../specs/005-catalogo/contracts/matriz-variantes.md).
