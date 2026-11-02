# Hechos, dimensiones y medidas

| Hecho | Grano | Fecha | Medidas | Dimensiones / exclusiones |
| --- | --- | --- | --- | --- |
| Presupuestado | Línea PRE/revisión | Emisión | Cantidad, neto, total propuesto | Cliente, producto, moneda, estado; no sumar revisiones como nuevas ventas |
| Pedido | Línea PED | Confirmación | Pedido, pendiente, cancelado | Cliente, producto, depósito, moneda; separar borrador |
| Entrega | Línea de movimiento terminado | Efectiva | Cantidad neta entregada | Ubicación, producto, lote, tercero; retornos con signo |
| Facturación | Línea de factura publicada | Contable y emisión separadas | Neto, impuesto, total | Tercero, producto, tipo, moneda; notas con signo |
| Compra | Línea PPC confirmada | Aprobación | Pedido/recibido/facturable | Proveedor, producto, unidad, moneda |
| Caja/banco | Apunte de liquidez publicado | Contable | Entrada, salida, neto | Diario, medio, moneda, tercero; no repetir por aplicación |
| Aplicación | Parcial de conciliación | Conciliación | Importe aplicado | Apuntes vinculados, monedas; separar reversión |
| Deuda | Apunte abierto a corte | Vencimiento/corte | Residual | Tercero, compañía, moneda; excluir borradores |
| Existencia | Producto/ubicación/lote | Actual o corte explícito | Físico, reservado, disponible | Unidad, compañía, depósito; histórico desde movimientos |

No sumar cantidades de unidades incompatibles ni importes de monedas diferentes.
Una conversión gerencial declara moneda objetivo, fecha y tasa; no altera tasa histórica del documento.
Evitar joins que multipliquen una factura por cada entrega/pago; agregar cada hecho a su grano antes de relacionarlo.
Toda medida muestra corte, fuente, signo, unidad/moneda, filtros y enlace al origen autorizado.
Físico actual = quantity; reservado = reserved_quantity; disponible inmediato = físico - reservado.
Previsto agrega entradas/salidas futuras según dominio y fechas declarado, no es existencia actual.
Saldo a fecha requiere reconstruir aplicaciones hasta el corte: residual actual no es automáticamente deuda histórica.
