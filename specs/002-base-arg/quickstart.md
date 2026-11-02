# Quickstart de validación posterior: Base ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Asignar PRE-000001 y PED-000001 desde secuencias independientes y conservar ambos códigos. Revisar además: rechazar una colisión, conservar números anulados y permitir crecimiento por encima de seis dígitos.
2. Asignar a una persona Ventas, Compras y Administración según permisos expresos. Revisar además: rechazar acceso a otra compañía o acción fuera de permisos efectivos.
3. Actualizar un enlace YouTube central sin reinstalar el módulo y encontrarlo desde su ayuda. Revisar además: mostrar guía escrita y estado pendiente cuando falte un video o canal de contacto.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.
