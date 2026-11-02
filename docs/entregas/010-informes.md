# Informes ARG —20.0.1.0.0 —2026-11-01

Estado: **desarrollado e instalado técnicamente; QA funcional/visual y aceptación pendientes**.
demo arg_demo, https://pymes.goxtechlabs.com.ar.91módulos:79nativos/dependencias y12ARG.
158archivos fuente/paquete/runtime coinciden; SHA256 `1cee3c05d02aaf2550296bcdb3a4e53c04231f7b93148575395e70f96efe9f42`. Sin commit/push.

## Entregado

Once consultas por hechos, filtros únicos compañía/moneda, agrupación por identidades reales,
detalle50filas, totales del corte por moneda/unidad/circuito, navegación a documentos, CSV UTF-8 y PDF.
Sin libro paralelo, SQL nuevo, sudo comercial, Enterprise ni obligación de instalar todos los circuitos.
Stock actual y reconstruido a fecha separados; deuda actual por vencimiento explícita; aplicaciones
contables no se presentan como dinero. Ejes ARG conservan parciales y cierre con faltante.

## Evidencia técnica

- AST/XML/JS/manifests/rutas y Gitleaks sin hallazgos;145fuentes anteriores sin cambios y13nuevas.
- Instalado en entorno aislado sin red y demo, sólo arg_pyme_informes. No-uall.
- Instalación mínima nueva UTF8 en arg_install_010_min, entorno aislado sin red:31módulos, sin account.move.line ni stock.move.line. Demuestra ausencia de dependencia obligatoria de esos circuitos. Cron/correo desactivados.
- Chromium autenticado: Home/formulario montados, once fuentes disponibles, cero diálogos/erroresJS.
- Consulta vacía con filtros transitorios propios; HTML200, CSV200 UTF-8/BOM/no-store y PDF200 de25915bytes. No se crearon facturas, pagos, conciliaciones ni movimientos para verificarla.
- Cero documentos comerciales/financieros/inventarios/movimientos/quants/asientos/parciales/eventos; cron/correo0activos y servicios Odoo/túnel activos.
- Dos revisiones independientes de fuente, misma familia/cuenta: correcciones ACL20, reporte20, almacenables/unidad base histórica, TZ y exportación releídas. No equivalen a QA de cálculos, roles o concurrencia con datos.

Primer arranque técnico detectó ausencia de motor PDF. Se instaló wkhtmltox1:0.12.6.1-3.jammy
(patched Qt) del release oficial, SHA2564f723b2691ad8638a9df960e0421d346d7315083e3583a334f33362280ddba15.
Se añadieron fontconfig/xfonts-75dpi/xfonts-base; cero upgrades y cero removals. entorno aislado verificó generación
sin red antes de instalar lo mismo en demo. Enlaces /usr/bin a binarios /usr/local/bin resuelven PATH;
reinicio de Odoo limpia la detección cacheada del motor. Capturas y hashes del paquete en evidencia.
Fuentes primarias: [guía Odoo](https://github.com/odoo/odoo/wiki/Wkhtmltopdf),
[release oficial](https://github.com/wkhtmltopdf/packaging/releases/tag/0.12.6.1-3).

## Recuperación

Snapshot `punto de recuperación previo de la entrega` y backup consistente con Odoo detenido: `respaldo privado de la entrega`,
1330490559bytes, SHA256 `51fd09693492df3e8d3df0462e4f8e8e78ac6e9075c8d3b174a225a6f90619d9`; integridad zstd verificada.
Este backup nuevo no fue restaurado; baseline inicial sí restaurado en entorno aislado sin red. No restaurar
bases anteriores automáticamente si hubo escrituras posteriores.
Evidencia sanitizada en registro técnico privado de la entrega fuera del repositorio público.

Siguen portada/documentación011 y preparación global de entrega. Integraciones/rubros posteriores.
Escenarios quickstart sin ejecutar; QA posterior y aceptación siguen pendientes.
