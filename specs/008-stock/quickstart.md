# Quickstart de validación posterior: Circuito Stock ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Consultar producto y depósito mostrando cada cantidad con unidad y fecha de corte. Revisar además: no presentar cantidad prevista como existencia física ni sumar el mismo traslado dos veces.
2. Validar una entrega parcial y encontrar su remito, movimiento y pendiente vinculado. Revisar además: pedir serie/lote sólo al producto trazable y ofrecer dejar pendiente o cerrar faltante explícitamente.
3. Guardar INV, comparar contado/teórico y aplicar AJU enlazado a movimientos nativos. Revisar además: detectar cambios concurrentes antes de aplicar y evitar sobrescribir cantidad real sin evidencia.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.

## F14 · escenarios preparados para QA posterior, no ejecutados

1. Serie/lote con entrada, traslado, salida, ajuste y devolución: una fila por línea finalizada,
   cantidades/unidad/origen nativos, páginas30 y apertura del picking o movimiento sin picking.
2. Número con ceros, referencias iguales en productos/compañías diferentes, producto archivado o
   sin seguimiento: búsqueda/alcance explícitos, sin renumerar ni activar seguimiento automáticamente.
3. Rango histórico con quants actuales: fecha de consulta y ámbito claros; no sumar historia como saldo.
4. Operador con permisos parciales, relaciones restringidas y otra compañía: no nombres/IDs filtrados,
   cantidades no determinadas ante falta de permiso, no ceros de sustitución.
5. Alta mínima: producto rastreable+número, referencia opcional; confirmar/reintentar devuelve el
   mismo lote. Colisión concurrente/otro asistente pide corregir y no registra movimiento de stock.
6. Volver desde documentos conserva lote/rango/página; claro/oscuro, teclado y ancho estrecho sin
   perder controles. Abrir traza nativa es una acción avanzada; no renderizar PDF ni imprimir en este escenario.

## F15 · escenarios preparados para QA posterior, no ejecutados

En una composición aislada con compras y puente MRP instalados, sin correo/cron/canales reales:

1. Crear regla manual de ejemplo con producto, depósito y mínimo/máximo; guardar/consultar no
   crea PO/MO ni altera una regla automática previa. Revisar unidad y límites inválidos.
2. Comparar propuesta con cantidades nativas, compras pendientes y horizonte. Cambiar proveedor,
   ruta, BOM o existencias entre revisión y confirmación exige revisar de nuevo, sin efectos parciales.
3. Confirmar compra positiva: reconocer nueva RFQ o ampliación de línea existente y sus cantidades;
   confirmar/reintentar misma clave devuelve operación previa; otra cantidad con misma clave falla.
4. Confirmar fabricación normal: nueva/ampliada MO y estado nativo; tamaño de lote puede producir
   varias MO/más unidades explícitas. Revisar componentes/kits phantom sin sumar sus UOM como kit.
5. Lote de reglas con una inválida revierte todo; compañía/ACL/relaciones restringidas no filtran
   nombres/IDs ni permiten native sudo como bypass del actor. Reintentos concurrentes sin duplicación.
6. Nueva confirmación tras una parcial incorpora pipeline anterior. Mostrar/consumir el override manual usado y preservar
   triggers previos; scheduler automático y otros disparadores siguen siendo una decisión separada.
7. Volver de maestros conserva selección/cantidades; fecha/hora y cantidades con unidad, botones
   diferenciados, teclado, tema claro/oscuro y pantalla estrecha. PDF/impresión sólo en su revisión.

No ejecutar estos recorridos durante instalación técnica. El manifiesto, registry, vistas, roles,
fuentes, actualización/arranque y restauración se comprueban por separado, sin generar abastecimiento.


8. MO borrador previa compatible: aparece como posible confirmación en revisión y su cambio de
   estado queda capturado. Cambio de cantidad/confirmación que dispare faltantes de insumos mantiene
   permisos y atomicidad; fallo hijo no deja una raíz presentada como exitosa. Parámetros globales
   de scheduler intactos. Otra rama no revisada exige propuesta nueva sin reposición parcial.

9. El actor pierde lectura de una PO/MO/dimensión después de confirmar: read/search_read/web_read/
   export/read_group del recibo crudo siguen denegados; el replay no revela IDs/nombres/cantidades
   y no vuelve a ejecutar. La representación autorizada falla completa con explicación genérica.
