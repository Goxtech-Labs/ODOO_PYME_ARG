# Data model: Circuito Administración ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Recibo / orden | `arg.pyme.treasury.document` | REC/OPA, tercero, fecha, moneda, payment_ids y total | No mantener saldo paralelo |
| Pago | `account.payment` | payment_type, partner_type, journal_id, payment_method_line_id, amount, date, memo | Configurar outstanding_account_id; no asumir move_id siempre existente |
| Imputación | `account.partial.reconcile` | debit_move_id, credit_move_id, amount y importes en moneda | Saldo desde apuntes/residuales, nunca invoice_ids por sí solo |

## Estados, efectos y seguridad

- Estados nativos de pago Odoo20: draft, paid, reconciled, canceled y rejected; no usar posted como estado de pago.
- Usar account.payment.register y conciliación nativa; no escribir residuales manualmente.
- REC/OPA confirmado exige efectos contables verificables; separar borrador, confirmado, parcialmente aplicado, aplicado y revertido.
- Separar documento recibo de pago y account.move out_receipt/in_receipt, que no son recibos de cobranza.
- No almacenar tarjetas ni claves bancarias; las referencias de operación no ejecutan transferencias.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.

Entidad adicional: arg.pyme.treasury.audit.event, sólo lectura tras creación, sin unlink para operador; conserva aplicación/desaplicación y referencia de evento inverso, no saldo.

## Primer incremento: consulta US1

`account.move.line` recibe campos calculados no almacenados de presentación: importe original,
saldo orientado deuda+/crédito−, moneda compañía, número/tipo de origen y progreso de cancelación.
La granularidad es apunte/cuota; no se copia total de factura a cada vencimiento ni se guarda otro saldo.
Los importes de presentación usan aggregator=False y compute_sudo=False. La consulta exige asientos publicados,
conserva reglas nativas y permite filtrar/salir de Con saldo para consultar cancelaciones históricas.
Administración implica lectura contable nativa; no se agregan permisos de escritura en este incremento.
REC/OPA y auditoría se incorporaron con20.0.1.1.1; ver el incremento siguiente.

## Incremento1.1: medios y auditoría

arg.pyme.treasury.line conserva medio e importe y vínculo inmutable al pago nativo. arg.pyme.treasury.audit.event conserva payload histórico, actor/fecha, compañía/moneda y eventos inversos. Los tres wizards aplican, desaplican un conjunto JSON estable o revierten por fecha/motivo. Snapshot y eventos conservan historia; saldo vigente deriva de contabilidad. Estado propio del wrapper y eje de aplicación son independientes. Ver docs/tecnica/009-administracion.md.
