# Reparaciones ARG · Recepción y diagnóstico

Estado: código20.0.1.1.0 preparado; instalación y revisión funcional/visual pendientes.
La recepción se amplía con presupuesto, autorización, trabajo y entrega. No está disponible aún en la demo.

## Recibir un equipo

En Ventas → Reparaciones, elegí Nuevo. La fecha propone hoy según tu zona horaria; podés corregirla.
Cargá cliente, una descripción reconocible del equipo y el problema que informa el cliente.
No necesitás crear un producto del catálogo, técnico, diagnóstico ni presupuesto para recibir.
Marca, modelo, serie, accesorios y estado recibido se completan si hacen falta.

Guardar asigna **REP-000001** y conserva un borrador. **Recibir equipo** registra la recepción
efectiva y su constancia, con el usuario y momento de registro. Una fecha futura conserva el borrador
hasta que la recepción ocurra. El equipo del cliente no aumenta existencias ni valoración propia.
Después de recibir se conserva la identificación, fecha y condición del equipo.

## Registrar el diagnóstico

Después de recibir, completá la pestaña Diagnóstico y elegí **Registrar diagnóstico**.
La constancia conserva el texto registrado. Este paso no autoriza un trabajo, no consume repuestos,
no confirma un presupuesto ni genera facturas. No hace falta asignar un empleado adicional para
cargarlo: una misma persona puede operar con las capacidades de Reparaciones habilitadas.

## Devolver sin reparar

Usá **Devolver sin reparar** si el equipo debe salir sin realizar el trabajo. Indicá fecha efectiva,
quién retira y motivo o constancia. La fecha no puede ser posterior a hoy ni anterior a los hechos
ya registrados. La devolución cierra la custodia y conserva recepción y diagnóstico, si lo hubo.
No crea un remito de mercadería propia ni cobra al cliente.

**Cancelar borrador** sólo cancela un registro aún no recibido. No elimina el número ni reemplaza
la constancia de devolución de un equipo que sí se recibió.

## Consultar e imprimir

El listado permite buscar REP, cliente, equipo o serie y filtrar equipos En custodia.
El historial conserva fecha efectiva, fecha de registro, usuario y constancia de cada hecho.
Los ejes separan recepción, diagnóstico y devolución; devolver sin diagnóstico no significa haberlo
completado. El parte impreso distingue borrador, datos de ejemplo y diagnóstico aún en preparación.
Es una constancia de gestión y custodia; no es factura ni autorización de trabajo.

## Presupuestar y autorizar

**Presupuesto** prepara un PRE independiente con cliente y diagnóstico conocidos. Agregá repuestos
y servicios, por ejemplo un repuesto y dos horas de mano de obra. Emití el PRE, confirmá cantidades
y generá su PED separado con las acciones de Ventas. Una revisión conserva el vínculo con REP.

**Autorización del cliente** pide pedido, fecha, quién autoriza y constancia. Si sólo hay un pedido
pendiente se propone. La cobertura puede ser a cargo del cliente, garantía declarada o mixta;
declararla no cambia precios ni certifica una garantía. Los precios se acuerdan en el PRE, incluidos
ceros expresamente aceptados. Después confirmá el PED e **Iniciá trabajo**. Ninguno de estos pasos
entrega repuestos, factura ni cobra por sí solo. Un alcance adicional usa revisión, PED y autorización propios.

## Repuestos y partes de trabajo

**Repuestos** abre entregas y devoluciones nativas del PED. Completá cantidades efectivas, series/lotes
si corresponden, y validá. Esa salida representa los repuestos instalados/entregados; no crees además
una salida interna por el mismo hecho. El equipo ajeno sigue separado del stock propio.
La devolución parte del movimiento validado y debe actualizar cantidades del pedido; no genera
automáticamente una nota de crédito ni otro cobro.

**Registrar trabajo** prepara un PTM con fecha, reparación, servicio del PED y cantidad realizada.
Se propone la persona actual; no necesitás crear otro técnico. La cantidad representa horas si la
unidad del servicio es hora; otra unidad conserva su significado. Guardar deja un borrador;
**Registrar trabajo** confirma el cumplimiento nativo, sin superar lo autorizado. Se admiten servicios
de cantidad manual; este adaptador no reemplaza analítica ni partes de horas de otros módulos.

**Revertir parte** pide fecha y motivo, conserva el PTM y corrige la cantidad nativa. Si estaba listo,
el trabajo vuelve a estar en curso. Si el equipo ya se entregó, su constancia física se conserva y
los pendientes muestran la corrección; no se afirma que volvió al taller. No revierte facturas ni cobros.

## Terminar, entregar, facturar y cobrar

**Trabajo listo** comprueba repuestos y servicios efectivos de los pedidos activos. Deben resolverse
pedidos en borrador, cancelados sin liberar y cantidades de PRE confirmadas sin pedido. Los
pendientes se completan o se corrigen mediante sus documentos/revisiones, sin marcarlos como cumplidos.
**Retomar trabajo** exige motivo; **Entregar equipo reparado** pide fecha y quién retira, vuelve a
comprobar el alcance y cierra custodia. Entregar no factura ni cobra.

Desde **Pedidos**, abrí el PED y usá **Preparar factura**, conservando la política y el origen por
línea nativos. **Facturas** consulta facturas/notas vinculadas; REP no genera una segunda factura.
El recibo REC y sus medios se registran en Administración y se aplican a la factura. Los ejes se
explican por PRE/PED, unidad, moneda y documento; no se suman cobros entre pedidos.

Recibir/diagnosticar requiere Reparaciones ARG; presupuestar y cargar PTM agrega Ventas ARG.
Autorizar/confirmar/revertir requiere Responsable ARG y permisos nativos; Stock conserva sus
capacidades. Una misma persona puede reunirlas. No se exigen departamentos distintos.

Continúan pendientes las correcciones explícitas de recepción/diagnóstico, ejemplos operativos,
reportes completos, instalación, revisión funcional/visual, PDF y aceptación. El cargador de
ejemplo sólo prepara cliente y REP borrador; no ejecuta este circuito.

El tutorial específico de YouTube está pendiente. La guía escrita y el catálogo son editables sin
inventar un enlace de video. No se envían mensajes ni se activa una integración al instalar el addon.
