# Quickstart de validación posterior: Circuito Administración ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Consultar facturas publicadas y saldos residuales separados por moneda y compañía. Revisar además: excluir borradores y no sumar ARS con USD ni confundir una relación con una conciliación.
2. Crear REC u OPA con un medio y aplicar un pago parcial conservando saldo pendiente. Revisar además: permitir anticipo sin factura y exigir cuentas transitorias configuradas antes de contabilizar.
3. Consultar caja por diario y fecha y revertir una aplicación conservando historial. Revisar además: impedir borrar evidencia publicada y distinguir caja, banco, deuda y conciliación.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.
