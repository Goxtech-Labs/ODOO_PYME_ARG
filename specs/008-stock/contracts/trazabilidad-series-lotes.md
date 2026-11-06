# F14 · Series/lotes y trazabilidad ARG

## Entrada y alcance

Buscar número/nombre/referencia de lote, con producto opcional, páginas30. Un número textual
conserva sus ceros. El producto se valida con su variante/unidad/compañía; no se interpreta una
plantilla como una variante. Mantener compañía actual y permisos nativos en servidor, sin sudo.

La consulta requiere un lote elegido. Lista de movimientos finalizados por fecha/id y páginas30;
rango de fecha/hora opcional en sección progresiva, sin reemplazar fechas elegidas. Fecha/hora de
consulta actual propuesta como dato informativo local. El rango filtra historia, no existencias actuales.
Mostrar recepción, entrega, traslado, devolución, ajuste y otros hechos nativos según sus ubicaciones
y relaciones; el tipo no altera cantidades ni inventa su estado. Una fila corresponde a stock.move.line.

## Cantidades y documentos

Producto/unidad/cantidad reales de cada línea; usar quantity_product_uom cuando se presenta en
unidad base. La cantidad no se convierte en ingreso neto ni se suma entre ubicaciones como si fuera
saldo. La existencia actual visible usa lot.product_qty nativa, y los detalles paginados de quant
muestran ubicación, propietario, paquete, cantidad y reserva. Total y detalle usan exactamente el
mismo dominio nativo de ubicaciones de product._get_domain_locations()[0], el mismo lote/contexto
y las mismas reglas de acceso; no incluir ubicaciones externas que ese dominio excluye.
Contexto limpio, sin filtros de otra
consulta. Sin acceso a cantidades, estado no determinado; no un cero de sustitución.

Abrir picking o movimiento revalidando lote/línea/compañía/permisos. Las relaciones comerciales se
consultan desde el documento, sin inferir factura por lote. Ajustes sin picking conservan su movimiento
nativo. La traza avanzada abre la acción nativa del lote: su experiencia es distinta de la tabla ARG.
No reconstruir historia por textos de referencia ni asignar documentos a números coincidentes.

## Alta mínima explícita

Asistente transitorio: producto rastreable y número; referencia opcional. Compañía actual deducida.
No activar seguimiento en productos existentes ni cambiar ubicaciones mediante el alta. Crear el lote
nativo con permisos de creación y abrir su consulta. Las existencias se registran en recepciones,
transferencias o inventarios validados, con los controles actuales de Stock ARG.

Serializar el mismo asistente y los productos para evitar duplicación concurrente. Extender
stock.lot.create y las escrituras de identidad (nombre/producto/compañía) con el mismo lock técnico
de producto, también para altas nativas; conservar las validaciones de unicidad del core. Conservar un enlace al
lote creado, protegido contra RPC directo; repetir la misma confirmación devuelve el mismo resultado.
Tras completar el alta, los datos del asistente quedan inmutables. Otra alta usa otro asistente.
Número/referencia entre1–256/0–256 caracteres como límites de captura, sin imponer formato ARG a
identificadores del fabricante ni renumerar existentes.

## Seguridad y entrega

Consulta sólo interna con Stock ARG/admin y ACL nativas; contexto limitado a compañía/lang/tz.
IDs, páginas y rangos validados. Permiso insuficiente en relaciones devuelve dato restringido sin
revelar nombres/IDs no autorizados. Elegir/filtrar/paginar no crea maestros ni movimientos.
Guardar configuración y producir efectos son acciones distintas. Conservar selección/rango al volver.

No crear otro saldo ni tabla de movimientos. Servicio abstracto y asistente transitorio, con resultado
idempotente del alta, no libro nuevo. Manual, tutorial versionado planeado y escenarios de QA posterior.
Instalación/upgrade/arranque técnicos ahora; recorridos de negocio/visual/PDF/aceptación posteriormente.
F15/reposición sigue como incremento posterior y parent016T009 no se cierra sólo con F14.

## Dependencia nativa de lotes y series

El rol Stock ARG implica stock.group_production_lot para mostrar lote/serie en los detalles nativos
de movimientos. Este grupo permite usar los controles nativos del circuito con productos rastreables;
no cambia su seguimiento ni registra existencias. Conservar ACL nativas de lotes/movimientos y
no conceder roles ARG a usuarios ajenos al módulo. La lectura de grupos/configuración no es QA de un movimiento.
