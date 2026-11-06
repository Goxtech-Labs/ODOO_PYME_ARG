# Variantes ARG · incremento de Catálogo1.1.0

2026-11-06. Código instalado técnicamente en aislado y demo, sin QA acreditada. Catálogo1.1.0/Stock1.0.6
están en la [composición aislada](../../composition/environments/isolated-development.json); el [lock de la demo](../../composition/versions.lock.json) registra la misma versión instalada.

Matriz por atributos opcionales con dos ejes elegibles y filtros restantes, páginas8×15 y búsqueda
de valores30. Distingue exclusión, variante visible y variante no determinada, sin generar ni reactivar
variantes. Fichas, precios y etiquetas usan sus fuentes/acciones nativas. Selección hasta200,
conservada al paginar/filtrar y revalidada al abrir etiquetas. Cantidades son opcionales por Stock y permisos.

[Contrato](../../specs/005-catalogo/contracts/matriz-variantes.md) · [Manual](../usuario/005-catalogo.md) ·
[Técnica](../tecnica/005-catalogo.md) · [Escenarios posteriores](../../specs/005-catalogo/quickstart.md).

Controles realizados: AST/XML/JS, manifests/ACL, Gitleaks0 y revisión estática independiente de otra
sesión de la misma familia/cuenta, sin bloqueantes. No es auditoría externa. Paquete290 archivos SHA256
`4bd58a7bb465593bc3b8cba1a4f4a9db2b30ef3ced219dc97bdac207b1fbd378`. Snapshot aislado previo,
upgrade de Catálogo/Stock, fuente completa coincidente y103 módulos conservados. Registro, vista
combinada/procesada, adaptador de cantidades, servicio y HTTP local200 comprobados. Conteos de
ocho modelos y de Reparaciones/Valores, metadatos seleccionados y cron/correo iguales. Aislado sin
red ni túnel activo; no se ejecutaron recorridos de negocio ni se generaron datos nuevos de ejemplo.

Promoción a demo completada con respaldo fresco/snapshot, restauración en nueva copia sin red y
upgrade controlado de esa composición antes de actualizar el entorno público. Se conservaron los
módulos nativos, incluido POS, y conteos/metadatos seleccionados. Odoo/PostgreSQL/túnel activos y
formulario público HTTP200. El observador local agotó una consulta SSH; una lectura posterior del
mismo job confirmó su recibo final y salud, sin relanzar la operación ni restaurar una DB antigua.

Pendientes: QA funcional/visual, impresión y aceptación posterior. Los ejemplos específicos de la
matriz se registran por separado; no se presentan como recorridos de negocio ejecutados.
Parent016T008 conserva F19/condiciones pendientes; F17/F22 mantienen sus ampliaciones. El objetivo
completo de22 capacidades/E1/017–024/Integraciones continúa, sin cerrar tareas por un parseo estático.

## Maestros de ejemplo

Tras revisión estática del cargador y snapshot por entorno, se creó un artículo EJEMPLO con tres
atributos de dos valores y ocho variantes activas nativas, primero en aislado y después en demo.
Los códigos son textuales ARG-EJ-VAR-001…008; moneda de la compañía y unidad del catálogo nativo.
Doce conteos operativos observados por el cargador se conservaron. No se cargó stock ni se generó
una operación comercial, contable, financiera o de reparación. Carga inicial única por entorno,
sin reejecución para probar idempotencia ni recorrido de la matriz. [Cargador](../../ops/seed_variants_demo.py).

Tutorial de Variantes1.1 registrado como planeado, sin URL ficticia. QA, impresión y aceptación
permanecen pendientes.
