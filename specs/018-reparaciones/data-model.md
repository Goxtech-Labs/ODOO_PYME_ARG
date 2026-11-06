# Modelo conceptual · Reparaciones y servicio técnico ARG

Parte de reparación: cliente, equipo ajeno, marca/modelo/serie opcionales según identificación, síntoma, diagnóstico, fechas y autorización. Intervención: técnico, trabajo, horas y repuestos con movimientos. Custodia: recepción/entrega del equipo del cliente, separada de existencias propias.

## Fuentes y validaciones

Consumir/devolver repuestos mediante stock nativo; mano de obra como servicio; facturar desde el documento comercial vinculado sin duplicar pedido ni consumo.

- El equipo del cliente no aumenta stock propio ni su valoración.
- Confirmar el diagnóstico no factura ni consume repuestos.
- Cada consumo, devolución y factura conserva su origen por línea.
- Garantía y presupuesto aceptado son condiciones explícitas; no se inventan por fecha.

Identificación documental: REP para parte propio, PTM para trabajo de servicios; PRE/PED/REM/FAC existentes. Compañía obligatoria en transacciones; relaciones
compatibles con compañías permitidas. Cantidades/importes usan precisión monetaria/unidad nativa.
Fechas iniciales usan contexto de usuario; las históricas y externas conservan origen. Eventos incluyen
actor/fecha/origen, clave idempotente y efecto nativo; no almacenar residuales alternativos.

## Transiciones

Recepción → diagnóstico → presupuesto vinculado → autorización → trabajo → listo → entrega; facturación y cobro por ejes independientes.
Cada transición declara precondición, actor, efectos, evidencia y corrección en el contrato; no permitir
cambio directo de estado por escritura RPC para simular el efecto.

## Primer incremento de código

arg.pyme.repair.case: fecha de recepción, cliente, equipo descriptivo, síntoma; marca/modelo/serie,
accesorios y condición opcionales; diagnóstico y observaciones. Estados draft/received/diagnosed/
returned/canceled. returned significa exclusivamente devolución sin reparación en este incremento.
No representa entrega de trabajo terminado ni garantía cumplida. Estado, identidad y eventos protegidos.

arg.pyme.repair.event: parte/compañía, kind receive/diagnose/cancel/return, fecha efectiva, usuario,
momento de registro y evidencia. Un hecho por parte/tipo, inmutable; la devolución conserva quién
retira y motivo. Diagnóstico aún en edición se distingue del registrado. Sin cantidades de stock,
asientos ni importes de factura en estos modelos. Las siguientes etapas extienden el contrato.

## Ampliación1.1

REP agrega estados authorized/in_progress/ready/delivered. quotation_root_id enlaza una única
familia PRE; cada revisión conserva arg_repair_case_id. PED deriva el vínculo y su evento order
conserva Many2one real. authorization_ids y worklog_ids son relaciones protegidas, no formularios
alternativos de contabilidad. Facturas/REC conservan sus modelos y origen nativos.

arg.pyme.repair.authorization: una por PED, fecha/autoriza/constancia/cobertura/actor y términos
congelados. Garantía declarada no altera precios. arg.pyme.repair.intervention identifica PTM,
fecha/caso/línea de servicio/cantidad/unidad/persona/nota y estado draft/confirmed/reversed/canceled;
confirmación/reversión preservan actor/fecha/motivo y actualizan cumplimiento nativo con trazabilidad.

Eventos agregan order/authorize/start/ready/resume/deliver/work_correction y request_key único por
caso. Migración conserva los anteriores con clave legacy-id y retira unicidad caso/tipo, para
permitir ready/resume repetibles sin reejecutar solicitudes antiguas. No duplica efectos de stock
ni de cobro; repuestos desde movimientos reales actuales, servicios desde PTM vigentes.

## Ampliación1.2

Eventos receipt_correction/diagnosis_correction conservan campo, antes/después, etiquetas y motivo.
Snapshot completo y clave inmutable en wizard; replay no reescribe el valor actual. Date/partner sólo
antes de raíz PRE y con custodia abierta; datos esenciales no se vacían. Diagnóstico rectificado no
modifica acuerdos existentes. Estado comercial, cantidades nativas y dinero no cambian por corregir.

Caso agrega previous_case_id/followup_key protegidos y únicos por solicitud. Event.related_case_id
enlaza al REPdraft preparado para nueva visita desde custodia terminada. Copia sólo identificación
estable/cliente, registra nuevo problema y fecha propuesta. No comparte identidad, trabajo ni acuerdos;
otro REP se recibe y presupuesta independientemente. Las relaciones anteriores no se retargetean.
