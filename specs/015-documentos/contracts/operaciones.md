# Contrato de operaciones: Motor documental e impresión ARG

**Alcance**: Identidad, vínculos y presentación documental común sin reemplazar los modelos operativos nativos.

## Recorridos y datos mínimos

### Operación 1: Identificar documento

Como usuario necesito reconocer tipo, número, fecha y estado de cualquier documento.

**Resultado**: Abrir PRE-000001 y distinguir su número interno de referencias fiscales o externas.
**Excepción**: No reutilizar una secuencia cancelada ni mezclar compañías.

### Operación 2: Vincular derivados

Como operador necesito recorrer origen y derivados por cabecera y línea.

**Resultado**: Desde PRE confirmado abrir PED distinto con trazabilidad de cada línea.
**Excepción**: Impedir un segundo PED por reintento de la misma confirmación.

### Operación 3: Imprimir

Como usuario necesito un PDF simple y consistente.

**Resultado**: Generar PDF con identidad ARG, tercero, detalle, totales y estado correcto.
**Excepción**: Marcar borrador/ejemplo y no mostrar autorización fiscal inexistente.

## Invariantes

- Presupuesto y pedido son documentos distintos, no dos vistas o estados del mismo sale.order.
- Los documentos nativos conservan su name técnico cuando sea necesario; arg_number se muestra como identificador interno ARG.
- Confirmar PRE preserva condiciones y no genera PED automáticamente; Generar pedido es la acción explícita posterior e idempotente. Ninguna de las dos registra por sí sola asiento, cobro ni movimiento de stock.
- Códigos estables; nunca renumerar documentos existentes al cambiar configuración.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.

Contrato de estados y pendientes: [v1](../../../docs/tecnica/ESTADOS-Y-PENDIENTES.md). Aplicar pendiente/parcial/completo por eje y conservar cantidades/importes explicables.
