# Guía de validación posterior · Cartera de valores y tesorería argentina

No ejecutada durante planificación/desarrollo. Usar base aislada con ejemplos, correo/cron externos
desactivados y composición exacta de la entrega, nunca la demo compartida para crear efectos.

1. Instalar/actualizar sólo el addon previsto y registrar versión/dependencias.
2. Crear maestros mínimos de ejemplo y un usuario operador con compañía única.
3. Abrir documento nuevo: hoy propuesto, tercero y conceptos; descartar no crea efectos.
4. Ejecutar: Factura de120000ARS: REC con20000 efectivo y100000 cheque aplica120000 a deuda; efectivo20000, cartera100000 y banco acreditado0. Depositar no genera otro cobro; acreditar reclasifica. Un rechazo revierte/reclama sólo el valor vinculado, preservando efectivo e historia.
5. Repetir clave/evento; comprobar cero duplicados y corrección vinculada.
6. Probar fecha corregida/reapertura, rol restringido y cruce de compañía rechazado.
7. Consultar informe/origen con monedas separadas; registrar esperado/observado/evidencia.

Completar manual y aceptación personal aparte; un arranque exitoso no equivale a estos recorridos.

## Disponibilidad del incremento20.0.1.1.0

En aislado se prepararon maestros y CHQ-000001 en borrador mediante seed_values_demo.py, sin
REC/pagos/asientos nuevos. Los pasos monetarios anteriores NO fueron ejecutados. Este incremento
permite preparar QA de REC con cheque papel, depósito, acreditación completa y rechazo previo.
No ejecutar aún los escenarios ECHEQ/OPA/transmisiones/descuento/parciales como si estuvieran
implementados. El plan los conserva para incrementos posteriores.
