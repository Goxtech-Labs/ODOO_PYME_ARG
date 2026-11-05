# Modelo conceptual · Obras, capítulos y costos ARG

Obra y capítulo; presupuesto versionado; parte de material con movimiento; parte de mano de obra con horas/tarifa histórica; vínculo analítico y certificación/hito comercial.

## Fuentes y validaciones

Costos reales desde compras, consumos y horas nativos; distinguir comprometido, devengado y pagado. No sumar dos veces compra y consumo del mismo material.

- Material comprado para depósito y material consumido en obra son hechos distintos.
- Costo previsto, real, facturado y pagado no se suman como una misma medida.
- Cambiar la tarifa vigente no reescribe horas ni presupuestos aceptados.
- Una obra admite un operador con roles combinados.

Identificación documental propuesta: OBR / PMA / PMO propuestos. Compañía obligatoria en transacciones; relaciones
compatibles con compañías permitidas. Cantidades/importes usan precisión monetaria/unidad nativa.
Fechas iniciales usan contexto de usuario; las históricas y externas conservan origen. Eventos incluyen
actor/fecha/origen, clave idempotente y efecto nativo; no almacenar residuales alternativos.

## Transiciones

Presupuesto de obra → capítulos → compras/consumos/horas → avance → facturación por capítulos o hitos → cierre.
Cada transición declara precondición, actor, efectos, evidencia y corrección en el contrato; no permitir
cambio directo de estado por escritura RPC para simular el efecto.
