# Entrega Stock ARG y puentes — 2026-11-01

Estado: código desarrollado y desplegado, **QA funcional y aceptación pendientes**.
Stock20.0.1.0.1, Ventas–Stock20.0.1.0.1 y Compras–Stock20.0.1.0.1.
Composición SHA256 `bd3f4d7f0983014ba6446bdb4b55ffa0bdbbef1d3fe5f18ec4498ddeeec797e3`;125archivos coinciden entre fuente, artefacto y runtime.
89módulos:79nativos/dependencias y10ARG. Destino demo arg_demo, https://pymes.goxtechlabs.com.ar.
Sin commit/push: versión fijada por artefacto y recibo, no por un commit inexistente.

## Controles y límites

Manifest/dependencias/rutas, Python/XML/JS y Gitleaks correctos. Core instalado inicialmente y upgrade final con
ambos puentes en entorno aislado sin red. El mismo paquete instaló únicamente esos tres addons en demo, sin -u all.
Preflight verificó cero pedidos comerciales, pickings, movimientos y quants; los puentes nativos ya estaban instalados.
No fue necesario migrar operaciones abiertas en esta demo. No extrapolar ese resultado a otras instalaciones.

Chromium autenticado: Home, matrices de precios/existencias, listas PRE/PPC/INV y formularios sin guardar
arrancan; cero pageerror/alertas de matriz/diálogos. Ayuda/soporte200. Odoo/túnel activos; cron/correo0activos.
Cero PRE/PED/PPC/INV/AJU, pickings, movimientos, quants, facturas y asientos publicados después del arranque.
No se registraron operaciones como QA ni se emitieron mensajes/fiscales. La matriz consulta maestros de ejemplo.

Revisión independiente de fuente por sesiones Codex de la misma familia/cuenta; hallazgos corregidos y releídos.
No es auditoría externa ni prueba funcional de concurrencia/permisos/multiempresa/cantidades. Las verificaciones
anteriores son técnicas; los escenarios de quickstart permanecen para la fase de QA posterior acordada.

## Respaldo

Snapshot `punto de recuperación previo de la entrega`. Backup consistente con Odoo detenido:
`respaldo privado de la entrega`, 1323921703bytes,
SHA256 `e3a046788ee90f6e812ffbad8ecc1ca5fe71cb869b0f56dea71b2b5458cae66d`, integridad zstd correcta.
Este backup nuevo no se restauró; la restauración aislada previa certificó el baseline inicial. No revertir una DB
antigua automáticamente si hay nuevas escrituras. Evidencias sin secretos en registro técnico privado de la entrega.

## Entregado y siguiente etapa

Consulta separa físico/reserva/disponible/previsto; documentos físicos usan mecanismos nativos de retorno/backorder.
INV/AJU conservan evidencia y aplican diferencias mediante quants/movimientos nativos, sin libro paralelo.
Puentes agregan ejes y vínculos a PED/PPC; servicios físicosNA, faltante cerrado separado y to_refund nativo respetado.
Los enlaces de factura son a movimientos de pedidos origen, sin fingir atribución exacta factura–remito.
Dinero cobrado/pagado y su aplicación siguen pendientes de Administración009; residual saldado no acredita caja.
Sigue feature009 y luego Informes010, web/documentación011; integraciones/rubros son posteriores al núcleo.

Corrección core1.0.1: los detalles de movimiento rechazan cambios directos de estado y altas/traslados
sobre movimiento o picking terminal. Upgrade secuencial entorno aislado→demo y arranque técnico repetido sin errores.
Los puentes conservan versión1.0.0. Revisión independiente de este diff cerrada; no QA funcional.
