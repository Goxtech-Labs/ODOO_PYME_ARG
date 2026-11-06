# Correcciones y nuevas visitas · Reparaciones ARG

## Corrección registrada

Responsable con Reparaciones ARG selecciona dato, fecha, nuevo valor y motivo. El servidor captura
snapshot y UUID al abrir; no acepta sustituirlos por write. Antes de aplicar comprueba rol, compañía,
estado y snapshot completo bajo bloqueo raíz/caso. Si cambió la ficha se vuelve a abrir el diálogo.
Reintento de la misma solicitud devuelve éxito sin volver a escribir; constancia distinta se rechaza.

Campo permitido: fecha, cliente, equipo, problema, marca, modelo, serie, accesorios, estado recibido
o diagnóstico registrado. No cambia estado/compañía/identidad/trabajo/dinero mediante un nombre libre.
Campos esenciales permanecen completos; opcionales admiten vaciado explícito. Fecha efectiva no
futura ni anterior al último hecho. Cliente/fecha sólo antes de PRE y con custodia abierta; recepción
corregida no posterior a otros hechos. Diagnóstico aún no registrado se edita por su flujo ordinario.

Se conservan evento original y corrección con antes/después, etiquetas, actor y motivo. Rectificar
texto no modifica los acuerdos PRE/PED, trabajo, factura ni cobro. Un nuevo alcance usa sus acciones.
El informe muestra datos vigentes, historia y correcciones; no representa una factura fiscal.

## Nueva visita

Desde returned/delivered se prepara otro REP en borrador. Fecha propone hoy y no precede al fin
de custodia anterior; futura sólo permite preparar el borrador. Se pide el nuevo problema y se toman
cliente/equipo/identificación estables. No se copian diagnóstico, estado físico, accesorios, acuerdos,
trabajo, cobros ni identidad. Recibir equipo y el nuevo PRE registran sus propios hechos.

previous_case_id y followup_key se asignan sólo por fábrica privada; no se cambian después.
Unicidad por origen/solicitud. Evento followup conserva Many2one real al hijo. Replay devuelve ese
registro con permiso de lectura, aunque ya haya avanzado; no restablece fecha, síntoma ni estado.
La visita anterior conserva su cierre físico. Corrección posterior del origen no modifica el hijo.

## Informe y permisos

Reporte REP agrega correcciones y ejes por fuente PRE/PED/unidad/moneda. Falta de acceso comercial
produce unknown y conserva hechos de custodia, sin sudo, ceros ni cumplimiento inventados.
No hay stock del equipo ajeno ni efectos financieros implícitos al corregir o preparar otra visita.
Escenarios y PDF se revisan después; fuente, instalación, QA y aceptación son estados separados.
