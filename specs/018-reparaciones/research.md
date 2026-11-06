# Investigación · Reparaciones y servicio técnico ARG

**Fecha**: 2026-11-05. Diseño, no verificación funcional.

## Decisión

Crear/extender `arg_pyme_reparaciones` opcional sobre arg_pyme_ventas, arg_pyme_stock, arg_pyme_documentos; evaluar repair y product/stock como candidatos Community; verificar composición exacta.

## Razonamiento

Consumir/devolver repuestos mediante stock nativo; mano de obra como servicio; facturar desde el documento comercial vinculado sin duplicar pedido ni consumo. La independencia del núcleo evita imponer un rubro a todas las pymes.

## Alternativas

Copiar pantallas españolas o duplicar libros fue descartado: cambia identidad y pierde trazabilidad.
Una dependencia nativa se prefiere si su licencia/API y su interacción con hooks ARG son compatibles;
no se declara probada antes de inspección. Las funciones propias se desarrollan desde cero.

## Fuentes

Ver [investigación coordinada](../016-expansion-argentina/research.md), contratos actuales y composición.
Referencias pertinentes: FactuSOL partes. Políticas de cuentas, bancos y garantías se fijan con
configuración versionada; nunca usar una fuente española como normativa argentina.

## Límite de certeza

La selección de APIs/clases y dependencias mínimas se cierra al inspeccionar las fuentes fijadas y
contrastar el runtime antes de instalar. No autoriza instalar candidatos por anticipado.

## Inspección de fuente fijada y decisión de recepción

Revisión pública Odoo bb238af6f0ddd70d7ff91521c6104472583661d1, ya usada en investigación de esta
composición. Se leyó [manifest repair](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/repair/__manifest__.py)
(LGPL-3, dependencias sale_stock/sale_management), modelos repair/stock_move/sale_order y ACL.
La inspección de esta fuente no demuestra igualdad de todos los archivos del paquete instalado.

El [modelo nativo](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/repair/models/repair.py)
crea venta/factura por sus acciones y, al completar con producto a reparar, prepara un movimiento
del producto y evalúa su propietario en existencias. No usar esas acciones como recepción física
de un equipo libremente descripto ni como sustitución del contrato PRE/PED ARG.

Decisión: parte propio REP sin producto obligatorio ni efectos de stock del equipo; eventos de
custodia propios. Stock/contabilidad siguen nativos para repuestos y facturación futura. No instalar
repair como dependencia ni usar sus generadores comerciales en este primer incremento. No es
rechazo global del candidato: una futura adopción requiere verificar esos efectos y su composición.
T001 tiene evidencia de fuente; instalación y compatibilidad de los puentes continúan pendientes.

## Fuentes del puente de trabajo1.1

También se inspeccionó la revisión fijada de
[sale.order.line](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/sale/models/sale_order_line.py),
[sale_stock](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/sale_stock/models/sale_order_line.py)
y [unidades](https://github.com/odoo/odoo/blob/bb238af6f0ddd70d7ff91521c6104472583661d1/addons/uom/data/uom_data.xml).
Servicios manuales admiten cumplimiento nativo editable; consumibles con sale_stock derivan de
movimientos. El clasificador de stock acepta un contexto de corte accrual_entry_date: se elimina
para controles actuales, y el neto se toma de movimientos terminados, no del float almacenado.

La inicialización sobre new() usa el cálculo nativo de método con cumplimiento cero explícito,
evitando que preferencias ir.default conviertan un borrador en trabajo realizado. Es una preparación
virtual, sin crear documentos ni stock. Las unidades de ejemplo unidad/hora existen en esa fuente.
Estas lecturas y la revisión estática no acreditan registro, migración ni funcionamiento del runtime.
