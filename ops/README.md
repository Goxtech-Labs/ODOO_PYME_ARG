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
