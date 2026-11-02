# Entrega inicial comercial Ventas ARG — 2026-11-01

Estado: desarrollado y desplegado, **QA funcional y aceptación pendientes**. Feature006 parcial:
se entrega PRE/PED y facturación; el puente físico y cobros efectivos requieren Stock y Administración.

Paquete SHA256 `7bf2fdf7c4951898da5d66fb768ebaa15d6730b61cd639bc691dd114de12170c`; 90 archivos coinciden por SHA256 entre artefacto y runtime demo.
85 módulos instalados: 79 nativos/dependencias y 6 ARG. Versiones:
Base20.0.1.0.2, UI20.0.1.0.0, Terceros20.0.1.0.0, Catálogo20.0.1.0.3,
Documentos20.0.1.0.2, Ventas20.0.1.0.0. demo arg_demo, https://pymes.goxtechlabs.com.ar.
Sin commit/push; el artefacto y su recibo fijan esta entrega sin atribuir un commit inexistente.

## Controles técnicos realizados

- AST Python, XML, JS, dependencias y rutas de manifest/assets correctos; Gitleaks sin hallazgos.
- Instalación inicial de Ventas y upgrade final en entorno aislado sin red; actualización exacta de Base/Catálogo/Documentos/Ventas,
  nunca `-u all`. El mismo paquete se instaló en demo.
- Registro confirma versiones/installed y servicios Odoo/túnel activos. Cron y correo: cero activos.
- Chromium autenticado: Home, matriz, lista PRE y formulario PRE sin guardar montan; cero pageerror y diálogos de error;
  ayuda/soporte HTTP200. No se editó ni guardó un documento.
- Después del arranque: cero PRE, cero PED, cero facturas y cero asientos publicados. No se ejecutaron
  aceptación/generación/facturación/stock/pagos, emisiones fiscales ni mensajes externos.
- Revisión estática independiente por sesiones Codex de la misma familia/cuenta; hallazgos corregidos y releídos.
  No acredita auditoría externa, QA funcional, concurrencia efectiva ni aceptación del usuario.

## Respaldo y recuperación

Snapshot `punto de recuperación previo de la entrega`. Vzdump consistente previo:
`respaldo privado de la entrega`,
1.321.531.814 bytes, SHA256 `6dca872c98f572dcbd7decd594f0c542dee085ce33f491d96117dc9f55e73c69`,
integridad zstd correcta. Este archivo nuevo no se restauró; la restauración aislada previa fue la del
baseline inicial y no certifica este backup nuevo. No restaurar una DB antigua automáticamente ante nuevas escrituras.

Evidencia privada de infraestructura sin secretos: `registro técnico privado de la entrega` fuera del repositorio público.
No incluye base de datos, filestore ni credenciales. Archivo del paquete fuera de Git.

## Cambios transversales y pendientes

Base incorpora guard de tasas propias efectivas; Catálogo evita conversiones implícitas, incluyendo extras
sobre reglas fijas; Documentos conserva marca Ejemplo en cada documento aunque cambie el ajuste de compañía.
Las relaciones de líneas sin atribución cuantitativa exacta muestran Sin desglosar.

T007/T008 se entregan por su parte de facturación; entrega física y T012 requieren el puente Ventas–Stock.
T011 tiene aceptación/generación/facturación/cancelación de deuda; dinero cobrado/aplicado requiere Administración.
No cerrar esos criterios por esta entrega. Escenarios en quickstart quedan para revisión posterior.
Sigue feature007 Compras, luego Stock/puentes, Administración e Informes, según dependencias.

Actualización posterior: [entrega007](007-compras.md) conserva el nuevo artefacto y cambios de seguridad/composición; esta evidencia anterior permanece histórica.

Actualización posterior: [entrega008](008-stock.md) incorpora el puente físico y conserva evidencias técnicas. Dinero efectivo y QA siguen pendientes.

Actualización009 posterior: Administración y ejes de dinero instalados; los pendientes físicos se entregaron con008. Este informe conserva la evidencia histórica del incremento comercial inicial. Estado vigente en docs/ESTADO-MODULOS.md y entrega009; QA posterior pendiente.

Incremento posterior: [interfaz y revisión parcial de Ventas,0.1.3-dev](INTERFAZ-Y-VENTAS.md). La evidencia inicial anterior se conserva como histórica.
