# OPA, reserva y entrega de cheques ARG

Incremento del contrato,2026-11-05. Conserva todo cartera-argentina.md y los pendientes de017.

## Hechos independientes

Reserva identifica una única línea de OPA borrador y no crea pago. Confirmar OPA con constancia de
entrega usa el título completo y crea pago nativo: débito a proveedor, crédito a cartera de terceros o
a cheques propios pendientes. El cheque propio no debita banco en esa instancia. Su débito completo
posterior reclasifica la obligación a banco; no paga nuevamente la factura.

Toda aplicación, corrección, débito y seguimiento se vincula a la línea/pago de su rol: recepción,
salida de tercero o salida propia. Estado físico del instrumento no decide por sí solo qué deuda
reabrir. Una devolución/rechazo de salida corrige sólo el pago OPA; REC conserva sus aplicaciones.
La posterior recuperación del cliente es otro evento explícito sobre el REC, con su propio inverso.

## Reserva y condiciones

- Reservar/liberar requiere responsable, OPA borrador, compañía/moneda/nominal compatibles y título disponible.
- Confirmar puede reservar automáticamente dentro de la misma transacción. Otra OPA no puede usarlo.
- Cambiar/eliminar una línea reservada exige liberarla primero. Cancelar el borrador libera sus reservas.
- Terceros: recibidos, en cartera y sin depósito/salida activa. Propios: borrador o devuelto, cuenta
  registrada de la compañía y banco/método compatible, librador y beneficiario conocidos.
- Constancia y tipo de transmisión se requieren al confirmar. Endoso, cesión y entrega sin nuevo
  endoso son hechos distintos. Se declara la cláusula conocida del título; no se presume firma ni
  aceptación bancaria. Endoso estándar sobre título declarado no a la orden se deriva a cesión/perfil
  específico, sin negar las excepciones previstas en la ley.
- Nominal/identidad/condiciones se congelan al primer efecto confirmado, también en un cheque propio.

## Corrección, liquidez y exposición

Devolver una salida sin cobro bancario genera inverso del pago OPA, devuelve tenencia y conserva
historia. Un rechazo de salida devuelve el título como discutido, no disponible para reutilización.
Antes de reabrir REC debe existir devolución y ninguna salida activa. Ningún botón revierte cliente
y proveedor automáticamente. Una OPA íntegramente corregida puede cerrarse como revertida sin
crear inversos repetidos. La reversión general de OPA exige registrar antes la devolución de títulos.

Seguimiento de responsabilidad pertenece a cada transmisión y se cierra sólo con constancia explícita.
Su nominal no se suma varias veces por el mismo título ni se agrega a caja/banco/deuda. Alcance desconocido
se marca como tal; una declaración sin recurso no libera automáticamente el seguimiento. Pago informado
al tenedor de un cheque de tercero no es dinero ingresado en la compañía. El débito de un propio sí
puede explicar dinero aplicado al proveedor cuando su asiento y aplicación están demostrados.

Operaciones posteriores a débito/acreditación, parciales, negociación y ECHEQ continúan en su alcance
completo del plan, sin simularlas con devolución genérica. Conexiones externas sólo Integraciones ARG.

## Referencias y alcance de la implementación

La [Ley24.452 actualizada](https://www.argentina.gob.ar/normativa/nacional/ley-24452-14733/actualizacion)
distingue transmisión y modalidades del título; no se copia el proceso español ni se certifica validez
jurídica desde una constancia local. La elección del circuito estándar es una política del producto.
El [BCRA distingue la operatoria ECHEQ](https://www.bcra.gob.ar/echeq-o-cheque-electronico/), incluidos
roles y estados externos; este incremento de papel no los sustituye.

QA posterior: reserva simultánea, OPA con100000 sobre factura150000, devolución que reabre sólo OPA,
rechazo que no deja libre el valor, posterior recuperación REC explícita, débito propio sin doble pago,
y cierre de responsabilidad sin falso dinero del cliente. No ejecutar estos casos durante desarrollo.
