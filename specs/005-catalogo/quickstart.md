# Quickstart de validación posterior: Catálogo y precios ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Crear un producto de ejemplo con nombre, tipo, unidad y precio sin completar atributos de un rubro ajeno. Revisar además: exigir lote o depósito sólo cuando la capacidad y el producto lo requieran.
2. Filtrar productos y editar precios en columnas alineadas, revisando antes de guardar. Revisar además: conservar cambios pendientes al filtrar y detectar modificaciones concurrentes.
3. Agregar un atributo opcional y conservar el mismo catálogo y sus referencias. Revisar además: evitar generar combinaciones innecesarias o reinterpretar un servicio como existencia física.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.

## Variantes FR-007/008 · escenarios preparados, no ejecutados

1. Plantilla sin atributos y servicio: una celda, unidad/código nativos, sin stock inventado ni generación.
2. Tres atributos opcionales, ejes intercambiados y uno fijo: filtros visibles/corregibles, páginas8×15 y valores30; exclusiones nativas respetadas.
3. Variante dinámica no creada, archivada o no visible: no determinado; ninguna fábrica ni reactivación.
4. Operador sin Stock/permiso cuantitativo, otra compañía y contexto con ubicación/fecha/propietario: ausencia explícita de dato o ámbito actual limpio, sin elevación.
5. Seleccionar variantes en varias páginas/filtros, quitar y cambiar producto: selección explícita hasta200, confirmación de descarte y revalidación al abrir etiquetas. No imprimir en este recorrido.
6. Abrir precios por plantilla y conservar reglas/moneda/cambios pendientes; verificar que la matriz general anterior mantiene su comportamiento.
7. Revisar teclado, etiquetas, selección, estados vacío/cargando/error y claro/oscuro en escritorio y ancho estrecho, sin afirmar QA por parseo.
