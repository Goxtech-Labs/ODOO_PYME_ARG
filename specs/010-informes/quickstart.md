# Quickstart de validación posterior: Circuito Informes ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Consultar facturación neta por fecha, tercero y producto con grano línea de factura. Revisar además: no sumar presupuesto con factura ni presentar cobro como venta.
2. Filtrar compañía, período y moneda y abrir las líneas que componen un total. Revisar además: rechazar comparación sin moneda homogénea y respetar acceso al documento original.
3. Exportar CSV UTF-8 y PDF con filtros, moneda, fecha y totales consistentes. Revisar además: proteger contra fórmulas en CSV y no exportar columnas restringidas.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.
