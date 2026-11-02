# Diccionario documental ARG v1

Código de tres letras + guion + secuencia de ancho mínimo seis, sin truncar crecimiento.
Secuencia por compañía y tipo; no reinicio anual implícito. Asignar al primer guardado documental válido,
permitir huecos técnicos y conservar cancelados. La unicidad se controla en base de datos, además de la secuencia.
Una ficha de cliente/producto no es un comprobante de transacción.

| Circuito | Código | Documento | Fuente de efecto |
| --- | --- | --- | --- |
| Ventas | PRE | Presupuesto | Ningún efecto físico/contable |
| Ventas | PED | Pedido de cliente | Compromiso comercial nativo |
| Ventas | REM | Remito de salida | Picking/movimientos validados |
| Ventas | FAC | Factura de venta | Asiento publicado; fiscal separado |
| Ventas | NCV | Nota de crédito venta | Asiento inverso vinculado |
| Ventas | DCL | Devolución de cliente | Picking de retorno vinculado |
| Compras | PPC | Pedido a proveedor | Compromiso de compra nativo |
| Compras | ENT | Entrada de mercadería | Picking/movimientos validados |
| Compras | FRC | Factura recibida | Asiento publicado y referencia proveedor |
| Compras | NCP | Nota de crédito proveedor | Asiento inverso vinculado |
| Compras | DCP | Devolución a proveedor | Picking de retorno vinculado |
| Stock | TRA | Transferencia interna | Movimiento por ubicación; neutro en total empresa |
| Stock | INV | Conteo de inventario | Sin efecto hasta aplicar ajuste |
| Stock | AJU | Ajuste de inventario | Movimientos de diferencia |
| Stock | SAL | Salida interna | Movimiento justificado |
| Administración | REC | Recibo de cobranza | Pagos nativos y aplicaciones |
| Administración | OPA | Orden de pago | Pagos nativos y aplicaciones |

Notas de débito NDV, movimiento entre cajas MCA y otros tipos adicionales requieren incremento específico; no implican capacidades ya implementadas.

FAC-000001 es una referencia interna ARG. Nunca reemplaza letra/tipo/punto de venta/número fiscal,
CAE u otra autorización, ni el número original de factura del proveedor.
No asignar secuencia documental nueva a cada reimpresión. Las plantillas usan copia de datos históricos.
Definir variantes o nuevos tipos en spec independiente; no reutilizar código con otro significado.
