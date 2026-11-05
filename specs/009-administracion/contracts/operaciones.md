# Contrato de operaciones: Circuito Administración ARG

**Alcance**: Recibos, órdenes de pago, cajas y cuentas corrientes con imputaciones claras y fuente contable única.

## Recorridos y datos mínimos

### Operación 1: Consultar deuda

Como responsable necesito ver qué se debe, por documento, vencimiento y moneda.

**Resultado**: Consultar facturas publicadas y saldos residuales separados por moneda y compañía.
**Excepción**: Excluir borradores y no sumar ARS con USD ni confundir una relación con una conciliación.

### Operación 2: Cobrar o pagar

Como operador necesito registrar importe y medio e imputarlo a documentos.

**Resultado**: Crear REC u OPA con un medio y aplicar un pago parcial conservando saldo pendiente.
**Excepción**: Permitir anticipo sin factura y exigir cuentas transitorias configuradas antes de contabilizar.

### Operación 3: Revisar caja y revertir

Como responsable necesito consultar movimientos y corregir con trazabilidad.

**Resultado**: Consultar caja por diario y fecha y revertir una aplicación conservando historial.
**Excepción**: Impedir borrar evidencia publicada y distinguir caja, banco, deuda y conciliación.

## Invariantes

- Estados nativos de pago Odoo20: draft, paid, reconciled, canceled y rejected; no usar posted como estado de pago.
- Usar account.payment.register y conciliación nativa; no escribir residuales manualmente.
- REC/OPA confirmado exige efectos contables verificables; separar borrador, confirmado, parcialmente aplicado, aplicado y revertido.
- Separar documento recibo de pago y account.move out_receipt/in_receipt, que no son recibos de cobranza.
- No almacenar tarjetas ni claves bancarias; las referencias de operación no ejecutan transferencias.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.

Contrato de estados y pendientes: [v1](../../../docs/tecnica/ESTADOS-Y-PENDIENTES.md). Aplicar pendiente/parcial/completo por eje y conservar cantidades/importes explicables.

## Anticipos y evidencia de desaplicación

Deuda existente: usar account.payment.register sobre apuntes elegibles.
Anticipo sin deuda: crear account.payment independiente y confirmar con métodos nativos/cuentas transitorias configuradas;
conciliar después al aplicar contra apuntes de facturas. No intentar abrir el wizard sin apuntes elegibles.
Antes de aplicar/desaplicar registrar evento inmutable arg.pyme.treasury.audit.event con actor, fecha,
compañía, moneda, importe y referencias de apuntes/documentos; enlazar evento inverso.
remove_move_reconcile elimina conciliaciones parciales: sus IDs solos no conservan historia.
El evento preserva evidencia, no calcula un saldo paralelo; saldo vigente siempre desde contabilidad nativa.

## Recibo argentino · definición del titular 2026-11-05

REC documenta el cobro de una o varias facturas y detalla efectivo, transferencias, cheques u otros medios
habilitados. Puede reunir varios medios y aplicaciones parciales. Conservar cobros a cuenta existentes.
Aplicar deuda no equivale a acreditar dinero en banco: un cheque aceptado entra en cartera con identidad
propia. Su liquidación posterior no genera otro ingreso comercial ni vuelve a cancelar la misma factura.
El incremento de valores deberá ampliar clasificación y evidencia del motor monetario antes de admitir
cheques; los medios manuales actuales no constituyen por sí solos ese soporte.
OPA conserva identidad y función de pago. Usar lotes de órdenes/transferencias para el uso práctico de
remesas; un pagaré jurídico, cuando se utilice, es un instrumento separado y no una OPA renombrada.
