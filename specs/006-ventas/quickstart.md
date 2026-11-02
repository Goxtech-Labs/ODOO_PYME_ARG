# Quickstart de validación posterior: Circuito Ventas ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Guardar PRE-000001, confirmarlo y consultar sus líneas/condiciones sin movimientos de stock ni dinero. Revisar además: bloquear cambios sobre la versión confirmada y permitir una revisión nueva con historia.
2. Generar PED-000001 separado, enlazar PRE-000001 y conservar ambos documentos consultables. Revisar además: rechazar generación duplicada concurrente y mostrar el pedido existente.
3. Consultar cantidades pedidas, entregadas y facturadas con sus documentos de origen y acceder al cobro de Administración. Revisar además: separar faltante cerrado de cantidad cumplida y no crear otra entrega al facturar.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.
