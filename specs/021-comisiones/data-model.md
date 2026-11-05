# Modelo conceptual · Agentes y comisiones ARG

Agente como tercero/usuario vinculado; regla por agente/familia/producto con vigencia y prioridad; devengamiento por línea fuente; liquidación y ajustes; cuenta/pago nativo.

## Fuentes y validaciones

Base explícita por facturación neta o cobro efectivo aplicado; separar comisión devengada de pagada y conservar devoluciones/rechazos. Regla inicial propuesta por facturación neta, seleccionable por compañía antes de activar.

- Una línea fuente y regla no devengan dos veces por reintento.
- Una liquidación confirmada conserva base y porcentaje históricos.
- Un cheque recibido sin acreditar no es cobro efectivo para una regla basada en liquidez.
- La liquidación no envía dinero; la OPA conserva su propia ejecución.

Identificación documental propuesta: LIQ propuesto. Compañía obligatoria en transacciones; relaciones
compatibles con compañías permitidas. Cantidades/importes usan precisión monetaria/unidad nativa.
Fechas iniciales usan contexto de usuario; las históricas y externas conservan origen. Eventos incluyen
actor/fecha/origen, clave idempotente y efecto nativo; no almacenar residuales alternativos.

## Transiciones

Regla versionada → devengamiento por fuente elegida → propuesta → liquidación → pago por OPA → ajustes.
Cada transición declara precondición, actor, efectos, evidencia y corrección en el contrato; no permitir
cambio directo de estado por escritura RPC para simular el efecto.
