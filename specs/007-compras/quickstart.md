# Quickstart de validación posterior: Circuito Compras ARG

## Requisitos

Instalar dependencias y módulo desde una revisión fijada en un entorno de ejemplo.
Conservar datos de [ejemplos comunes](../../docs/ejemplos/DATOS-DE-EJEMPLO.md) y usuarios con roles controlados.
Mantener integraciones y envíos reales desactivados.

## Controles técnicos de la implementación

Usar el runtime confirmado en [entorno](../../docs/tecnica/ENTORNO-DEMO.md).
Comprobar sintaxis, manifest, carga de vistas, instalación/upgrade del módulo exacto y arranque.
Derivar comandos del servicio activo; no ejecutar actualizaciones globales por defecto.

## Escenarios reservados para QA posterior

1. Guardar PPC-000001 y confirmar condiciones conocidas sin exigir circuitos departamentales adicionales. Revisar además: mantener aprobación adicional sólo si el responsable la configura y preservar referencia del proveedor.
2. Recibir parte del pedido mediante ENT y registrar FRC vinculada sin duplicar entrada. Revisar además: conservar cantidades pendientes y distinguir recepción cerrada de cumplimiento total.
3. Generar devolución desde entrada y consultar su efecto neto y documentos relacionados. Revisar además: no descontar dos veces una devolución ni confundirla con cancelación del pedido.

Comprobar rol restringido, segunda compañía, navegación por teclado y ayudas de la versión.
Registrar evidencia técnica, QA funcional/visual y aceptación como estados distintos.

## Carga básica20.0.1.0.6 · escenarios preparados, no ejecutados

- FRC/NCP nueva: fecha propuesta antes de proveedor/referencia; corregirla y conservarla al guardar/reabrir.
- FRC preparada, listado PPC y enlaces de origen: mismo orden; valores conocidos sin nueva carga.
- Fecha del comprobante distinta de fecha contable/vencimiento: conservar significados y reglas nativas.
- Comprobante publicado: fecha readonly y referencia según modificadores nativos; sin perder avisos/errores.
- Otras fichas contables: FAC/NCV/asiento conservan sus bloques de fecha. Recibo proveedor nativo usa orden de proveedor.
- Roles contables restringidos/multiempresa, escritorio/angosto y teclado: no conceder acceso por presentación;
  proveedor con nombre largo, todas las condiciones visibles y errores localizables. Comparar ficha combinada real.
