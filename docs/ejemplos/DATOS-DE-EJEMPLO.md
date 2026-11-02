# Datos y recorridos de ejemplo

Base aislada `arg_demo`, compañía «Ejemplo — Odoo Pymes ARG», ARS, país Argentina.
Tres terceros y tres productos identificables mediante XML IDs `arg_demo.*`.
Contactos con correo `example.invalid`, sin CUIT real. Producto A $10.000, Producto B $20.000,
Servicio A $15.000; importes ficticios. Depósito «Ejemplo — Depósito Principal».
El cargador `ops/seed_demo.py` es idempotente y sólo admite arg_demo; crea maestros, no operaciones publicadas.
No borra datos existentes ni reescribe contactos/productos encontrados por XML ID.
Sí vuelve a fijar compañía, depósito y acceso administrador del entorno de ejemplo; usar sólo para inicialización aislada.
No usar esta base para clientes reales o emisión fiscal. Configuración fiscal de ejemplo no acredita situación tributaria.

## Recorridos preparados para QA posterior

1. PRE por 2 unidades A: $20.000 antes de impuestos. Confirmar, mantener PRE y generar PED independiente.
2. Entregar 1 A en REM: entregado 1, pendiente 1. Facturar esa unidad según política; saldo sólo tras publicación.
3. Cobrar parcialmente $4.000 sobre factura cuyo total real se lee del documento: residual = total - aplicación.
4. PPC por 3 B; recibir 2 en ENT y conservar 1 pendiente. FRC no vuelve a aumentar stock.
5. Contar A en depósito, comparar existencia teórica real y aplicar diferencia mediante AJU con motivo.
6. Filtrar informe por moneda/fecha y comparar detalle con total, sin sumar PRE/PED/FAC como tres ventas.

Estos recorridos están preparados para QA posterior: no se ejecutaron como demostración del producto ARG.
La demo contiene maestros ficticios y doce addons ARG instalados técnicamente, sin operaciones de negocio.

[Inventario y retirada controlada de ejemplos](RETIRAR-EJEMPLOS.md).
