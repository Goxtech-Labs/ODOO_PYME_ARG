# Valores ARG · recibos con cheques en papel

La ficha conserva **fecha → tercero → documento → importe**. Propone hoy según la zona horaria
y la moneda de la compañía inicial/contextual. Los valores explícitos, incluso vacíos, se conservan.
Si cambia manualmente de compañía durante la preparación, revise la moneda antes de guardar.
Datos del título y observaciones quedan en pestañas. El número CHQ/PAG se asigna al guardar.

## Configuración inicial

En la compañía, pestaña Administración ARG, configure un medio exclusivo para recibir cheques.
Necesita diario bancario, método manual de entrada y cuenta conciliable de valores a depositar
(tipo activo corriente), diferente de la cuenta bancaria. No reutilice el medio habitual de caja/banco
ni uno que ya tenga pagos sin instrumento. La configuración no conecta con ninguna entidad financiera.

La instalación no modifica diarios ni cuentas existentes. Hay un cargador optativo de ejemplos:
[seed_values_demo.py](../../ops/seed_values_demo.py). Requiere arg_demo, compañía explícita en modo
Ejemplo y confirmación mediante variable de entorno. Crea maestros propios y un cheque ficticio en
borrador; no publica recibos/asientos ni cambia cron o correo. Repetirlo conserva los registros usados.

## Preparar el recibo

1. Abra un recibo desde una factura publicada o desde Administración. Revise fecha y cliente.
2. Agregue el efectivo u otros medios habituales con su importe.
3. En otra línea seleccione el cheque del mismo cliente y moneda. Se proponen su nominal completo
   y el medio exclusivo de valores. Puede abrir una ficha nueva para completarlo.
4. Antes de confirmar, complete banco, código bancario conocido, cuenta y número del título,
   librador, emisión y fecha de pago. El borrador admite datos incompletos; la recepción los requiere.
5. Confirme con permiso Responsable Administración ARG. Cada medio genera su pago nativo y
   aplica deuda mediante conciliación. Sin facturas seleccionadas, queda crédito a cuenta.

Un mismo cheque no puede recibirse dos veces. Después de recibirlo conserva nominal, identidad y
condiciones; las correcciones se vinculan al original. Un pagaré continúa como registro de borrador.

## Depósito, acreditación o rechazo

Desde el cheque recibido abra **Operación de cheque**. Indique fecha y constancia/motivo:

- **Depósito:** elija banco destino. Cambia a pendiente de acreditación y no genera dinero ni otro recibo.
- **Acreditación completa:** use la constancia del banco. Reclasifica valores a banco con un asiento
  nativo y concilia cartera; no vuelve a aplicar la factura.
- **Rechazo:** disponible antes de acreditar o transmitir el cheque. Revierte únicamente el pago de
  ese instrumento y reabre su deuda aplicada, conservando otros medios del recibo. El cheque rechazado
  queda fuera del saldo reutilizable y conserva su inverso/historia.

Ejemplo de comportamiento previsto, pendiente de QA: factura120000, efectivo20000 y cheque100000.
El recibo aplica120000 a deuda, con caja20000 y cartera100000; banco del cheque0. Depositar no cambia
esa deuda. Acreditar reclasifica100000. Rechazar antes de acreditar deja aplicado20000, deuda100000
reabierta y saldo reutilizable del cheque0. No hay reversión global del efectivo.

## Disponibilidad y límites

Versión20.0.1.1.0 instalada técnicamente sólo en el entorno aislado. La demo compartida sigue0.1.5.
No se ejecutó QA financiero/visual ni se afirma validado el ejemplo anterior.

Este incremento recibe cheques de terceros en papel y acredita su nominal completo. ECHEQ, cheques
propios, OPA con valores, reservas/endosos, custodia, descuento, acreditación parcial, devolución y
recuperación después de acreditación siguen en desarrollo. El banco no recibe instrucciones desde
estas pantallas. La constancia manual registra un hecho informado por el operador.

Tutorial específico: pendiente; [canal general Goxtech Argentina](https://www.youtube.com/@Goxtech_Arg).
[Contrato completo](../../specs/017-cartera-valores/contracts/cartera-argentina.md) · [Entrega](../entregas/017-rec-cheques.md)
