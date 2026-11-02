# Entrega comercial Compras ARG — 2026-11-01

Estado: desarrollado y desplegado, **QA funcional y aceptación pendientes**. Feature007 parcial:
PPC y FRC/NCP entregados; ENT/DCP, puente físico y pagos efectivos requieren Stock/Administración.

Paquete SHA256 `5612c635b1385d3fbc29b75d89d49c544d3980e8ab89468de33d7aa2e0ca9de5`; 102 archivos coinciden por SHA256 entre fuente, artefacto y runtime demo.
86 módulos instalados: 79 nativos/dependencias y 7 ARG. Compras20.0.1.0.0, Ventas20.0.1.0.1,
Documentos20.0.1.0.3, Base20.0.1.0.2, UI20.0.1.0.0, Terceros20.0.1.0.0 y Catálogo20.0.1.0.3.
Destino demo arg_demo, https://pymes.goxtechlabs.com.ar. Sin commit/push; la entrega está fijada por artefacto.

## Evidencia técnica

- Manifest/archivos, AST Python, XML y JS correctos; Gitleaks sin hallazgos.
- Primera instalación de Compras y upgrade final en entorno aislado sin red. Mismo paquete en demo, sólo módulos
  Documentos/Ventas/Compras; nunca actualización global. Registro confirma installed y versiones.
- Chromium autenticado monta Home, matriz, listas PRE/PPC y ambos formularios sin guardar; cero erroresJS,
  alertas de matriz y diálogos de error. Ayuda/soporte HTTP200.
- Servicios Odoo/túnel activos; cero cron/correo activos. Cero PRE/PED/PPC/facturas/asientos publicados.
- No se ejecutaron recorridos comerciales, publicaciones contables, movimientos, pagos, fiscales ni mensajes.
- Dos sesiones Codex independientes de lectura revisaron fuente y cerraron hallazgos; misma familia/cuenta,
  no independencia de proveedor ni auditoría externa. La comparación de hashes acredita contenido desplegado,
  no comportamiento funcional. QA efectivo de ACL/multiempresa/concurrencia y aceptación siguen pendientes.

## Respaldo previo

Snapshot `punto de recuperación previo de la entrega`. Vzdump con Odoo detenido durante el backup:
`respaldo privado de la entrega`, 1323562459bytes,
SHA256 `8308a1eb0531b7752e21ed600ddfd9859812431abf2e6d24f19dff791a4e3bd3`, integridad zstd correcta.
Este archivo no se restauró; la restauración aislada previa certificó el baseline inicial, no este backup nuevo.
No restaurar una DB anterior automáticamente ante nuevas escrituras. Evidencia en registro técnico privado de la entrega.

## Cambios y límites

PPC conserva condiciones/snapshot y reporte histórico. Preparación parcial FRC tiene clave/hash/evento
inmutable y control de cantidades. Se preserva número original del proveedor. Publicación suma lote y notas;
no se confunde borrador facturado ni residual con pago efectivo. Se fijan contextos de compañía y tipo documental.
Documentos/Ventas corrigen defaults RPC protegidos y composición de adaptadores contables por tipo.

T005/T006 se entregan por su parte FRC y T007/T008 por NCP contable; recepción/devolución física continúan en T012
con feature008. T011 sigue parcial hasta recepción y dinero efectivo. Escenarios quickstart quedan para QA posterior.
Sigue Stock008, incluyendo puentes de ambos circuitos; luego Administración009 e Informes010.

Actualización posterior: [entrega008](008-stock.md) incorpora el puente físico y conserva evidencias técnicas. Dinero efectivo y QA siguen pendientes.

Actualización009 posterior: Administración y ejes de dinero instalados; los pendientes físicos se entregaron con008. Este informe conserva la evidencia histórica del incremento comercial inicial. Estado vigente en docs/ESTADO-MODULOS.md y entrega009; QA posterior pendiente.
