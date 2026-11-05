# Modelo conceptual · Fabricación y artículos compuestos ARG

Lista de materiales versionada por condiciones nativas; orden de fabricación; cantidades previstas/reales, merma y subproductos opcionales; relaciones a movimientos.

## Fuentes y validaciones

Usar orden, consumos, producción, lotes y valoración nativos. Un kit comercial no registra producción ficticia.

- No escribir quants ni inventar un segundo libro de materiales.
- Fabricación parcial conserva cantidad pendiente y origen de componentes.
- Un kit y un producto fabricado no activan simultáneamente doble consumo.
- Un cambio de receta no modifica producción ya terminada.

Identificación documental propuesta: FAB propuesto; movimientos de stock nativos. Compañía obligatoria en transacciones; relaciones
compatibles con compañías permitidas. Cantidades/importes usan precisión monetaria/unidad nativa.
Fechas iniciales usan contexto de usuario; las históricas y externas conservan origen. Eventos incluyen
actor/fecha/origen, clave idempotente y efecto nativo; no almacenar residuales alternativos.

## Transiciones

Preparación → disponibilidad → orden → consumos/producción efectivos → terminación o cancelación.
Cada transición declara precondición, actor, efectos, evidencia y corrección en el contrato; no permitir
cambio directo de estado por escritura RPC para simular el efecto.
