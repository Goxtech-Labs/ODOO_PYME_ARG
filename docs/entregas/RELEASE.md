# Odoo Pymes ARG — 0.1.7-dev

Matriz de variantes ARG desplegada en demo el2026-11-06: Catálogo1.1.0 y Stock1.0.6.
Atributos opcionales con ejes/fijos elegibles, páginas8×15 y búsqueda de valores30. Consulta variantes
visibles y exclusiones nativas sin generar combinaciones; cantidades según Stock/permisos y compañía.

Fichas, precios por producto y preparación de etiquetas usan acciones/fuentes nativas. La selección
de hasta200 variantes se conserva al paginar/filtrar y se revalida al preparar etiquetas; abrir el
asistente no imprime. Un artículo EJEMPLO con ocho variantes permite empezar a explorar; no se
cargaron existencias ni documentos de negocio por ese catálogo. [Manual y controles](005-variantes.md).

103 módulos:14 ARG y89 nativos/dependencias, incluido POS;290 fuentes propias coincidentes con el
paquete SHA256 `4bd58a7bb465593bc3b8cba1a4f4a9db2b30ef3ced219dc97bdac207b1fbd378`.
[Composición instalada](../../composition/versions.lock.json). Código de addons en
[cf3bc95](https://github.com/Goxtech-Labs/ODOO_PYME_ARG/commit/cf3bc95cea03c09ce20af8e8aed4098ea4002479).

Respaldo fresco/snapshot y recuperación en nueva copia aislada comprobados, después actualización
de Catálogo/Stock en esa copia y demo. Nativos/versiones, conteos operativos y metadatos seleccionados
conservados. Registro/vista/adaptador, servicios y formulario público HTTP200 comprobados.
No es una instalación vacía de todo Odoo ni una prueba del funcionamiento de la matriz.

QA funcional/visual, impresión/PDF y aceptación pendientes. No se ejecutaron recorridos financieros,
emisión fiscal ni mensajes. Las ampliaciones F19/F17/F22 y las demás22 capacidades/E1/017–024 e
Integraciones continúan según el plan, sin cerrar el objetivo general.
[Entrega anterior](RELEASE-0.1.6-dev.md). Licencias/atribuciones conservadas.
