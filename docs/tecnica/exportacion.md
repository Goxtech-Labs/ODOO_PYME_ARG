# Exportación abierta y relaciones

Hay dos necesidades diferentes: extraer información legible para trabajar y recuperar una instalación completa.
CSV/PDF no reemplazan una copia coherente de PostgreSQL, filestore, configuración y revisión de código.

## Informes y listados

Informes ARG exporta CSV UTF-8 con filtros, compañía, moneda, fecha de generación, grano, criterio y totales.
Los textos se protegen contra fórmulas de planilla. PDF conserva el mismo corte, sujeto a límites documentados.
Ambas salidas vuelven a consultar fuentes vigentes con permisos efectivos; no son un snapshot fiscal almacenado.
Para conservar evidencia de un cierre, coordinar el corte de escrituras y guardar su reporte con metadatos.

Los listados Odoo conservan exportación nativa según permisos. Para reimportación, preferir el modo compatible
con importación y conservar identificadores externos; un nombre visible puede repetirse y no es una clave.
No exportar columnas restringidas ni ejecutar sudo para sortear acceso. La API usada depende de la versión
instalada; autenticar como usuario autorizado y consultar sus campos disponibles antes de diseñar un extractor.

## Conservar relaciones

Exportar en conjuntos separados: compañías/monedas/unidades; terceros/roles; productos/listas;
cabeceras y líneas PRE/PED/PPC; movimientos/ubicaciones/lotes; facturas/apuntes; pagos/conciliaciones;
REC/OPA/medios/eventos. Conservar IDs externos, identidad ARG, documento origen y claves de relación.
No reconstruir vínculos sólo desde origin textual ni reemplazar el libro contable con un CSV de saldos.

Cada conjunto debe declarar modelo, campos, versión, fecha de corte, zona horaria, moneda, unidad y signo.
Las referencias Many2one/Many2many se exportan con claves, no sólo etiquetas. Los eventos preservan historia;
conciliaciones eliminadas no se reconstruyen únicamente con sus IDs. Las importaciones se diseñan aparte,
con idempotencia y conciliación; exportar no ejecuta una migración de datos reales.

## Adjuntos y recuperación

Para continuidad completa conservar DB y filestore de la misma base y corte, incluidos metadatos ir.attachment.
No copiar sólo imágenes ni publicar archivos privados en el repositorio. Un extractor selectivo de adjuntos
usa permisos del usuario y guarda un manifiesto de referencia, nombre, tipo, tamaño y hash; no exporta URLs
públicas permanentes de documentos privados por comodidad.

El respaldo portable usa pg_dump y filestore con escrituras detenidas, configuración protegida y código fijado.
Restaurar en entorno aislado, desactivar salidas/cron y verificar adjuntos y conteos antes de abrir acceso.
[Operación y recuperación](OPERACION-Y-RECUPERACION.md) distingue integridad de archivo y restauración real.
