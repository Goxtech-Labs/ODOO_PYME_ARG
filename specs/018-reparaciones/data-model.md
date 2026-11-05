# Modelo conceptual · Reparaciones y servicio técnico ARG

Parte de reparación: cliente, equipo ajeno, marca/modelo/serie opcionales según identificación, síntoma, diagnóstico, fechas y autorización. Intervención: técnico, trabajo, horas y repuestos con movimientos. Custodia: recepción/entrega del equipo del cliente, separada de existencias propias.

## Fuentes y validaciones

Consumir/devolver repuestos mediante stock nativo; mano de obra como servicio; facturar desde el documento comercial vinculado sin duplicar pedido ni consumo.

- El equipo del cliente no aumenta stock propio ni su valoración.
- Confirmar el diagnóstico no factura ni consume repuestos.
- Cada consumo, devolución y factura conserva su origen por línea.
- Garantía y presupuesto aceptado son condiciones explícitas; no se inventan por fecha.

Identificación documental propuesta: REP / PTM propuestos; PRE/PED/REM/FAC existentes. Compañía obligatoria en transacciones; relaciones
compatibles con compañías permitidas. Cantidades/importes usan precisión monetaria/unidad nativa.
Fechas iniciales usan contexto de usuario; las históricas y externas conservan origen. Eventos incluyen
actor/fecha/origen, clave idempotente y efecto nativo; no almacenar residuales alternativos.

## Transiciones

Recepción → diagnóstico → presupuesto vinculado → autorización → trabajo → listo → entrega; facturación y cobro por ejes independientes.
Cada transición declara precondición, actor, efectos, evidencia y corrección en el contrato; no permitir
cambio directo de estado por escritura RPC para simular el efecto.
