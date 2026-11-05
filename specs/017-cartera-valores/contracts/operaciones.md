# Contrato · Cartera de valores y tesorería argentina

## Entrada mínima

Recibir un cheque o registrar uno propio, identificarlo una sola vez y usarlo como medio de REC/OPA. Fecha de hoy propuesta, tipo desde la tarea y número automático; conservar valores existentes.

## Efectos y límites

Separar nominal disponible, aplicación de deuda, dinero acreditado/debitado y exposición por recurso. REC/OPA multim medio usa cuentas transitorias de valores y conciliación nativa, nunca residuales escritos a mano.

- El nominal es positivo, en la moneda del instrumento, y no cambia después del primer evento confirmado.
- Un instrumento no puede estar reservado o comprometido simultáneamente por dos salidas.
- Transmitir el título no fracciona su identidad; imputar su importe a varias facturas es otra operación.
- El nominal en cartera no es dinero bancario disponible ni se vuelve a cobrar al liquidarlo.
- Evento confirmado es inmutable; reversión explícita enlazada conserva historia y revisa su efecto contable.
- La integración bancaria no se ejecuta desde un formulario de cartera ni se infiere de una referencia manual.

## Flujo

Recepción → cartera → endoso/entrega, depósito o negociación → liquidación o rechazo; propio → emisión registrada → entrega → débito o devolución.
Validar permiso/compañía, precondición y clave estable de operación; confirmar atómicamente identidad,
evento y efecto. Los errores no dejan marcas de completado. Frente a operación externa incierta,
consultar estado antes de repetir mediante Integraciones ARG. No enviar al cargar ni abrir pantalla.

## Escenario de referencia

Factura de120000ARS: REC con20000 efectivo y100000 cheque aplica120000 a deuda; efectivo20000, cartera100000 y banco acreditado0. Depositar no genera otro cobro; acreditar reclasifica. Un rechazo revierte/reclama sólo el valor vinculado, preservando efectivo e historia.

## Contratos compartidos

- [Interfaz](../../001-pyme-argentina/contracts/interfaz.md).
- [Administración](../../009-administracion/contracts/operaciones.md).
- [Integraciones](../../012-integraciones/contracts/operaciones.md).
- [Documento](../../015-documentos/contracts/operaciones.md).
