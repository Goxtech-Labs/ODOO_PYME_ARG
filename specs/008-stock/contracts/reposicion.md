# F15 · Reposición ARG por mínimos y máximos

## Entrada y documentos

Stock → Reposición abre reglas existentes de la compañía actual. Página y selección máxima30.
Producto, depósito/ubicación y mínimo/máximo son la configuración esencial; deducir compañía y
ubicación principal sólo si están determinadas. Avanzado: ruta, múltiplo, proveedor/BOM y horizonte.
Guardar regla es configuración; consultar propuesta es lectura; confirmar es una acción explícita.
Nuevas reglas ARG manuales. Las existentes conservan manual/auto y su configuración/scheduler.

Proveedor/BOM son selecciones nativas de los puentes opcionales de compra y fabricación. La
elección explícita requiere una ruta explícita; sin ella se conserva la selección nativa del
producto para la futura propuesta. Validar compañía, plantilla/variante y tipo de BOM; no copiar
precios al formulario ni exponer nombres de dimensiones inaccesibles. Quitar una ruta puede
limpiar proveedor/BOM según las inversas nativas; validar también el múltiplo resultante.

El horizonte es `res.company.horizon_days`, común a todas sus reglas, no un dato persistido por
producto. Mostrarlo plegado en el listado y editarlo en una tarea separada que explica ese alcance.
Exigir responsable ARG, permiso nativo de compañía/campo y token vigente; no guardar el horizonte
al guardar una regla. Reconsultar mantiene el valor en edición y muestra la configuración actual
antes de volver a guardar. Ni ese cambio global ni los selectores ejecutan abastecimiento.

La propuesta no es un pedido ni una orden de fabricación. La confirmación genera o amplía documentos
nativos: compras continúan por PPC; fabricación conserva sus referencias nativas y sus estados.
La evidencia técnica de confirmación no sustituye numeraciones ni crea otro documento financiero.

## Propuesta revisable

Mostrar momento/horizonte, producto, ubicación, unidad, físico, previsto y abastecimiento en curso,
sugerencia nativa y cantidad elegida. No sumar pipeline dos veces ni reemplazar la sugerencia por
máximo menos físico. No representar falta de permiso como cero. Efectos esperados por ruta efectiva,
proveedor o BOM accesibles; cantidades positivas finitas y coherentes con unidad/múltiplo nativos. Mostrar si existe una
cantidad manual pendiente y que la confirmación la deja resuelta.

La revisión incluye rutas encadenadas, componentes/kit y lotes de producción cuando correspondan.
Fabricación puede crear varias MO o ampliar una existente, con estados según configuración nativa;
no prometer siempre borradores. Intermedios pueden planificar/reservar stock; confirmar reposición
no equivale a validar una recepción, consumir fabricación, facturar o pagar.

Al volver de maestros conservar reglas/cantidades y la propuesta revisada. Si una configuración
relevante o el abastecimiento cambia, requerir una nueva revisión antes de producir efectos.
La ausencia de compra/MRP/configuración explica qué falta, sin simular un resultado.

## Confirmación y reintentos

Responsable ARG y permisos nativos de reglas, compañía, productos, rutas, proveedor/BOM y destinos.
Contexto limpio, una compañía; serializar reglas/productos/maestros en orden estable con actualización
efectiva de filas y relectura, compatible con el aislamiento/reintento nativo.

Tras autorizar/serializar, buscar operación por compañía+clave antes de volver a calcular una
propuesta ya ejecutada: misma clave/payload devuelve evidencia original; carga distinta falla.
Para operación nueva comparar huella y fijar cantidades aceptadas sin `action_replenish`, que las
sustituye. Usar confirmación nativa sin nuevo cursor, con errores propagados y sin commits internos;
mostrar el manual previo, reemplazarlo por la cantidad aceptada y consumir ese override al completar;
no cambiar modalidad. En reglas automáticas escribir el campo manual directamente, pues la inversa
de qty_to_order borra el manual.

Una sola transacción para efectos y evidencia inmutable de actor/compañía/momento/cantidades y
referencias/deltas. UUID canónico36 y unicidad por compañía; uso interno, no numeración comercial.
Fallo de permiso/configuración/postcondición revierte todo; no éxitos parciales ocultos.

## Permisos y captura de resultados

El core contiene sudo interno; llamarlo no basta para proteger al actor. Objeto Python privado
hashable en contexto vincula identidad/compañía/decisiones/collector. No aceptarlo desde datos RPC.
Guardas de destinos revalidan acceso como actor original antes de crear/ampliar y al devolver/open.
Capturar referencias/deltas por hooks en la misma transacción, incluidos PO/MO ya existentes,
cambios de cantidad, lotes y componentes. No correlacionar sólo por fecha/count ni crear una referencia
única que modifique agrupación nativa. Cada rama aceptada debe acreditar efectos nativos compatibles;
la ausencia de error o retorno vacío no demuestra éxito.

No persistir un saldo nuevo. La evidencia cruda no tiene ACL de lectura/escritura/exportación
para usuarios de gestión, incluido el actor original; sólo acceso técnico elevado desde métodos
privados autorizados. No basta ocultar botones o limitar create_uid. El servicio valida rol y
compañía, carga únicamente la evidencia técnica y revalida SIN sudo todas sus referencias/dimensiones
nativas con el solicitante ACTUAL de esa lectura antes de devolver cualquier dato de resultado,
incluido un replay. El actor histórico de la confirmación no presta sus permisos al receptor. Si alguna dimensión
ya no es accesible o no puede validarse, denegar la representación completa con mensaje genérico,
sin nombres/IDs/cantidades ocultas. No volver a ejecutar una clave ya registrada aunque no pueda
mostrarse su resultado. Leer/exportar/buscar raw JSON por RPC debe fallar por ACL del modelo;
las rutas de lectura autorizadas sólo devuelven la representación validada. Abrir resultados vuelve
a comprobar permisos actuales. No usar sudo para leer documentos de negocio ocultos. Las rutas automáticas
existentes y otros disparadores conservan semántica; inventariar cobertura de sus caminos sin
atribuirles garantías del flujo ARG si no pasan por la confirmación ARG.

## Modularidad y entrega

Core Stock ARG para reglas/propuesta/orquestación; compra en Compras–Stock ARG y fabricación en
puente opcional Stock–MRP. Fabricación permanece dentro de F15 completo aunque MRP sea optativo
por instalación. Composición demo habilitada explícitamente, manual y tutorial por versión.
Desarrollar/revisar fuentes, respaldar y comprobar instalación/arranque en el CT definitivo, con
snapshot o respaldo del mismo CT para probar o recuperar. No crear CT temporales de desarrollo,
QA, clonación o restauración ni utilizar otro existente como staging. Publicar según autorización;
QA funcional/visual/concurrencia/PDF y aceptación posteriores. Parent016T009 sigue abierta hasta
entregar F14/F15; no reducir las22 capacidades ni Integraciones ARG.

## Efectos encadenados de fabricación

La propuesta enumera también MO borrador previas que el postprocesado nativo puede confirmar.
Cambiar cantidad de una MO actualiza insumos/subproductos/trabajos/planificación y puede disparar
reposiciones automáticas de componentes. Conservar esa semántica dentro del alcance revisado,
sin cambiar parámetros globales del scheduler. Cantidades raíz aceptadas y cantidades derivadas
nativas se identifican por separado; explicar consecuencias sin prometer un valor fijo para cada
rama dependiente del proceso. Autorizar las reglas/componentes/documentos del grafo revisado antes
de efectos, propagar el collector y errores atómicos a las llamadas hijas. Una rama/configuración
fuera de la revisión aborta toda la operación y pide una propuesta nueva; no ejecutar una porción
ni saltar silenciosamente los efectos nativos para anunciar éxito.

El contrato de concurrencia exige participación de los mutadores nativos de físico/previsión,
abastecimiento pendiente y maestros, incluidos orígenes ajenos al flujo ARG. Un lock de wizard
no prueba esa cobertura. Mantener permisos nativos y super en esa serialización; la autorización
ARG adicional se limita al collector privado. Inventariar los campos/métodos de cada consumidor
antes de cerrar la implementación; no prometer atomicidad ampliada por una lectura de huella sola.
