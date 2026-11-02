# Operación, instalación y recuperación

## Instalación reproducible

1. Elegir Linux compatible, PostgreSQL 16 y paquete estable Odoo 20 oficial; verificar firma y registrar versiones/hash.
2. Crear usuario de servicio y rol PostgreSQL local; conservar DB, filestore y configuración como una unidad de respaldo.
3. Configurar base única, dbfilter exacto, list_db=False, contraseña maestra fuerte y permisos root:odoo 0640.
4. Instalar módulos exactos mediante `odoo server`, con servicio detenido y `--stop-after-init`; consultar ayuda del binario.
5. Para ejemplos, usar exclusivamente arg_demo y cargar ops/seed_demo.py mediante shell Odoo con contraseña desde almacén protegido.
6. Configurar reverse proxy HTTPS del propietario o túnel elegido; habilitar proxy_mode sólo detrás del proxy controlado.
7. Verificar servicio, login, versión, módulos y logs sanitizados. Registrar instalación separada de QA posterior.

La gestión puede funcionar en red local sin Cloudflare ni Internet. El túnel de esta demo es una elección de despliegue,
no una dependencia de los addons ni una cuenta obligatoria para las pymes.

## Antes de cada cambio

Inventariar CT/base, addon, SHA, dependencias y efectos. Detener trabajos/envíos; hacer backup consistente y snapshot
si está soportado. No aplicar hooks de stock sobre pedidos abiertos sin previsualización y respaldo recuperable.
Sólo actualizar los módulos previstos. Nunca restaurar una base vieja automáticamente si hubo nuevas operaciones.

## Respaldo

Respaldo íntegro del CT incluye PostgreSQL, filestore local, configuración y código instalado; comprobar volúmenes externos.
Para respaldo portable: detener escrituras y servicio Odoo, generar pg_dump formato custom y copiar filestore de la misma base,
configuración protegida, manifiesto de módulos/versiones y código fijado. Cifrar y restringir acceso porque incluye secretos.
Guardar otra copia fuera del disco del CT; snapshot solo no es backup.
Registrar fecha, tamaño, checksum y prueba de lectura; no publicar artefactos de recuperación.

## Restauración aislada

1. Crear CT/host de prueba sin publicación ni salidas externas y con cron detenido.
2. Restaurar la misma revisión, PostgreSQL, DB y filestore coherentes; adaptar propietarios y configuración protegida.
3. Cambiar URL/canales de salida antes de iniciar. Validar servicio, login, adjuntos, conteos y conciliación de totales.
4. Registrar resultado y límites de la prueba. Un checksum o listado de archivo no acredita una restauración completa.
5. Para migración real, planificar corte de escrituras y tratamiento de cambios posteriores; no mezclar dos bases activas.

## Reversión

Disparadores: fallo de arranque, migración fallida o pérdida de integridad confirmada. Aislar servicio y conservar logs/datos nuevos.
Revertir código sólo si el esquema sigue compatible; para recuperar DB/filestore exigir un punto consistente y preservar cambios posteriores.
No borrar CT, DNS o túnel compartidos. Los recursos de esta demo son exclusivos; su retirada se registra y autoriza como operación aparte.

## Motor PDF

Instalar el motor admitido por Odoo además de sus paquetes Python. Esta composición usa wkhtmltox1:0.12.6.1-3.jammy con patched Qt del release oficial, con SHA fijado en entrega010. Verificar dependencias por simulación, sin upgrades/removals implícitos; probar en entorno aislado antes del destino. Los binarios instalados en /usr/local/bin deben ser visibles en PATH del servicio (/usr/bin contiene enlaces explícitos en esta demo). Reiniciar Odoo después de instalar para limpiar la detección cacheada. La generación técnica de un PDF vacío no prueba diseño legible ni cálculos funcionales.
