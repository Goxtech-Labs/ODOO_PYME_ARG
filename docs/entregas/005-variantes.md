# Variantes ARG · incremento de Catálogo1.1.0

2026-11-06. Código instalado técnicamente en aislado, sin QA acreditada. Catálogo1.1.0/Stock1.0.6
están en la [composición aislada](../../composition/environments/isolated-development.json); el [lock de la demo](../../composition/versions.lock.json) conserva las versiones realmente instaladas.

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

Pendientes: promoción recuperable a demo y QA/aceptación posterior. La demo no cambió en esta etapa.
Parent016T008 conserva F19/condiciones pendientes; F17/F22 mantienen sus ampliaciones. El objetivo
completo de22 capacidades/E1/017–024/Integraciones continúa, sin cerrar tareas por un parseo estático.
