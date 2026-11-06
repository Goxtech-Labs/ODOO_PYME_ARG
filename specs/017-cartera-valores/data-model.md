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

## Esquema histórico implementado20.0.1.0.0: registro inicial

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

## Incremento financiero implementado20.0.1.1.0

El esquema anterior de registro describe20.0.1.0.0. Ahora `receipt_line_id` vincula instrumento a un
único medio de REC, con pago/asiento nativos. `financial_confirmed_at` fija la inmovilidad de términos,
incluso dentro del motor; `portfolio_account_id` conserva la cuenta efectiva del pago recibido.
`deposit_journal_id`/`deposited_on` identifican presentación sin efecto monetario; `settlement_move_id`
y `rejection_move_id` enlazan reclasificación e inverso. Los eventos añaden fecha efectiva/constancia,
referencias nativas y huella de la solicitud dentro del payload inmutable.

Estados actualmente operables para cheque de tercero en papel:
borrador → cartera → depositado → acreditado completo; cartera/depositado → rechazado;
cartera → recepción revertida mediante REC. El pagaré sigue en borrador/cancelado. Recibido no implica
acreditado. El original rechazado/retornado conserva número y nominal, pero no crédito reutilizable.

El medio exclusivo de compañía requiere cuenta conciliable de activo corriente distinta de banco,
y no puede ser el habitual de caja ni tener pagos históricos anónimos. Se bloquea el uso nativo de ese
medio sin instrumento, incluidos método calculado, edición posterior y publicación. Pagos, asientos,
apuntes y conciliaciones vinculados tienen guardas, además de permisos nativos y de Administración ARG.

Los hooks opcionales de Administración seleccionan pagos/importes activos y validan por línea.
`total` conserva el nominal original del REC; `corrected_value_amount` informa los instrumentos
revertidos. Libre/aplicado y partial_ids excluyen sus pagos, evitando que la conciliación con un inverso
se lea como nueva aplicación o saldo libre. Dinero en facturas: valor pendiente0; nominal totalmente
acreditado aporta la aplicación nativa demostrada. Acreditaciones parciales/atribución aún pendientes.

Son campos y código instalados técnicamente en aislado; el comportamiento financiero queda para QA
posterior. OPA, ECHEQ, transmisiones, negociación y resto del contrato siguen abiertos.

## Desarrollo1.2: efecto por rol y transmisión

Código preparado, sin instalación nueva. Instrumento añade reserva/línea de salida actual y lista de
medios históricos. Estados: reservado, entregado a tercero, propio entregado, propio debitado,
propio devuelto, devuelto en revisión y entrega con cierre informado. Disponibilidad, tenencia y
nominal con seguimiento son indicadores separados, sin suma entre monedas ni duplicación por título.

Cada línea conserva transmisión, cláusula declarada, constancia y alcance; inverso, débito y estado/
fecha de seguimiento son efectos internos protegidos. Pago nativo tiene rol y línea estables; legacy1.1
se identifica sólo por su relación histórica demostrada. Inverso por línea sustituye la clasificación
incorrecta por estado global cuando el mismo instrumento pasó por REC y OPA.

La reserva tiene una sola línea propietaria; no crea efecto monetario. La primera entrega propia
fija sus condiciones y cuenta de obligación/banco. Crédito de cartera de tercero se concilia con la
recepción. Débito propio reclasifica obligación y banco. Devolución/rechazo revierte sólo OPA y conserva
REC. Seguimientos viven por transmisión y se cierran uno a uno; el nominal del instrumento se muestra
una vez si hay seguimientos abiertos y conserva bandera de alcance desconocido.

Ver contrato [OPA/salidas](contracts/salidas-opa.md); QA y promoción posteriores.
