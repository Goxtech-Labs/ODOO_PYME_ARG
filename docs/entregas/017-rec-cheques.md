# REC y cheques en papel · incremento de desarrollo · 2026-11-05

Código desarrollado: Valores20.0.1.1.0 y Administración20.0.1.1.3. Instalación técnica en aislado;
la demo compartida conserva0.1.5 y su composición. No se declara terminada la feature017.

## Comportamiento implementado

REC admite cheque en papel de tercero identificado por línea junto a otros medios. La recepción
crea pago/conciliación nativos con cuenta transitoria de cartera y conserva instrumento, tercero,
moneda, nominal y condiciones. Depósito no crea dinero; acreditación completa reclasifica cartera
a banco y no vuelve a aplicar facturas. El rechazo previo a acreditación revierte sólo ese medio.

Los pagos corregidos quedan fuera de libre/aplicado y de aplicaciones vigentes del recibo; el nominal
original sigue visible con importe de valores revertidos. La reversión general no repite el inverso de
un valor ya rechazado. Un valor depositado/acreditado exige resolver su operación antes de revertir REC.
La presentación diferencia aplicación a deuda y dinero; un cheque pendiente aporta0 al dinero aplicado,
y uno acreditado íntegro puede aportar su aplicación nativa demostrada. No hay prorrateo parcial.

La extracción de hooks de Administración conserva el motor habitual para medios sin instrumento y
permite adaptar efectos por línea sin copiar toda la confirmación. Valores es una extensión opcional.
Método exclusivo, cuenta conciliable de activo corriente y registro de instrumento se validan en servidor;
un pago nativo no puede eludirlos omitiendo/cambiando su método. Contextos default_* se limpian antes
de habilitar motores internos; las marcas privadas no son booleanos utilizables por RPC.

## Evidencia y límites

Paquete250 archivos SHA2560f2b9be02eec6ed030168e1bf9637e761d07cebecd45e4a1ee29d9311b76bc1a.
[Composición candidata](../../composition/candidates/017-valores-rec.json), distinta de la
[composición de la demo](../../composition/versions.lock.json). Sin migrar transacciones de laboratorio.

AST/XML/JS/manifests y Gitleaks; revisión estática independiente por otra sesión de la misma
familia/cuenta. Dos hallazgos de contexto y método efectivo corregidos antes de instalar. Carga de
vistas/modelos, upgrade de ambos addons y arranque. Controles de metadatos y defaults sin confirmar
pagos, rechazos o acreditaciones. Esto no acredita QA funcional/visual, concurrencia real ni aceptación.

El cargador de ejemplos es optativo y no se ejecuta al instalar. Crea maestros nuevos y un borrador
ficticio identificado, con idempotencia por XMLID; no modifica configuración ajena ni liquidez/stock.
Se cargó sólo en aislado: cuenta/diario/medio propios, dos contactos ficticios y CHQ-000001 en
borrador;0pagos/asientos/stock nuevos. La carga de ejemplos no acredita QA del circuito financiero.

Pendientes del contrato: ECHEQ y su aceptación externa, OPA/propios, reservas y transmisiones,
custodia/devoluciones, negociación/descuento/recurso, acreditaciones parciales con atribución explícita,
recupero posterior, lotes/transferencias, pagaré formal, informes ampliados y tutorial. Ninguna integración
bancaria/fiscal/mensajería se activa por este incremento.

[Manual](../usuario/017-cartera-valores.md) · [Tareas](../../specs/017-cartera-valores/tasks.md)
