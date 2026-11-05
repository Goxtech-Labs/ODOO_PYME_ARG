# Modelo conceptual · Diseñador documental e informes ARG

Plantilla por compañía/tipo; versión inmutable activada; bloques y campos permitidos; vista previa; referencia de plantilla usada al emitir.

## Fuentes y validaciones

Diseñar presentación sin recalcular importes, cambiar hechos, ocultar requisitos fiscales necesarios ni ejecutar código arbitrario.

- La activación no reescribe documentos ni sus condiciones históricas.
- No aceptar Python/XML/QWeb arbitrario de un usuario de diseño.
- Importes y textos se escapan y las firmas/marcas respetan licencias y compañía.
- Un reporte mantiene grano, filtros y monedas aunque cambie su disposición.

Identificación documental propuesta: Plantilla/versiones, sin numeración de transacciones nueva. Compañía obligatoria en transacciones; relaciones
compatibles con compañías permitidas. Cantidades/importes usan precisión monetaria/unidad nativa.
Fechas iniciales usan contexto de usuario; las históricas y externas conservan origen. Eventos incluyen
actor/fecha/origen, clave idempotente y efecto nativo; no almacenar residuales alternativos.

## Transiciones

Plantilla borrador → vista previa con ejemplos → revisión → activar versión → imprimir/exportar con versión trazable.
Cada transición declara precondición, actor, efectos, evidencia y corrección en el contrato; no permitir
cambio directo de estado por escritura RPC para simular el efecto.
