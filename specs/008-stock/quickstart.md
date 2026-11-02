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
