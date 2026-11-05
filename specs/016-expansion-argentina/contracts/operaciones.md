# Contrato de coordinación

Toda capacidad tiene referencia funcional → adaptación argentina → datos mínimos → efectos → origen →
pendientes → corrección → permisos → manual/tutorial → composición. La matriz F01–F22 es inventario,
no evidencia de implementación. Una tarea de padre no marca implementado un módulo hijo.

Conservar [interfaz mínima](../../001-pyme-argentina/contracts/interfaz.md),
[REC/OPA](../../009-administracion/contracts/operaciones.md) y
[cartera](../../017-cartera-valores/contracts/cartera-argentina.md).

No mezclar estado interno con confirmación externa. Los movimientos se confirman desde acciones
validadas y con claves idempotentes; usuario, compañía y registro se autorizan en servidor. Para
reintento incierto externo, consulta primero. Sin activación explícita no hay efecto externo.

Migraciones aditivas con inventario previo; no reclasificar pagos antiguos por texto libre. Cada entrega
conserva datos y versión; restaurar requiere evaluar escrituras posteriores, no es fallback automático.
