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

Identificación documental: CHQ y PAG implementados para registro; VMO / LOP / TRB propuestos; REC y OPA existentes se conservan. Compañía obligatoria en transacciones; relaciones
compatibles con compañías permitidas. Cantidades/importes usan precisión monetaria/unidad nativa.
Fechas iniciales usan contexto de usuario; las históricas y externas conservan origen. Eventos incluyen
actor/fecha/origen, clave idempotente y efecto nativo; no almacenar residuales alternativos.

## Transiciones

Recepción → cartera → endoso/entrega, depósito o negociación → liquidación o rechazo; propio → emisión registrada → entrega → débito o devolución.
Cada transición declara precondición, actor, efectos, evidencia y corrección en el contrato; no permitir
cambio directo de estado por escritura RPC para simular el efecto.

## Esquema implementado: registro inicial

`arg.pyme.value.instrument`: fecha contextual, tercero, tipo cheque/pagaré, importe nominal y moneda;
origen propio/terceros y soporte con valores iniciales. Datos del título en sección secundaria:
clase común/diferido, número, identificador electrónico, emisión/vencimiento, librador/firmante,
identificación del firmante, beneficiario, cuenta bancaria nativa opcional y snapshots de banco/cuenta.
Compañía y código corto correlativo se fijan al guardar por el contrato documental ARG.
El nominal positivo se comprueba con precisión monetaria. El registro no puede cambiar de compañía
o tipo después de numerarse. No se elimina ni duplica; puede cancelarse conservando su identidad.

`identity_key` es una huella de los identificadores conocidos, única por compañía cuando puede
calcularse. Un borrador incompleto puede carecer de clave. Completar la identidad será precondición
del uso financiero; no confundir esta admisión de borradores con habilitación para recibir títulos.

`arg.pyme.value.event`: instrumento/compañía, actor y fecha del servidor, clase de evento,
UUID de operación, huella y payload. Eventos actuales: creado, modificado y cancelado en borrador.
No admiten edición o borrado. Las modificaciones conservan los nombres de campos cambiados;
esta base no ofrece una reconstrucción histórica completa de todos sus valores anteriores.

Estados actuales: `draft` → `canceled`. El nominal puede corregirse mientras permanece en borrador.
La inmovilidad después de una operación financiera confirmada, reservas, liquidaciones, rechazos,
transmisiones y efectos nativos aún requieren US2; no están representados por esos dos estados.
