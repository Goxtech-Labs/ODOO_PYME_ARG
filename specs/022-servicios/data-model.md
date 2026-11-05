# Modelo conceptual · Servicios recurrentes, reservas y expedientes ARG

Expediente con documentos enlazados; abono con vigencia/periodicidad/próxima generación; ocurrencia; recurso y reserva con inicio/fin/zona horaria/capacidad; cancelación.

## Fuentes y validaciones

Recurrencia genera borradores idempotentes por período; reservas de agenda no son reservas de stock ni cobros. Documentos emitidos conservan origen y evidencia.

- Un abono genera como máximo una ocurrencia efectiva por período y compañía.
- No publicar factura ni cobrar automáticamente por ejecutar el planificador inicial.
- Una reserva no supera la capacidad del recurso ni solapa en concurrencia sin regla de capacidad.
- Cancelar una reserva no borra una factura ni libera stock no vinculado.

Identificación documental propuesta: EXP / RSV / ABN propuestos. Compañía obligatoria en transacciones; relaciones
compatibles con compañías permitidas. Cantidades/importes usan precisión monetaria/unidad nativa.
Fechas iniciales usan contexto de usuario; las históricas y externas conservan origen. Eventos incluyen
actor/fecha/origen, clave idempotente y efecto nativo; no almacenar residuales alternativos.

## Transiciones

Expediente → contrato/abono o reserva → prestación → propuesta de documento comercial → factura/cobro existentes.
Cada transición declara precondición, actor, efectos, evidencia y corrección en el contrato; no permitir
cambio directo de estado por escritura RPC para simular el efecto.
