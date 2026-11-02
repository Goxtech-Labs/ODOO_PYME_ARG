# Informes ARG

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Abrí Informes → Consultas por hechos. Elegí qué querés medir, compañía, período y moneda.
Podés indicar tercero y buscar producto o ubicación por texto. Ver por permite detalle, fecha,
documento, tercero, producto, ubicación o estado propio. Consultar vuelve a la primera página.

## Qué mide cada consulta

| Hecho | Qué incluye | Cómo leerlo |
| --- | --- | --- |
| Facturación de ventas/compras | Líneas de facturas publicadas y sus notas | Neto e impuesto por línea; notas con signo contrario; no incluye presupuestos ni caja |
| Pedidos confirmados | Líneas de PED/PPC confirmado | Acuerdos comerciales; no equivale a venta facturada ni a dinero |
| Caja y banco | Apuntes publicados en cuentas de liquidez | Entrada positiva, salida negativa; no repite un cobro por cada factura; excluye cuentas transitorias |
| Deuda actual | Apuntes/cuotas por vencimiento, con residual actual | Deuda positiva, crédito negativo; el período filtra vencimientos, no reconstruye deuda histórica |
| Aplicaciones | Conciliaciones parciales vigentes, una vez cada una | Importe en moneda de compañía; una conciliación puede ser nota/ajuste, no prueba dinero |
| Movimientos físicos | Líneas terminadas y sus devoluciones | Entregas y recepciones positivas; retornos negativos en su circuito; origen y destino explícitos |
| Existencias actuales | Quants por producto/ubicación/lote/propietario/paquete | Físico, reservado y disponible actuales; el período se ignora |
| Existencias a fecha | Movimientos desde el inicio hasta fin de Hasta | Extremos internos de compañía, en unidad base; no usa el saldo actual como histórico |

La facturación muestra medidas de las líneas seleccionadas; no reconstruye el total fiscal de cabecera
ni incluye ajustes de redondeo separados. Unidades y monedas conservan su significado. No se suman
entregas y recepciones como si fueran variación de stock: cada circuito físico mantiene su total.
Stock histórico usa productos actualmente almacenables. Cambios históricos de unidad, clasificación
o compañía de ubicación requieren revisión; no se inventa la historia que falta.

## Explicar un total

El resultado informa fuente, granularidad, fechas, zona horaria, moneda y momento de generación.
Muestra50filas por página y totales del corte completo. Anterior/Siguiente navegan sin cambiar los filtros.
Ver por agrupa por identidad real, conservando la unidad y el circuito físico. Documento abre el origen;
Origen/contrapartida permite seguir una nota, devolución o aplicación. Se respetan tus permisos.
Los ejes ARG de avance mantienen pendiente/parcial/completo y cerrado con faltante; el informe no los edita.

## Exportar

CSV UTF-8 y PDF conservan filtros y criterios. El PDF usa A4 apaisado. Cada exportación vuelve a consultar
la fuente vigente y muestra su momento de generación; si hubo operaciones nuevas puede diferir de una
consulta anterior. Exportá con el mismo corte y sin nuevas escrituras para comparar una consulta y su salida.
No es una instantánea fiscal guardada. CSV protege textos que una planilla podría interpretar como fórmulas.

Un corte que supera5000registros fuente pide reducir filtros; no entrega cifras truncadas. El PDF admite
hasta2000filas resultantes; CSV conserva el corte admitido completo. La consulta no descarga todo al navegador.
Para stock histórico extenso, filtrar producto/ubicación reduce el historial; no se reemplaza por quants actuales.

Necesitás Consulta Informes ARG o Administrador ARG y permisos de lectura de cada fuente. Sólo aparecen
hechos disponibles en tu instalación; Informes no habilita fuentes ni instala todos los circuitos.
Las consultas son filtros temporales propios; no alteran documentos ni saldos. Ayuda contiene guía escrita;
YouTube queda pendiente hasta que el responsable configure videos reales. QA funcional/visual y aceptación pendientes.
