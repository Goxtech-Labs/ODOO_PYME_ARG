# Quickstart de validación posterior: Motor documental e impresión ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Abrir PRE-000001 y distinguir su número interno de referencias fiscales o externas. Revisar además: no reutilizar una secuencia cancelada ni mezclar compañías.
2. Desde PRE confirmado abrir PED distinto con trazabilidad de cada línea. Revisar además: impedir un segundo PED por reintento de la misma confirmación.
3. Generar PDF con identidad ARG, tercero, detalle, totales y estado correcto. Revisar además: marcar borrador/ejemplo y no mostrar autorización fiscal inexistente.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.

4. Revisar los seis escenarios transversales de parciales de spec.md: PED con entrega/facturación diferentes,
REC parcialmente aplicado, factura parcial cobrada sin presentar completo el cobro del pedido,
REC en borrador sin efecto, cobro parcial con saldo y cierre con faltante.
Ver [guía de estados](../../docs/usuario/ESTADOS-DOCUMENTALES.md). Escenarios sin ejecutar.
