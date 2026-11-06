# Odoo Pymes ARG — 0.1.8-dev

Precio y condiciones F19 desplegados en demo el2026-11-06: Catálogo1.2.0; Stock1.0.6 conservado.
Consulta con fecha/hora actual propuesta, cliente opcional, producto/variante, cantidad y lista
nativa corregible. Reutiliza el motor Odoo y explica reglas efectivas sin modificar documentos.

**Ver regla** conserva las ediciones de la matriz y usa fecha/cantidad cargadas. La explicación se
recalcula con la configuración actual; no es un snapshot histórico. La comparación de celda no
garantiza detectar todos los cambios de reglas base. Costos y parámetros respetan roles/permisos.
Los impuestos y totales se resuelven en el documento. [Manual y controles](005-precio-condiciones.md).

103 módulos:14 ARG y89 nativos/dependencias, incluido POS.294 archivos de addons coinciden con el
paquete SHA256 `08c329aa6770534e306516fd6d232cf4a7f1586a4a24975a6153bec6d64ac381`.
[Composición de0.1.8](../../composition/releases/0.1.8-dev.json). Fuentes de addons fijadas en
[68c47f8](https://github.com/Goxtech-Labs/ODOO_PYME_ARG/commit/68c47f89c0c9511adb5ffa57c9523637ce9ba959); el paquete identifica exactamente el código instalado.

Snapshot/respaldo fresco y restauración en nueva copia aislada comprobados, luego upgrade de
Catálogo en esa copia y demo. Versiones restantes, conteos operativos y metadatos seleccionados
conservados; registro/vista/servicios y formulario público HTTP200 verificados. El observador
relee los comprobantes de un trabajo que acaba de terminar; no repite el despliegue por perder
una consulta. No es una instalación vacía ni prueba funcional del recorrido de precios.

QA funcional/visual, impresión/PDF, tutorial publicado y aceptación pendientes. No se ejecutaron
recorridos financieros, emisión fiscal ni mensajes. F17/F22 y las demás capacidades/E1/017–024 e
Integraciones continúan; el objetivo completo sigue activo. [Entrega anterior](RELEASE-0.1.7-dev.md).
Licencias y atribuciones conservadas.
