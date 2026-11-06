# Herramientas de preparación de ejemplo

seed_demo.py se ejecuta dentro de `odoo shell`, nunca como addon de negocio ni contra otra base.
Requiere una base nueva `arg_demo`, una sola compañía y `l10n_ar` ya instalado. Rechaza documentos de negocio existentes, incluidos archivados. Fija la compañía principal antes de escribir propiedades o costos.
Requiere `ARG_DEMO_PASSWORD` (16 caracteres o más), `ARG_DEMO_LOGIN`, `ARG_DEMO_BASE_URL` y `ARG_DEMO_ACK_EXAMPLES=1`, provistos por el operador desde un archivo protegido. La URL debe ser el origen HTTP/HTTPS de su propia instancia. No se distribuyen credenciales ni dominio obligatorios.
El cargador completo necesita Contabilidad, Stock y listas de precios. El perfil de servicios sin Stock se instala por separado según [la guía](../docs/ejemplos/servicios.md); este cargador no se ejecuta allí.
No pasar secretos por argumentos visibles de proceso ni copiarlos a archivos del repositorio.
El loader crea maestros con XML IDs, no operaciones fiscales, documentos publicados ni movimientos de stock.
Conservar cron y correo desactivados; al instalar addons revisar que no se hayan reactivado registros.

Runtime y operación en docs/tecnica/ENTORNO-DEMO.md y OPERACION-Y-RECUPERACION.md.
No ejecutar este cargador sobre datos productivos ni interpretar sus maestros como validación de circuitos ARG.

seed_finance_demo.py se ejecuta por odoo shell sólo en arg_demo identificado como ejemplo, sin asientos/pagos/REC/OPA existentes. Crea diarios Caja/Banco y medios/cuentas de ejemplo, configura predeterminados y desactiva cron/correo; no registra operaciones. Rechaza sobrescribir configuración personalizada. En instalaciones nuevas crear PostgreSQL con template0/UTF8 explícito: no heredar SQL_ASCII de template1.

`configure_public_contacts.py` aplica un perfil JSON elegido mediante `ARG_PUBLIC_CONTACTS_JSON`
dentro de `odoo shell`. Valida web, canal, correo, WhatsApp y canal principal mediante los campos
de Ajustes, y escribe sólo esos cinco parámetros. No llama al guardado global de Ajustes, no
configura proveedores ni envía mensajes. El perfil público elegido para ARG está en
[canales.json](../docs/comunidad/canales.json); cada operador puede utilizar su propio perfil.

## Revisión aislada del circuito de Ventas

`qa_sales_flow.py` documenta y ejecuta el caso ficticio de la entrega0.1.3-dev. Requiere base
`arg_demo` con modo de ejemplo, usuario de gestión y contenedor sólo con interfaz loopback,
correo/cron desactivados y `ARG_QA_SALES_ISOLATED=1`. Nunca ejecutarlo en la demo del titular.

Invocarlo dentro de `odoo shell` sin HTTP/cron, pasando `ARG_QA_SALES_PHASE` en este orden:
`metadata`, `quote`, `order`, `delivery`, `invoice`, `checks`, `reports`. Cada fase exitosa confirma
su transacción y emite `ARG_QA_RESULT`. Crea documentos ficticios, apertura de inventario, entrega
parcial y factura interna no fiscal; conservar snapshot previo y evidencia, no limpiar producción.
No envía mensajes ni solicita CAE. [Resultados y límites](../docs/entregas/INTERFAZ-Y-VENTAS.md).

## Ejemplos de Valores ARG

`seed_values_demo.py` se carga dentro de `odoo shell` por un administrador, con
`ARG_VALUES_ACK_EXAMPLES=1` y `ARG_VALUES_COMPANY_ID` explícito, exclusivamente en arg_demo y
compañía en modo Ejemplo. Requiere Valores20.0.1.1.0 y Administración20.0.1.1.3. Crea una cuenta,
diario/medio nuevos, dos contactos sin CUIT inventado y un CHQ ficticio en borrador. No crea REC,
pago, asiento ni movimiento de stock; no cambia cron/correo ni los medios habituales de la empresa.
Se detiene si el perfil existente pertenece al titular o si las referencias fueron personalizadas.
Repetir no restablece un cheque que el usuario ya recibió o canceló. Los XMLIDs arg_demo.values_*
identifican el lote para inventariarlo; no borrar documentos numerados ni valores utilizados.
La carga de maestros/borradores y la QA de un circuito financiero son etapas distintas.

`seed_values_delivery_demo.py` amplía esos ejemplos después de instalar Valores20.0.1.2.0 y
Administración20.0.1.1.4. Requiere `ARG_VALUES_DELIVERY_ACK_EXAMPLES=1` y compañía explícita en modo
Ejemplo, así como los maestros del cargador anterior. Crea perfiles nuevos de salida, cuenta de
obligación, cuenta bancaria ficticia identificada, proveedor y un cheque propio en borrador.
No crea OPA/pagos/asientos/stock ni cambia cron/correo. Rechaza perfiles ajenos o referencias
personalizadas, y no restablece borradores que el usuario ya utilizó. Aún no ejecutado en este incremento.

## Ejemplo de recepción de equipo

`seed_repairs_demo.py` requiere Reparaciones ARG instalado, administrador ARG, base arg_demo,
`ARG_REPAIRS_ACK_EXAMPLES=1` y `ARG_REPAIRS_COMPANY_ID` en modo Ejemplo. Crea un cliente ficticio
y un REP en borrador, con equipo descriptivo y síntoma; no recibe el equipo ni registra diagnóstico,
movimiento, factura, pago o mensaje. No cambia configuración/cron/correo ni restablece un parte ya
utilizado. Referencias arg_demo.repairs_* se conservan; modelo/compañía inconsistentes detienen la
carga. Está preparado, no ejecutado; no equivale a QA de reparaciones.

El empaquetador valida operaciones canónicas de ir.access.csv de Odoo20, además de manifest,
AST/XML/JS y secretos. Ese control evita combinaciones como rc; no evalúa permisos en un runtime.
