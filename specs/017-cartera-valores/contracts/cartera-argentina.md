# Cartera argentina: instrumento, deuda, liquidez y responsabilidad

Decisiones de producto 2026-11-05. Los estados siguientes son internos propuestos, no un catálogo bancario oficial.

## Hechos y dimensiones

| Hecho | Grano | Medidas y dimensiones |
| --- | --- | --- |
| Tenencia de valor | Instrumento y evento vigente | Nominal; compañía/moneda, propio/tercero, soporte, banco, librador, entregante, tenedor, custodio |
| Aplicación a deuda | Aplicación nativa vinculada a REC/OPA y línea de medio | Importe aplicado; factura/apunte, tercero, fecha y moneda |
| Movimiento de liquidez | Apunte nativo bancario/caja y evento de liquidación | Acreditado/debitado, cargos; fecha valor y moneda |
| Exposición | Instrumento con obligación/garantía pendiente | Nominal y alcance; librador, endosante, receptor, contraparte de negociación |

Las cuatro medidas no se suman para obtener un supuesto total de dinero. Un cheque puede estar fuera
de cartera por endoso y conservar exposición. Un pagaré no es un cheque ni una transferencia pendiente.

## Datos mínimos por momento

- Recepción: hoy propuesto, quién entrega, nominal/moneda e identidad del cheque. Banco, librador,
  número/cuenta o identificador ECHEQ, fechas y soporte se completan con evidencia; no inventar datos.
- REC: cliente, factura(s), medio(s) e importes. Si se recibe cheque, seleccionarlo/crearlo una sola vez;
  el mismo instrumento enlaza medio, cartera y eventos. Conserva saldo a cuenta cuando corresponda.
- Emisión propia: banco/cuenta propia, beneficiario, nominal, fechas y referencia real. Preparar el registro
  local no emite un ECHEQ en el banco; distinguir ambos hechos con evidencia.
- Entrega/endoso: valor completo, destinatario y documento/operación de origen; tipo de transmisión,
  fecha y evidencia. Distinguir entrega física, endoso, cesión y mandato; respetar cláusulas aplicables.
- Depósito: banco/cuenta destino, fecha y constancia; acreditación requiere evento/constancia distinto.
- Venta/descuento: contraparte/contrato, nominal, recurso/garantías, gastos discriminados, neto y fecha.
  Guardar referencia al instrumento; no contabilizar una venta de mercadería por negociar un cheque.

## Matriz de transiciones

| Acción | Precondición | Resultado de cartera | Efecto monetario y corrección |
| --- | --- | --- | --- |
| Registrar recepción | Identidad única y sin salida vigente incompatible | Recibido, pendiente de aceptación si ECHEQ lo requiere | Sin crédito bancario por registrarlo |
| Confirmar REC | Facturas/medios coherentes, usuario autorizado, cuentas/estado válidos | Cartera y vínculo al medio | Aplicar deuda con motor nativo; valor transitorio, efectivo real separado |
| Reservar para OPA | Valor disponible, compañía/moneda compatible | Comprometido para una sola salida | No cancelar deuda por reservar |
| Entregar/endosar | Disponibilidad y transmisión permitida, destinatario/evidencia | Fuera de cartera operativa o pendiente de aceptación externa | OPA puede aplicar deuda; responsabilidad separada, sin simular débito bancario |
| Custodiar | Valor apto y custodio identificado | En custodia | No dinero acreditado; rescate como evento específico |
| Depositar/presentar | Valor disponible/custodiado y cuenta destino válida | En gestión/presentado | Pendiente de acreditación, sin nuevo REC |
| Acreditar/cobrar | Constancia y vínculo a presentación | Liquidado por importe real | Reclasificar valor y banco; pago parcial bancario, si ocurre, conserva saldo y evidencia |
| Negociar/descontar | Contrato, contraparte y perfil contable configurados | Transferido/en negociación | Separar nominal, neto, gastos y exposición; no baja contable automática por etiqueta sin recurso |
| Liquidar negociación | Evidencia del producido | Valor negociado con liquidación enlazada | Neto acreditado una vez; nominal no se duplica como ingreso |
| Rechazar | Hecho/constancia de rechazo y alcance conocido | Rechazado/en recupero | Corrección o reclamo vinculado al obligado pertinente, sin doble deuda ni reversión del efectivo ajeno |
| Devolver/recibir devolución | Custodia/tenencia y aceptación externa coherentes | Nueva tenencia por evento, misma identidad | Reversión específica según efecto anterior; no botón genérico de reset |

ECHEQ pendiente, rechazado o con restricciones externas conserva el estado original y su fecha. Una
solicitud de devolución, anulación o negociación no está cumplida sólo porque el servidor local la envió.
Timeout → incierto → consulta al proveedor antes de reintentar. Las operaciones manuales son constancias
de hechos realizados fuera del sistema, no emisiones electrónicas válidas por sí mismas.

## Invariantes de contabilización

1. Nominal positivo e identidad estable. No fraccionar transmisión de un mismo cheque entre dos salidas.
   El importe puede aplicarse a varias facturas dentro de un mismo cobro; un cobro parcial bancario es otro hecho.
2. Clasificar cada medio/evento: efectivo, transferencia en tránsito/ejecutada y valor pendiente/liquidado.
   Ampliar `money_application` antes de permitir cheques en REC/OPA; una cuenta transitoria no prueba liquidez.
3. Por defecto de producto, un REC confirmado con valor aceptado puede aplicar deuda en forma nativa,
   conforme a la definición del titular. Mostrar valor pendiente y exposición hasta liberación comprobada
   de la obligación según perfil/contrato; liquidar el producido de descuento no libera por sí solo exposición.
4. La acreditación posterior no cancela otra vez la factura. La conciliación y los asientos son nativos;
   los eventos explican su origen, sin escribir residuales ni otro saldo contable.
5. Rechazo de valor recibido: reconstruir aplicación/contrapartida afectada y proponer reversión/reclamo.
   No reabrir indistintamente factura del cliente y deuda al proveedor tras un endoso. Perfil de obligaciones
   y apuntes determina contraparte y evita deuda duplicada. Gastos de rechazo son conceptos separados.
6. Descuento con/sin recurso o desconocido se conserva como condición, no como presunción jurídica.
   El perfil define cuentas transitorias, garantías y tratamiento; sin perfil válido no contabilizar negociación.
7. Unicidad e idempotencia de evento por compañía/instrumento/operación; bloqueo de fila al comprometer
   y volver a comprobar disponibilidad antes de confirmar. Eventos/condiciones publicados no editables.
8. Reglas normativas/proveedor —fechas/plazos, monedas, límites, causales y capacidades— versionadas,
   no constantes universales copiadas de un manual. Ver [fuentes](../../016-expansion-argentina/research.md).
9. Adaptar por medio/evento `_arg_reverse`, `_compute_status`, `_compute_amounts` y `_compute_partials`
   de tesorería, además de `money_application`. El rechazo de cheque no llama a reversión global de REC.
   Un inverso conciliado no prueba aplicación vigente a factura ni deja el valor rechazado libre para reutilizar.
10. En cobros parciales de un valor aplicado a varias facturas, atribuir dinero a cada origen sólo con
    evidencia explícita. Sin ella mostrar No determinado y la parte conocida, sin prorrateo implícito.
    El producido del descuento es financiación, distinto de pago del librador y de cobro comercial.

## OPA, lotes, transferencias y pagarés

OPA puede incluir efectivo, transferencia, cheque propio o de tercero según perfil. El lote agrupa
instrucciones/OPA con ejecución parcial por línea; no crea un pago agregado duplicado. Transferencia
propia entre cuentas reclasifica liquidez y no cobra una factura ni paga otra vez un proveedor.
Referencia bancaria, fecha ordenada, fecha ejecutada y fecha acreditada son datos distintos.

Pagaré legal: registro aparte de emisión/recepción, vencimiento, tenencia, cancelación/negociación y
evidencia del título. No generar texto/firma con validez legal presumida. El uso cotidiano descrito como
remesa/pagaré se ofrece primero como orden/lote/transferencia; el instrumento formal se activa sólo cuando
la pyme realmente lo use y tenga configurado su circuito. Esto no elimina su alcance del plan.

## Ejemplos de aceptación posteriores

- Factura120000 → REC20000 efectivo+cheque100000: deuda aplicada120000, caja20000, cartera100000,
  banco del cheque0. Depósito no cambia deuda; acreditación100000 no duplica cobro comercial.
- Mismo caso con rechazo: queda cobro efectivo20000 y reclamo/efecto reversible100000, con referencias,
  sin borrar REC ni duplicar el valor. En perfil que reabre factura: deuda100000, aplicación vigente20000
  y libre reutilizable del cheque0. Si genera reclamo distinto, no crear también un segundo deudor.
  Regla aplicada debe explicarse desde apuntes y eventos.
- Dos OPA intentan usar el mismo cheque: sólo una reserva/confirma; la otra recibe error accionable.
- Cheque100000 endosado por una OPA contra factura150000: saldo50000; no crear otro cheque50000.
- Negociación nominal100000 con neto96000 y gastos4000: tres cifras distintas, sin afirmar costo fiscal
  ni tasa anual. Perfil/cargos discriminados; exposición depende del contrato, no de la salida de cartera.
- Importar dos veces una constancia ECHEQ conserva un evento. Un timeout no permite segundo endoso.
- Lote con tres transferencias y una fallida: dos ejecuciones y una pendiente, sin marcar todo pagado.
