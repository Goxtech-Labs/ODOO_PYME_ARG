# Research: Circuito Administración ARG

Fecha: 2026-11-01. Separar comportamiento nativo comprobado y decisiones de diseño ARG.

## Decisiones

### D01

**Decision**: Un wrapper documental agrupa medios y pagos; account.move.line continúa siendo la fuente del saldo.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D02

**Decision**: El vínculo invoice_ids puede existir sin conciliación y no acredita cancelación de deuda.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

### D03

**Decision**: La primera entrega admite efectivo, transferencia y anticipo registrados; cheques y conciliación bancaria automatizada requieren incremento posterior específico.
**Rationale**: Mantener fuente única, simplicidad operativa y extensibilidad compatible.
**Alternatives considered**: Duplicar circuitos/libros o modificar core; descartar por costo de mantenimiento y divergencia.

## Fuentes primarias

- [Fuente oficial 1](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/account/models/account_payment.py)
- [Fuente oficial 2](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/account/wizard/account_payment_register.py)
- [Fuente oficial 3](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/account/models/account_move_line.py)
- [Fuente oficial 4](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/account/models/account_partial_reconcile.py)

Consultar además [investigación general](../001-pyme-argentina/research.md) y [hallazgos nativos](../../docs/tecnica/DECISIONES-ODOO20.md).
Registrar revisión exacta y dependencias antes de instalar un addon. La existencia de un modelo no acredita cobertura Enterprise.

## Fuente runtime confirmada y atribución monetaria

Se inspeccionaron los archivos exactos del paquete instalado Odoo20.0.20261101 (entorno aislado),
conservados en caché local fuera del NAS. No confundir el SHA upstream de investigación con el build instalado.

La revisión estática independiente identificó límites para la implementación pendiente de cobros/pagos:

- Enumerar conciliaciones con `_get_reconciled_invoices_partials()`: conserva parcial, importe del lado factura y contraparte.
- `payment_id` y asiento publicado requieren estructura monetaria verificable; `invoice_ids` no acredita aplicación.
- El ratio de balances en moneda compañía puede distorsionarse por redondeo. El dinero debe explicarse en moneda del pago y convertirse con el parcial histórico.
- Priorizar descuento por pronto pago por factura, según `_get_payment_term_epd_info()` y `_is_early_payment_discount_applied()`, antes de prorratear ajustes genéricos. Un pago agrupado196 para facturas100+100 con descuento4 sólo en la primera no atribuye98+98: corresponde96+100.
- `_seek_for_lines()` tiene fallback que puede reclasificar ajustes como liquidez; validar las cuentas efectivas.
- Varias contrapartes, ajustes/retenciones complejos o estructura monetaria no demostrable requieren mostrar importe monetario no determinado, sin inferir cobro0 ni100%.
- `statement_line_id` por sí solo tampoco demuestra que todo el importe conciliado sea dinero. Inspeccionar su fuente antes de implementar ese adaptador.
- Recalcular desde parciales vigentes después de desaplicar, preservando evidencia inmutable separada.

Revisión de fuentes por otra sesión Codex de la misma familia/cuenta; sin independencia de modelo ni QA funcional.
No se ejecutaron pagos, conciliaciones ni operaciones contables.
