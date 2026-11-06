# Trabajo autorizado · Reparaciones ARG

Complementa [operaciones](operaciones.md). Código1.1 preparado, sin instalación ni QA acreditadas.

## Documentos y secuencia

REP identifica equipo ajeno/custodia. PRE conserva condiciones/revisiones; PED es otro documento
nativo generado desde cantidades confirmadas. Vínculo por raíz comercial y evento con Many2one
real al PED, sin búsqueda por texto ni omisión silenciosa de pedidos ocultos.

1. Recibir y registrar diagnóstico, sin movimientos ni factura.
2. Preparar/emitir PRE, confirmar cantidades y generar PED borrador con acciones existentes.
3. Registrar autorización inmutable del PED: fecha, quién, constancia, cobertura, actor y términos.
   No confirma el pedido ni certifica firma digital. Garantía declarada/mixta no cambia precios.
4. Confirmar PED autorizado e iniciar trabajo. Salidas requieren este estado y pedido activo.
5. Validar repuestos por sale_stock, sin segunda salida interna por el mismo hecho. Devolver desde
   movimiento validado, misma línea/compañía/producto y cantidades actualizables (to_refund).
6. Registrar PTM de servicios manuales, en unidad del PED; horas sólo si la unidad es hora.
7. Marcar listo cuando el alcance esté cumplido, sin borradores, cancelados sin liberar o cantidades
   de PRE confirmadas sin PED. Retomar requiere motivo.
8. Entregar equipo reparado con fecha y quién retira; nueva comprobación y fin de custodia.
9. Facturar desde PED y cobrar mediante REC en Administración; REP no genera otra factura.

Un alcance adicional usa revisión/PED/autorización nuevos, conservando los anteriores.

## Fuente de cumplimiento

PTM confirmado actualiza qty_delivered nativo con actor/momento, hasta el máximo autorizado.
Antes de cambiarlo exige coincidencia con PTM vigentes; no sobrescribe una cantidad ajena.
No sustituye analítica ni partes de horas de otras composiciones.

Consumibles se explican con movimientos nativos terminados clasificados outgoing/incoming en
contexto actual. Un corte histórico no limita el control. El float qty_delivered no prueba salida.
Líneas se crean con cantidad cero/método nativo derivado; defaults/RPC no fabrican cumplimiento,
gastos ni anticipos. El neto de salida/devolución no supera el autorizado ni queda negativo.

## Corrección e idempotencia

Revertir PTM conserva original y fecha/motivo, recalcula con PTM aún confirmados y retoma trabajo
si estaba listo. Después de entregar conserva la constancia física y muestra el pendiente corregido;
no afirma reingreso al taller ni revierte facturas/cobros. Esos documentos se corrigen por separado.
Pedidos cancelados/liberados conservan historia. Devolver sin reparar exige resolver pedidos y
trabajo previo. Recepción/diagnóstico registrados aún no tienen operación de corrección explícita.

Eventos usan clave estable por solicitud. Asistentes fijan parte/modo/UUID; un diálogo viejo no
actúa sobre una nueva etapa. Reintento no repite efecto; constancia diferente ya registrada se rechaza.

## Permisos y entrega

Ejes por PRE/PED/línea/unidad/moneda, sin otra suma de caja. Permisos insuficientes producen
desconocido/rechazo, nunca cero/completo inventado ni sudo de negocio. Roles combinables.
Raíces comerciales ordenadas antes de casos; operaciones mixtas incluyen todas sus raíces.
Fábricas limpian defaults y selector histórico. Migración1.0→1.1 conserva evidencia y asigna claves
legacy antes de cambiar unicidad. Instalación, PDF, casos físicos/financieros y QA son hitos posteriores.
