# Quickstart de validación posterior: Terceros ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Guardar un contacto de ejemplo con nombre y rol y continuar el documento. Revisar además: permitir borrador sin datos fiscales desconocidos y señalar requisitos antes de la operación que los necesita.
2. Agregar rol proveedor a un cliente y conservar identidad, contactos e historia. Revisar además: advertir posibles duplicados sin fusionar automáticamente identidades diferentes.
3. Aplicar moneda, tarifa, plazo y dirección conocidas al crear un documento. Revisar además: conservar corrección explícita del usuario y no completar con datos inventados.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.
