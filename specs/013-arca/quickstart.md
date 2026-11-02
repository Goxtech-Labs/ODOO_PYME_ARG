# Quickstart de validación posterior: Contrato futuro ARCA dentro de Integraciones ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Validar configuración de homologación sin usar CUIT o certificados reales del usuario. Revisar además: bloquear producción sin configuración y autorización específicas.
2. Preparar solicitud consistente y registrar autorización, rechazo o resultado incierto. Revisar además: consultar último autorizado ante timeout antes de solicitar otra numeración.
3. Distinguir borrador, pendiente, autorizado y rechazado en pantalla e impresión. Revisar además: no imprimir CAE ficticio ni borrar un comprobante autorizado.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.
