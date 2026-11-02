# Quickstart de planificación y validación posterior

## Revisar esta entrega documental

Desde la raíz del checkout, consultar constitución, spec, plan y tareas.
Ejecutar comprobaciones documentales oficiales de Spec Kit:

```bash
bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
```

Consultar [README](../../README.md), [plan maestro](../../docs/PLAN-MAESTRO.md)
y [contrato documental](contracts/documentos.md).

## Preparar la implementación

Elegir el primer módulo del catálogo y crear su spec independiente.
Fijar revisión Community y dependencias en `composition/versions.lock.json` al preparar runtime.
Crear base aislada de demostración, usuario administrador y roles operativos.
Mantener conectores desactivados y ejemplos etiquetados.
Derivar comandos de instalación del runtime confirmado; no existen todavía scripts operativos del producto.

## Escenarios para QA posterior

Preparar estos recorridos cuando los módulos estén instalados; no ejecutarlos en esta fase documental.

1. Guardar dos presupuestos con cliente/producto existentes. Comprobar carga mínima y códigos correlativos.
2. Generar pedido desde presupuesto; entregar parcialmente, facturar y registrar cobro parcial.
   Comprobar estados, pendientes y trazabilidad sin duplicar líneas ni importes.
3. Crear pedido proveedor; recibir parcialmente, registrar factura recibida y realizar pago imputado.
4. Transferir entre depósitos e inventariar una diferencia. Comprobar neutralidad del traslado empresarial.
5. Consultar facturación, stock y caja por separado. Conciliar cada hecho con sus documentos fuente.
6. Cambiar tema y recorrer listados, ficha, matriz, mensajes y PDF; comprobar marca y orden constantes.
7. Acceder mediante rol restringido y segunda compañía; comprobar aislamiento de lectura y exportación.
8. Restaurar una copia completa de ejemplo en otro entorno y verificar documentos, adjuntos y relaciones.
9. Consultar portada y manuales; encontrar propósito, estado, instalación y contribución sin enlaces rotos.

Registrar evidencia separada de instalación, QA funcional, QA visual y aceptación del usuario.
