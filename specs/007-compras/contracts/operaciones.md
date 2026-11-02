# Contrato de operaciones: Circuito Compras ARG

**Alcance**: Pedido a proveedor, entrada, factura recibida y devolución separados, con mínima carga y documentos vinculados.

## Recorridos y datos mínimos

### Operación 1: Pedir al proveedor

Como comprador necesito crear un pedido con proveedor, productos y cantidades.

**Resultado**: Guardar PPC-000001 y confirmar condiciones conocidas sin exigir circuitos departamentales adicionales.
**Excepción**: Mantener aprobación adicional sólo si el responsable la configura y preservar referencia del proveedor.

### Operación 2: Recibir y registrar factura

Como operador necesito entradas y facturas recibidas independientes del pedido.

**Resultado**: Recibir parte del pedido mediante ENT y registrar FRC vinculada sin duplicar entrada.
**Excepción**: Conservar cantidades pendientes y distinguir recepción cerrada de cumplimiento total.

### Operación 3: Gestionar devolución

Como operador necesito devolver mercadería o registrar una nota vinculada sin borrar historia.

**Resultado**: Generar devolución desde entrada y consultar su efecto neto y documentos relacionados.
**Excepción**: No descontar dos veces una devolución ni confundirla con cancelación del pedido.

## Invariantes

- Estados nativos de compra: draft, sent, to approve, purchase y cancel; etiquetas ARG sin falsificar estado real.
- Usar product_qty, qty_received, qty_invoiced y qty_to_invoice según política del producto.
- Conservar unidad uom_id de purchase.order.line en la rama Odoo20 verificada.
- Usar relaciones de líneas, no sólo texto origin.
- No interpretar receipt_status full como prueba de todas las cantidades recibidas.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.

Contrato de estados y pendientes: [v1](../../../docs/tecnica/ESTADOS-Y-PENDIENTES.md). Aplicar pendiente/parcial/completo por eje y conservar cantidades/importes explicables.
