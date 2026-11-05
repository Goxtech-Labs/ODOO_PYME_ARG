# Modelo conceptual · Punto de venta ARG

Sesión, pedido/ticket, medios, diferencias de caja, factura vinculada y devolución nativas; relación documental ARG sin segunda contabilización.

## Fuentes y validaciones

Conservar pagos, stock, impuestos y asientos del POS nativo; puentes ARG sólo enlazan y clasifican. No crear REC duplicado por cada pago ya registrado por POS.

- Un cobro y un movimiento POS se registran una sola vez aunque exista enlace ARG.
- Un ticket no acredita autorización fiscal.
- Devolución y devolución de dinero son efectos separados con origen.
- La cuenta de demo no determina los permisos definitivos de cajero.

Identificación documental propuesta: Identidad de tickets nativos preservada; no reutilizar FAC para ticket no fiscal. Compañía obligatoria en transacciones; relaciones
compatibles con compañías permitidas. Cantidades/importes usan precisión monetaria/unidad nativa.
Fechas iniciales usan contexto de usuario; las históricas y externas conservan origen. Eventos incluyen
actor/fecha/origen, clave idempotente y efecto nativo; no almacenar residuales alternativos.

## Transiciones

Sesión → venta → cobro → ticket/factura según caso → devolución → cierre y conciliación.
Cada transición declara precondición, actor, efectos, evidencia y corrección en el contrato; no permitir
cambio directo de estado por escritura RPC para simular el efecto.
