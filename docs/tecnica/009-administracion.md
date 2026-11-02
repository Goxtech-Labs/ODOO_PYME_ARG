# Administración ARG — implementación20.0.1.1.1

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Depende de Base/UI/Terceros/Documentos ARG y account nativo. No depende de Ventas/Compras;
los adaptadores monetarios de esos circuitos usan un contrato opcional. No modifica el core.
Código e instalación técnica completados; QA funcional/visual y aceptación pendientes.

## Fuente nativa y granularidad

current_account.py extiende account.move.line con campos de presentación no almacenados,
compute_sudo=False y aggregator=False. La unidad es apunte/cuota, con importes originales y residuales
nativos, orientación receivable/payable y precisión de moneda. No mantiene una tabla de saldos.
List/form/search de sólo consulta, paginación50, sin sumatorios entre monedas y dominio publicado.

arg.pyme.treasury.document es un wrapper REC/OPA con código propio, tercero, compañía, moneda,
fecha, medios, facturas elegidas y referencias a account.payment/account.move/conciliaciones.
No es account.move de tipo out_receipt/in_receipt. Estado propio calculado desde sellos y efectos:
draft, confirmed, exception, canceled, reverted; aplicación es un eje separado.
Importes aplicado/libre derivan de contrapartidas nativas; snapshot preserva condiciones históricas,
no un libro alternativo de saldos. Medios positivos, finitos, máximo100, manuales caja/banco,
moneda compatible y payment_account_id explícito. FX requiere cotizaciones explícitas.

Deuda elegible usa account.payment.register y conciliación nativa; anticipo usa account.payment
directo y action_post nativo. Contexto de compañía explícito, defaults externos eliminados y permisos
del usuario conservados. Confirmar exige un pago y asiento publicado por medio, contrapartida correcta,
dos líneas con importes/moneda esperados y estado nativo paid/reconciled. Fallar revierte la transacción.
No se usa posted como estado de account.payment.

## Inmutabilidad, concurrencia e idempotencia

Cabecera y líneas se serializan con UPDATE efectivo del padre bajo el aislamiento PostgreSQL nativo;
una edición concurrente no puede introducir medios después de confirmar. Campos técnicos, defaults y
vínculos a pagos/asientos ARG están protegidos del RPC. Un token objeto privado habilita únicamente
el motor interno, sin sudo comercial. Guardas de pagos, asientos y apuntes impiden editar efectos por
rutas nativas alternativas; la conciliación nativa legítima conserva permisos y cambios derivados.

Aplicación posterior usa conciliación nativa al menor saldo/deuda, misma compañía/tercero, por vencimiento.
Desaplicación conserva IDs objetivo en JSON al abrir el diálogo: no pierde el conjunto al borrar parciales.
Cada operación lleva UUID y huella; reintento igual no duplica efecto y payload distinto se rechaza.
Reversión usa _reverse_moves con fecha/motivo, preserva pagos/asientos originales e identifica inversos.
Conciliación de liquidez contra banco exige revisión previa, no se borra silenciosamente.

arg.pyme.treasury.audit.event conserva evidencia inmutable con actor, fecha, compañía, moneda,
importes, IDs de extremos y vínculos inversos. Los hooks de account.partial.reconcile capturan evidencia
antes de unlink y resultado de aplicación. IDs de conciliaciones eliminadas no son el único historial.

## Atribución de dinero

money_application.py implementa el contrato opcional de ejes para FAC/FRC y PED/PPC. Usa parciales
nativos por lado factura y valida accesos sin sudo. Distingue efectivo de notas, compensaciones y FX.
Pagos simples exigen prueba de liquidez/contrapartida y moneda nominal. Descuento pronto pago se
atribuye por factura sólo con parcial real único e importe completo explicable; no por total nominal.
Un writeoff simple compatible puede prorratearse usando amount_currency L/C, nunca balances de compañía.
Casos ambiguos, pagos complejos o lectura insuficiente producen unknown/No determinado con importe
conocido y explicación; no un falso pendiente/cero. Residual0 no acredita caja.
El widget y QWeb comunes soportan este estado de calidad separado del avance pendiente/parcial/completo.

cash_report.py consulta AML publicados asset_cash y pagos registrados, sin agregaciones entre monedas.
Se distinguen efectivo, cuentas transitorias y efectos revertidos. Transferencias manuales son registro,
no ejecución bancaria. Las vistas listas preceden explícitamente las formas.

## Roles y ayuda

Operación Administración implica account.group_account_readonly (lectura contable nativa amplia).
Responsable Administración implica Operación, Responsable ARG y account.group_account_invoice;
Administrador ARG lo incluye. ACL y reglas globales por compañía en wrappers, líneas, eventos y wizards.
Confirmar/aplicar/desaplicar/revertir comprueban rol efectivo y acceso ORM. No sustituyen reglas por sudo.

La ayuda1.1 escrita es vigente. La guía US1 queda reemplazada, con enlace a la nueva. Migración1.1.1
conserva un video personalizado previo como por revisar; no borra URLs. Instalación limpia y upgrade
usan el mismo criterio de vigencia. YouTube/soporte requieren destinos reales antes de activación.

## Ejemplos y evidencia

ops/seed_finance_demo.py sólo admite arg_demo identificado como demo y sin documentos financieros.
Crea maestros Caja/Banco de ejemplo ARG, medios manuales y cuentas transitorias cuando faltan;
no sobreescribe personalizaciones ni registra pagos/asientos. Se identifica por XML IDs arg_demo.
Runtime, hashes, controles y límites en la [entrega](../entregas/009-administracion.md).
