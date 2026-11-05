# Primer incremento de carga práctica · 2026-11-05

Interfaz documental: fecha primero en PRE, PED, PPC, REC/OPA, movimientos y conteos propios.
Los campos existentes y sus permisos/dominios se conservan. Facturas/notas de venta y compra
proponen invoice_date de hoy por contexto cuando el campo se solicita y no tiene valor/default
explícito. Fecha existente, importada, de origen o indicada en contexto no se reescribe; ni vencimiento
ni fecha contable se sustituyen por este cambio.

Versiones: Ventas20.0.1.0.6, Compras20.0.1.0.5, Stock20.0.1.0.5 y Administración20.0.1.1.2.
Interfaz sigue20.0.1.1.5. El resto conserva su versión. Paquete231 archivos SHA256
898b636eaac4a8d567470f5668ca6bc1c10d2ccdbe808df64b02fca06ea625ba.101 módulos en composición:12 ARG y89 nativos/dependencias.

Controles: AST/XML/JS/manifests/Gitleaks, revisión estática independiente del diff exacto por otra
sesión de la misma familia/cuenta y carga/upgrade de los cuatro addons. En aislado se igualó la
composición nativa del POS observado, sin red ni correo y con cron desactivado sólo allí.
Comprobación técnica de default_get en cuatro tipos, fechas explícitas incluso vacías conservadas,
campo no solicitado ausente; orden declarado de cinco vistas. Ningún documento operativo creado.

Esto no acredita QA funcional/visual ni que todas las pantallas ya estén simplificadas. La factura
nativa conserva su disposición; la experiencia ampliada de captura y datos secundarios continúa
en E1. Las specs017–024, integraciones y mejoras comerciales restantes siguen pendientes de código.
Respaldo completo previo verificado; no restaurado en esta entrega. Mantener datos/configuración
del titular, incluidos sus módulos POS y cron; no restaurar historia antigua para corregir presentación.

Ver [plan completo](../PLAN-EXPANSION-ARG.md) y [tareas](../../specs/016-expansion-argentina/tasks.md).
