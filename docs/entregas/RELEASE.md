# Odoo Pymes ARG — 0.1.3-dev

Interfaz con cinta de comandos, iconos Lucide locales, campos delimitados, portada y acceso con
industria argentina. Preferencias personales de tema/densidad. Correcciones de compatibilidad con
Odoo 20 para cantidades e impresión. [Cambios y pruebas](INTERFAZ-Y-VENTAS.md).

Composición:91 módulos,79 nativos/dependencias y12 ARG. Paquete227 archivos,
SHA256 `a4e0dcadaaa7a64985cda7fdf56429f9c1a904b700986d5c8c9a2b1d199d24bf`. [Versiones exactas](../../composition/versions.lock.json).
Interfaz20.0.1.1.2, Documentos20.0.1.0.6; los consumidores de cantidades incrementan sus versiones.
Composición actualizada explícitamente en aislado y demo, sin actualización global de módulos.

Se ejecutó QA aislada del recorrido PRE→PED→REM parcial→FAC parcial con ejemplos, diario interno
sin emisión fiscal y permisos del usuario de gestión. Dos unidades pedidas, una entregada y una
facturada; pendientes físicos, de facturación y deuda diferenciados. HTML documental y consultas
PED/FAC/existencias comprobados. No acredita pruebas completas de todos los circuitos.

Se verificaron arranque OWL, cinta y configuración, combo de cliente, edición sin guardar,
cambio de pestaña conservando datos, descarte sin persistencia, tema claro/oscuro y ancho390px.
El acceso conserva autenticación/CSRF nativos. La aceptación del titular sigue pendiente.

Respaldo consistente previo con integridad verificada; no restaurado en esta revisión. La demo
conserva sus datos; las operaciones de QA están sólo en el entorno aislado. No hubo emisión fiscal,
pagos ni mensajes externos. Cron y correo permanecen desactivados.

Canales Goxtech configurados según [entrega anterior](RELEASE-0.1.2-dev.md).
Tutoriales específicos, integraciones, ARCA y módulos por rubro continúan como etapas posteriores.
Código original AGPL-3.0-only; documentación/recursos originales CC BY-SA 4.0; Lucide ISC/Feather MIT.
[Recursos y procedencia](../RECURSOS-VISUALES.md). [QA y límites](QA.md).
