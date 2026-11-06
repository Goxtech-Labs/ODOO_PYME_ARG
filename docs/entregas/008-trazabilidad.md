# Series/lotes ARG · incremento F14 de Stock1.1.1

2026-11-06. Código instalado técnicamente en aislado y demo. Stock1.1.1 y Catálogo1.2.0 constan en el lock. F15/reposición y el resto del plan
completo de22 capacidades continúan; parent016T009 no se cierra sólo con esta entrega.

Búsqueda de productos y lotes, historia de movimientos finalizados y quants actuales paginados.
Alta explícita de maestro con producto+número; sin otro saldo de stock. Fechas aplicadas y
pendientes separadas, relaciones nativas autorizadas y numeración del fabricante conservada.
La extensión de identidad serializa también las altas nativas y cambios de nombre/producto/compañía,
con permisos nativos, sin exigir rol ARG a todos esos consumidores.

[Contrato](../../specs/008-stock/contracts/trazabilidad-series-lotes.md) ·
[Manual](../usuario/008-stock.md) · [Técnica](../tecnica/008-stock.md) ·
[Escenarios posteriores](../../specs/008-stock/quickstart.md).

AST/XML/JS, CSV/manifest/rutas y XPath contra la vista nativa comprobados en9 archivos. Revisión
estática independiente sinP1/P2 tras corregir dos puntos de contrato y dos de backend; misma
familia/cuenta, sin independencia de modelo. Paquete299 archivos SHA256
`c660a0d977fbab58283f54a0cedad5f9ffa17b8c0d2d3e6ba05d8f91c5c823e6`,
299 fuentes coincidentes con NAS y9 archivos con la revisión. Snapshot y upgrade aislado de
Stock1.1.1 completados, conservando Catálogo1.2.0 y los103 módulos. Registro/acción/extensión
nativa de lotes, vistas combinadas/procesadas de maestro y asistente, servicio y HTTP local200
comprobados. Conteos operativos y de lotes/REP/valores, metadatos seleccionados y cron/correo
conservados. Aislado sin NIC externa ni túnel activo. Promoción a demo completada con respaldo fresco restaurado en una nueva copia sin red,
upgrade de Stock comprobado allí y el mismo paquete en demo. Se conservaron versiones restantes,
conteos de operaciones/lotes y metadatos seleccionados; servicios activos y login público HTTP200.
La copia de recuperación queda apagada y sin NIC. Fuente de addons publicada en
[f32bde9](https://github.com/Goxtech-Labs/ODOO_PYME_ARG/commit/f32bde9c630409a23bdca496c4cc10ec396d3263).
Fuentes, composición y documentación de esta entrega se publican juntas en main. No acredita instalación vacía, concurrencia ni QA.

Stock1.1.1 agrega al rol Stock ARG el grupo nativo de lotes y series. La lectura de grupos
posterior al upgrade confirmó su propagación a los usuarios activos de Stock ARG; conserva
los roles ARG existentes, el seguimiento de cada producto y los conteos de asistentes/lotes.
Se repitieron el upgrade aislado y la recuperación desde un respaldo fresco antes de promover
este paquete; las copias anteriores se conservan. La lectura de permisos no acredita un movimiento.

QA funcional/visual, PDF/impresión, tutorial de YouTube y aceptación posteriores. No se cargó una
historia de movimientos ni se ejecutó un circuito como prueba. Ejemplo documental ficticio
preparado, no presentado como dato cargado. Licencias y atribuciones se conservan.
