# Reparaciones ARG · Registro y custodia

Fuente candidata20.0.1.0.0, sin instalación acreditada. Addon opcional arg_pyme_reparaciones,
dependencias ARG Ventas/Stock/Documentos, sin dependencia del núcleo hacia esta especialización.
Odoo20 usa ir.access.csv con modelos operativos y columnas operation/domain; no importar ACL de18.

## Fuentes de verdad

arg.pyme.repair.case contiene identificación del equipo ajeno, cliente, problema y estado del parte.
No es producto, quant, lote ni movimiento de existencias. arg.pyme.repair.event conserva los hechos
receive, diagnose, cancel y return, únicos por parte/tipo en este incremento no repetible.
No se almacena un saldo, costo o stock paralelo. Los futuros efectos se enlazarán al motor nativo.

REP usa la identidad/secuencia documental común por compañía, sin reiniciar ni renumerar historia.
El instalador extiende _ensure_companies; sudo sólo configura tipos/secuencias, nunca un parte.
El evento es inmutable y su fábrica privada usa identidad de objeto Python, sin flag JSON confiable.
Antes de crear evidencia se eliminan default_* heredados del contexto.

## Acciones y permisos

Operación Reparaciones ARG implica Operador ARG. Administrador ARG implica este rol; no se otorgan
Ventas/Contabilidad/Stock por recibir un equipo. El menú padre Ventas admite el rol de Reparaciones
para mostrar ese destino; las ACL de otros modelos se conservan. Capacidad combinable en una persona.

Cada mutación bloquea la fila del parte con UPDATE de auditoría, después de comprobar acceso,
rol y compañía. Esto serializa edición y transición en el aislamiento de PostgreSQL/Odoo.
Sólo las acciones privadas de servidor escriben estado; create rechaza estados adelantados y hechos
inyectados mediante valores o defaults. Un callback público no puede modificar evidencia existente.
Repetir recepción/diagnóstico/cancelación ya registrados no repite su hecho ni retrocede estado.
Devolución repetida exige misma fecha/constancia; otra constancia produce un error sin efectos.

Las reglas globales filtran compañías permitidas. La devolución por asistente vuelve a comprobar
permisos/estado del parte; abrir un diálogo no reserva ni cierra custodia. Fecha real de devolución
no anterior al último hecho ni futura. Fecha inicial context_today, explícitos existentes conservados.

## Impresión y consulta

Informe propio sin tabla de precios vacía; usa web.external_layout y la compañía del parte.
Contenido del usuario mediante t-field/t-out, sin t-raw. Verifica acceso documental y conserva
marca de ejemplo, borrador, diagnóstico no registrado y constancia de retiro. Los ejes se derivan
de eventos, sin inferir trabajo/facturación aún no implementados. Los listados se paginan en servidor.

## Límites de entrega

No se instalaron ni ejercitaron estas vistas/acciones. AST/XML/manifest/secretos y revisión estática
son controles técnicos separados de instalación, render PDF y QA. Falta completar puentes a PRE/PED,
autorización, intervención, consumos/devoluciones de repuestos, horas, entrega final, factura, hechos
de informes y correcciones explícitas; ver [tareas completas](../../specs/018-reparaciones/tasks.md).
