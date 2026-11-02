# Contrato de operaciones: Circuito Stock ARG

**Alcance**: Consultar existencias y operar entradas, salidas, transferencias, inventarios y ajustes con trazabilidad nativa.

## Recorridos y datos mínimos

### Operación 1: Consultar cantidades claras

Como responsable necesito distinguir stock físico, reservado, disponible y previsto.

**Resultado**: Consultar producto y depósito mostrando cada cantidad con unidad y fecha de corte.
**Excepción**: No presentar cantidad prevista como existencia física ni sumar el mismo traslado dos veces.

### Operación 2: Registrar movimiento

Como operador necesito una entrada o salida con origen y cantidades reales.

**Resultado**: Validar una entrega parcial y encontrar su remito, movimiento y pendiente vinculado.
**Excepción**: Pedir serie/lote sólo al producto trazable y ofrecer dejar pendiente o cerrar faltante explícitamente.

### Operación 3: Contar inventario

Como operador necesito registrar cantidad contada y aplicar diferencias de forma trazable.

**Resultado**: Guardar INV, comparar contado/teórico y aplicar AJU enlazado a movimientos nativos.
**Excepción**: Detectar cambios concurrentes antes de aplicar y evitar sobrescribir cantidad real sin evidencia.

## Invariantes

- Una transferencia interna es neutra para el total de empresa y cambia saldos por ubicación.
- Distinguir demanda product_uom_qty, cantidad operada quantity y cantidades finalizadas.
- Usar backorders y retornos nativos, conservando enlaces.
- No escribir qty_delivered o qty_received comerciales cuando derivan de movimientos.
- No generar stock por editar tarifas ni contabilizar otra entrada al registrar factura.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.

Contrato de estados y pendientes: [v1](../../../docs/tecnica/ESTADOS-Y-PENDIENTES.md). Aplicar pendiente/parcial/completo por eje y conservar cantidades/importes explicables.
