# Reparaciones ARG · Registro y custodia

Fuente candidata20.0.1.2.0, sin instalación acreditada. Addon opcional arg_pyme_reparaciones,
dependencias arg_pyme_ventas_stock y Documentos, sin dependencia del núcleo hacia esta especialización.
Odoo20 usa ir.access.csv con modelos operativos y columnas operation/domain; no importar ACL de18.

## Fuentes de verdad

arg.pyme.repair.case contiene identificación del equipo ajeno, cliente, problema y estado del parte.
No es producto, quant, lote ni movimiento de existencias. arg.pyme.repair.event conserva los hechos
receive/diagnose/cancel/return/order/authorize/start/ready/resume/deliver/work_correction, únicos
por parte y clave de operación. ready/resume admiten nuevas solicitudes explícitas.
No se almacena un saldo, costo o stock paralelo. Los futuros efectos se enlazarán al motor nativo.

REP usa la identidad/secuencia documental común por compañía, sin reiniciar ni renumerar historia.
El instalador extiende _ensure_companies; sudo sólo configura tipos/secuencias, nunca un parte.
El evento es inmutable y su fábrica privada usa identidad de objeto Python, sin flag JSON confiable.
Antes de crear evidencia se eliminan default_* heredados del contexto.

## Acciones y permisos

Operación Reparaciones ARG implica Operador ARG. Administrador ARG implica este rol; no se otorgan
Ventas/Contabilidad/Stock por recibir un equipo. El menú padre Ventas admite el rol de Reparaciones
para mostrar ese destino; las ACL de otros modelos se conservan. Capacidad combinable en una persona.

Cada mutación bloquea raíces comerciales ordenadas y luego el parte con UPDATE de auditoría,
después de comprobar acceso, rol y compañía. La recepción sin Ventas sólo serializa metadata de
la raíz ya vinculada, sin leer ni cambiar condiciones financieras. Los efectos se mantienen en su motor.
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
de eventos y fuentes nativas por PRE/PED, sin prorratear dinero. Los listados se paginan en servidor.

## Puentes1.1

quotation_root_id se asigna internamente una vez por REP, con unicidad. El PRE y sus revisiones
conservan arg_repair_case_id; el PED deriva ese vínculo. Su creación conserva un evento order con
Many2one real: los controles usan referencias y verifican acceso, sin buscar y omitir pedidos ocultos.
El generador limpia default_*; vínculos no aceptan escritura ni preferencias ir.default del operador.

arg.pyme.repair.authorization conserva PED, fecha, quién autoriza, cobertura, constancia, actor,
hash y snapshot de términos. Una por PED; nuevos alcances usan otro pedido. No confirma ni pone
precios en cero. Confirmar PED exige autorización; iniciar valida sus condiciones y estado nativo.

Repuestos usan exclusivamente sale_stock. _action_done exige trabajo iniciado para salidas;
devoluciones conservan movimiento validado/línea y to_refund. El neto según clasificación nativa
outgoing/incoming no supera el autorizado ni queda negativo. En operaciones mixtas se bloquean
también raíces de otros movimientos antes de partes. No hay otro consumo ni escritura de quants.

PTM arg.pyme.repair.intervention admite servicios con qty_delivered_method manual. Confirmar
actualiza qty_delivered nativo; revertir recalcula desde PTM aún confirmados, con fecha/motivo.
Exige coincidencia entre PTM y cantidad nativa antes de cambiarla; no sobrescribe cantidades ajenas.
Cumplimiento/método no editables por RPC. Corrección posentrega conserva su constancia física.

Las líneas parten de cantidad cero y método calculado nativamente sobre new(), sin efectos;
se neutralizan defaults de cumplimiento, gasto y anticipo. Stock deriva el neto de movimientos
terminados actuales y retira accrual_entry_date de controles y efectos. Comprueba primero IDs de
la relación completa, acceso y compañía: un retorno oculto no se convierte en entrega completa.

Listo/entregar comprueban cumplimiento y cantidades confirmadas sin PED. Asistentes conservan
parte/modo/UUID; diálogos viejos no retoman una etapa nueva. Facturas, notas y REC usan operaciones
existentes. Los ejes de PRE/PED mantienen unidad/moneda/origen, sin otra suma financiera.

Migración1.0→1.1 asigna claves legacy-id a eventos antes de la nueva unicidad, retira unicidad
parte/tipo, registra PTM y señala guía anterior para revisar; conserva evidencia y texto/URLs del titular.

## Límites de entrega

No se instalaron ni ejercitaron estas vistas/acciones. AST/XML/manifest/secretos y revisión estática
son controles técnicos separados de instalación, render PDF y QA. Falta comprobar esta composición
y migraciones en runtime, cargar ejemplos y completar tutoriales;
ver [tareas completas](../../specs/018-reparaciones/tasks.md).

## Correcciones y continuidad1.2

repair_correction.py permite rectificar campos seleccionados mediante valor anterior/nuevo,
fecha/motivo/actor. Wizard captura snapshot y UUID en servidor; write no cambia caso/clave/snapshot.
Aplicar revalida responsable+Reparaciones+compañía, bloquea raíz/caso, compara snapshot y guarda
evento inmutable. Cliente/fecha sólo antes de PRE y durante custodia; fechas respetan hechos previos.
Datos de acuerdos comerciales permanecen congelados aunque se rectifique el texto del diagnóstico.

previous_case_id/followup_key se asignan sólo mediante fábrica privada, con unicidad de solicitud;
write/defaults externos no los inyectan. Seguimiento desde returned/delivered crea REPdraft con
identidad nueva y sólo datos estables, sin diagnóstico/condiciones físicas ni compromisos heredados.
Evento followup tiene Many2one real al hijo; replay comprueba acceso y devuelve ese registro sin
restablecer sus datos o estado. No hay reapertura implícita de la custodia anterior.

Reporte incluye correcciones y componente común document_axes. AccessError comercial se presenta
como unknown conservando _arg_custody_axes, sin sudo ni ceros inferidos. La migración1.2 sólo
actualiza la cadena de ayuda; columnas/relaciones nuevas son opcionales y no reescriben evidencia.
