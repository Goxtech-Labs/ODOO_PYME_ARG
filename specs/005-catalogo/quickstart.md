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

## F19 FR-009/010 · escenarios preparados, no ejecutados

1. Abrir consulta: fecha/hora local actual, cantidad1, cliente opcional; elegir producto y lista.
   Corregir fecha/hora y conservarla al abrir maestros/volver; un campo vacío requiere corregirlo.
2. Elegir cliente: proponer lista nativa; elegir otra manualmente y cambiar cliente sin reemplazarla.
   Usar lista del cliente restaura explícitamente esa propuesta. Paginar selectores de30 registros.
3. Consultar casos fijo, descuento y recargo; reglas por variante/plantilla/categoría/global, mínimos,
   vigencia exacta y listas encadenadas. Contrastar con cálculo nativo en el mismo momento/unidad.
4. Revisar sin regla, tasas efectivas ausentes, listas archivadas, otra compañía, permisos insuficientes,
   cadena circular/larga y extensión no conocida: no inventar cero ni una explicación completa.
5. Responsable y operador: cadena con costo no expone parámetros al operador; límites de margen
   restringidos se distinguen de detalle completo. No interpretar precio de venta como costo.
6. Desde matriz con ediciones pendientes y filtros aún no aplicados, abrir Ver regla: conservar buffer
   y usar fecha/cantidad de la página cargada. La explicación debe aclarar que usa configuración actual; el aviso se limita a cambios
   detectados por el token de celda, sin prometer un snapshot de todas las reglas base.
7. Abrir reglas/ficha con permisos nativos; explicar alcance de lista compartida. Cambiar una regla
   no reescribe precios históricos ni aplica cambios a la matriz al volver.
8. Revisar teclado, etiquetas, DateTimeInput, escritorio/ancho estrecho, claro/oscuro y estados
   vacío/cargando/error. El parseo XML no acredita visualización ni esos recorridos.
