# Quickstart de validación posterior: Integraciones ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Crear configuración por compañía y entorno con secreto referenciado fuera de Git. Revisar además: deshabilitar por defecto y detectar configuración incompleta sin revelar claves.
2. Encolar una operación con clave idempotente y registrar resultado sanitizado. Revisar además: resolver timeout como estado incierto y consultar proveedor antes de repetir.
3. Pausar proveedor y consultar intentos sin contenido sensible. Revisar además: conservar evidencia al rotar credenciales o revocar servicio.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.
