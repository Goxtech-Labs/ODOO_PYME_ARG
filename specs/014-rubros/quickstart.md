# Quickstart de validación posterior: Extensiones por rubro y personalizaciones ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Completar plantilla con problema, documentos, campos mínimos y exclusiones. Revisar además: rechazar supuestos de otro cliente que contradigan la gestión genérica.
2. Proponer addon arg_pyme_rubro_nombre con extensiones y relaciones al núcleo. Revisar además: resolver conflicto entre reglas de rubros mediante composición explícita.
3. Encontrar manual, datos de ejemplo, tutorial y notas de compatibilidad por rubro. Revisar además: conservar datos al deshabilitar menús y documentar límites de desinstalación.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.
