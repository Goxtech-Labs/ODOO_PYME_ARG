# Contrato de documentos y circuitos

## Circuitos comunes

| Circuito | Flujo | Separación obligatoria |
| --- | --- | --- |
| Ventas | Presupuesto → pedido → remito → factura | Propuesta, compromiso, entrega y facturación |
| Compras | Pedido proveedor → entrada → factura recibida | Solicitud, recepción y deuda |
| Stock | Entrada/salida → transferencia → inventario/ajuste | Existencia física, reserva y disponibilidad |
| Administración | Recibo/cobro → aplicación; orden/pago → aplicación | Dinero, deuda e imputación |
| Informes | Hecho → dimensiones → filtros → resultado → documento fuente | Consulta sin modificar operaciones |

Admitir facturación directa, servicios sin remito y entregas/facturas parciales mediante políticas explícitas.
Definir devoluciones y notas como recorridos inversos vinculados, sin borrar la operación original.
Ubicar recibos y pagos en Administración, con accesos contextuales desde ventas/compras.

## Identidad y mínimo de datos

Mantener Presupuesto ARG y Pedido de cliente ARG como documentos independientes.
Confirmar presupuesto sin crear por ese acto movimientos físicos, facturas ni cobros.
Generar pedido mediante acción explícita sobre presupuesto confirmado; asignar otro número y conservar origen.
Bloquear repetición accidental de la generación y conservar las líneas y condiciones aprobadas.
Mantener presupuesto original consultable después de generar el pedido.

Mostrar tipo, código corto, número, compañía, estado y fecha relevante.
Separar identidad interna, referencia del tercero y numeración fiscal.
Conservar compañía, moneda y vínculo de origen al generar derivados.
Tratar seis dígitos como ancho mínimo; permitir crecimiento del contador sin truncarlo.
No reiniciar por ejercicio de forma implícita ni reutilizar números anulados.

| Documento | Selecciones mínimas con configuración completa | Completar automáticamente |
| --- | --- | --- |
| Presupuesto | Cliente, producto/servicio y cantidad | Fecha, moneda, tarifa, impuestos y condiciones conocidas |
| Pedido derivado | Origen y aceptación de cantidades | Cliente, líneas y condiciones aprobadas |
| Entrada/remito | Origen y cantidades efectivas | Tercero, depósito predeterminado y pendientes |
| Factura derivada | Origen y cantidades/importes facturables | Tercero, moneda, impuestos y vencimientos configurados |
| Recibo/cobro | Cliente o deuda, importe y medio si no existe uno predeterminado | Fecha, moneda y referencia |
| Orden/pago | Proveedor o deuda, importe y medio si corresponde | Fecha, moneda y referencia |
| Inventario | Depósito, producto y cantidad contada | Existencia teórica y diferencia |

Mostrar campos adicionales sólo por datos faltantes, excepción, permiso o característica habilitada.
No inventar CUIT, domicilios fiscales, medios de pago ni cotizaciones desconocidas.
Permitir borrador incompleto cuando el documento nativo lo admita; validar requisitos al confirmar.

## Invariantes

- Conservar origen/destino bidireccional y detalle de cantidades/importes pendientes.
- Evitar aplicar dos veces una línea ya entregada, facturada o cobrada.
- Verificar concurrencia en servidor antes de confirmar efectos.
- Mantener versiones aceptadas de presupuestos identificables.
- Respetar cantidades, redondeos, unidades e impuestos nativos.
- Separar dato visible, permiso de edición y permiso de confirmación.
- Registrar correcciones mediante reversiones cuando existan efectos confirmados.
- Conservar importes históricos al cambiar listas, impuestos o cotizaciones.
- Etiquetar factura interna sin autorización fiscal hasta incorporar ARCA.

## Hechos y dimensiones

Aplicar granularidades y medidas de [data-model.md](../data-model.md).
Definir cada indicador con hecho, fecha, signo, moneda, filtros y origen navegable.
Evitar unir líneas documentales mediante relaciones múltiples sin controlar duplicaciones.
Calcular totales desde datos fuente autorizados; no desde filas parcialmente cargadas en pantalla.

## Evolución

Versionar contratos con cada cambio incompatible y enumerar módulos consumidores.
Mantener extensiones por rubro compatibles con identidad, orden y efectos comunes.

Regla vinculante de parciales: [estados y pendientes](../../../docs/tecnica/ESTADOS-Y-PENDIENTES.md). PRE/PED admite generación parcial según [contrato v1.1](../../../docs/tecnica/CONTRATO-PRESUPUESTO-PEDIDO.md).
