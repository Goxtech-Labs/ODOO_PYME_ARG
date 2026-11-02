# Lote conciliable previsto: hechos y dimensiones

Datos ficticios para QA posterior. No se cargaron como documentos de negocio en la demo.
Una compañía, ARS, producto A en Unidad, todos los documentos del mismo período. Los importes son
netos y sin impuestos en el ejemplo didáctico; las operaciones reales usan su configuración efectiva.

| Hecho | Documentos | Medida esperada |
| --- | --- | --- |
| Propuesta | PRE por10A a$100 | $1.000propuestos; no son venta ni caja |
| Pedido | PED por10A | 10pedidos; no sumar con PRE |
| Entrega | REM de4A | 4entregados,6pendientes |
| Venta facturada | FAC de2A a$100 | 2facturados y$200netos;8pendientes de facturar |
| Cobro | REC confirmado$80, aplicado a FAC | Caja/registro$80según medio; cobrado parcial, deuda$120 |
| Corrección comercial | NCV de1A por$100 | Facturación neta1A/$100; no crea salida de dinero por sí sola |
| Aplicación de nota | NCV$100contra FAC | Deuda$20; dinero aplicado sigue$80 |

Comparar detalle y agrupación por misma moneda, fecha y signo. Un vínculo no duplica importes:
REC mantiene un único ingreso aunque cubra varias cuotas. La nota no es cobro ni devolución física.
Si además vuelve1A al depósito, registrar DCL separado y descontarlo del hecho físico de entregas.
El pedido conserva alcance facturado y cobro sobre lo facturado como indicadores distintos.

## Compra y stock

PPC por3B; ENT por2B; FRC por1B. Recepción2/3 y facturación1/3 son parciales diferentes.
FRC no vuelve a sumar stock. Devolución DCP de1B y NCP por1B son hechos separados.
Un traslado interno entre ubicaciones resta de origen y suma a destino; no altera físico total propio.
Para comparar stock a fecha, normalizar unidades base nativas y cortar movimientos efectivos en la misma zona horaria.

## Validación posterior

Preparar casos con segunda moneda, cuotas, descuentos, notas, devoluciones, pago agrupado y permisos
restringidos. El resultado no determinado se conserva cuando no hay evidencia suficiente de dinero.
Registrar esperado/observado y documentos que explican cada diferencia; no convertir estos resultados
previstos en un informe de pruebas ejecutadas.
