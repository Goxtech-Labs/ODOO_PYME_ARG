# Odoo Pymes ARG — 0.1.9-dev

Series y lotes F14 desplegados en demo el2026-11-06: Stock1.1.1; Catálogo1.2.0 conservado.
Búsqueda paginada, historia de movimientos finalizados, documentos de origen autorizados y
cantidades actuales visibles, con unidad y ámbito separados del rango histórico.

**Nueva serie o lote** pide producto rastreable y número, con referencia opcional. El maestro se
usa después en recepciones/inventarios. La confirmación del mismo asistente conserva el resultado;
la extensión nativa serializa altas y cambios de identidad del lote. Ese comportamiento concurrente
se revisó en código, sin ejecución de escenarios funcionales. [Manual y controles](008-trazabilidad.md).

103 módulos:14 ARG y89 nativos/dependencias, incluido POS.299 archivos coinciden con el paquete
SHA256 `c660a0d977fbab58283f54a0cedad5f9ffa17b8c0d2d3e6ba05d8f91c5c823e6`.
[Composición instalada](../../composition/versions.lock.json). Fuentes de addons en
[f32bde9](https://github.com/Goxtech-Labs/ODOO_PYME_ARG/commit/f32bde9c630409a23bdca496c4cc10ec396d3263).

Snapshot/respaldo fresco, restauración en nueva copia sin red y upgrade allí comprobados antes
de actualizar Stock en demo. Versiones restantes, conteos de operaciones/lotes y metadatos
seleccionados conservados. Registro/vistas/servicios y formulario público HTTP200 verificados.
No es una instalación vacía, una prueba funcional de trazabilidad ni de concurrencia.

QA funcional/visual, PDF/impresión, tutorial publicado y aceptación pendientes. No se generó una
historia de movimientos por esta entrega ni se ejecutaron circuitos financieros o envíos reales.
F15/reposición sigue pendiente y parent016T009 permanece abierta; el objetivo completo de22
capacidades/E1/017–024/Integraciones continúa. [Entrega anterior](RELEASE-0.1.8-dev.md).
Licencias y atribuciones conservadas.
