# Guía de gestión ARG

Estado: módulos ARG instalados técnicamente en demo; recorridos funcionales y aceptación pendientes.
Consultar los manuales por módulo en [el índice](../site/MANUALES.md).
Público: dueños y operadores de micropymes/pymes. Una persona puede combinar tareas según permisos.

## Recorrido común

Elegí área y documento; buscá tercero; revisá generales automáticos; cargá detalle; revisá totales y elegí acción.
Guardar conserva trabajo. Confirmar acepta un paso del circuito. Entregar, publicar factura, cobrar y pagar son acciones distintas.
No hace falta completar información avanzada que la operación todavía no requiere.

## Ventas

Crear PRE con cliente, producto/servicio y cantidad. Revisar condiciones y confirmar aceptación total o parcial.
Generar PED separado por las cantidades aceptadas pendientes; confirmar el pedido cuando corresponda.
Entregar mediante REM y facturar mediante FAC según política. Consultar cada pendiente por línea.
Cobros se registran desde Administración con acceso contextual; una factura parcial saldada no completa todo el pedido.

## Compras

Crear PPC con proveedor, líneas y cantidades. Confirmar; registrar ENT por lo efectivamente recibido.
Registrar FRC con el número original del proveedor, separado del código interno. El pago corresponde a Administración.
Conservar recepción y facturación independientes; devolución física y nota de crédito son documentos distintos vinculados.

## Stock

Consultar físico, reservado y disponible. Validar movimientos reales sin volver a cargar stock al facturar.
Contar con INV, revisar diferencia y aplicar AJU con motivo. Pedir lote/serie sólo si el producto lo requiere.
Mostrar pendientes de recepción/entrega, backorders y faltantes cerrados sin confundirlos con cumplimiento.

## Administración

Consultar deuda por documento, vencimiento y moneda. Crear REC para cobro u OPA para pago con uno o varios medios.
Aplicar total/parcial a deuda existente o conservar anticipo libre. Consultar caja/banco desde apuntes publicados.
Corregir mediante reversión/desaplicación con historial; no borrar movimientos confirmados para cuadrar saldos.

## Informes y ayuda

Elegir compañía, fecha y moneda; distinguir venta, entrega, cobro y saldo. Abrir documentos que componen el indicador.
Exportar con filtros/unidades/moneda identificados. Manual y tutorial de versión desde ayuda del módulo.
Soporte general ARG abre sólo canales configurados; no envía datos por abrir la ayuda.
