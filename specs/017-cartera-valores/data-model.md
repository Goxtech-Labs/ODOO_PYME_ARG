# Modelo conceptual · Cartera de valores y tesorería argentina

Instrumento: compañía, origen propio/tercero, soporte papel/ECHEQ, clase común/diferido, moneda, nominal, banco/cuenta libradora, número/identificador, librador, tercero entregante, beneficiario y fechas. Evento: operación, actor, fecha, instrumento, origen/destino, evidencia, estado externo y efecto nativo. Lote de pagos/transferencia: instrucciones y ejecuciones vinculadas. Pagaré: instrumento distinto con vencimiento y rol propio/tercero.

## Fuentes y validaciones

Separar nominal disponible, aplicación de deuda, dinero acreditado/debitado y exposición por recurso. REC/OPA multim medio usa cuentas transitorias de valores y conciliación nativa, nunca residuales escritos a mano.

- El nominal es positivo, en la moneda del instrumento, y no cambia después del primer evento confirmado.
- Un instrumento no puede estar reservado o comprometido simultáneamente por dos salidas.
- Transmitir el título no fracciona su identidad; imputar su importe a varias facturas es otra operación.
- El nominal en cartera no es dinero bancario disponible ni se vuelve a cobrar al liquidarlo.
- Evento confirmado es inmutable; reversión explícita enlazada conserva historia y revisa su efecto contable.
- La integración bancaria no se ejecuta desde un formulario de cartera ni se infiere de una referencia manual.

Identificación documental propuesta: CHQ / VMO / LOP / TRB / PAG propuestos; REC y OPA existentes se conservan. Compañía obligatoria en transacciones; relaciones
compatibles con compañías permitidas. Cantidades/importes usan precisión monetaria/unidad nativa.
Fechas iniciales usan contexto de usuario; las históricas y externas conservan origen. Eventos incluyen
actor/fecha/origen, clave idempotente y efecto nativo; no almacenar residuales alternativos.

## Transiciones

Recepción → cartera → endoso/entrega, depósito o negociación → liquidación o rechazo; propio → emisión registrada → entrega → débito o devolución.
Cada transición declara precondición, actor, efectos, evidencia y corrección en el contrato; no permitir
cambio directo de estado por escritura RPC para simular el efecto.
