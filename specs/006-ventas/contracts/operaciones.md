# Contrato de operaciones: Circuito Ventas ARG

**Alcance**: Presupuesto propio PRE, pedido cliente PED independiente, entregas y facturas vinculadas sin duplicar efectos nativos.

## Recorridos y datos mínimos

### Operación 1: Preparar y confirmar presupuesto

Como vendedor necesito un presupuesto como documento independiente del pedido de cliente.

**Resultado**: Guardar PRE-000001, confirmarlo y consultar sus líneas/condiciones sin movimientos de stock ni dinero.
**Excepción**: Bloquear cambios sobre la versión confirmada y permitir una revisión nueva con historia.

### Operación 2: Generar pedido cliente

Como vendedor necesito crear un pedido posterior desde el presupuesto confirmado sin reescribir líneas.

**Resultado**: Generar PED-000001 separado, enlazar PRE-000001 y conservar ambos documentos consultables.
**Excepción**: Rechazar generación duplicada concurrente y mostrar el pedido existente.

### Operación 3: Entregar y facturar

Como operador necesito distinguir pendiente de entrega, facturación y cobro.

**Resultado**: Consultar cantidades pedidas, entregadas y facturadas con sus documentos de origen y acceder al cobro de Administración.
**Excepción**: Separar faltante cerrado de cantidad cumplida y no crear otra entrega al facturar.

## Invariantes

- Estados de presupuesto: borrador, emitido, parcialmente confirmado, confirmado, rechazado, vencido y cancelado; registrar revisión al cambiar condiciones confirmadas.
- Generar pedido mediante acción explícita; ofrecer confirmar y generar como acción combinada sólo si explica ambos efectos.
- Asignar PRE al presupuesto y PED al pedido; conservar numeración fiscal separada.
- Conservar sale.order como única fuente operativa de pedidos, entregas y facturación.
- Mantener bloqueo idempotente contra doble clic o concurrencia en generación del pedido.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.

Contrato vinculante detallado: [PRE/PED v1](../../../docs/tecnica/CONTRATO-PRESUPUESTO-PEDIDO.md).

Contrato de estados y pendientes: [v1](../../../docs/tecnica/ESTADOS-Y-PENDIENTES.md). Aplicar pendiente/parcial/completo por eje y conservar cantidades/importes explicables.
