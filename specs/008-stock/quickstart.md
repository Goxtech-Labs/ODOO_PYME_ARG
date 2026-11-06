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
