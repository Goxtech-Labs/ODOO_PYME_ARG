# Data model: Circuito Informes ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Hecho facturación | `account.move.line/account.invoice.report` | línea publicada, signo, cantidad, neto, moneda, fecha contable | No es caja ni presupuesto |
| Hecho caja y deuda | `account.move.line/account.partial.reconcile` | liquidez y residuales separados de aplicaciones | No repetir pago por cada factura relacionada |
| Dimensiones | `res.company/res.partner/product.product/res.currency` | compañía, tercero, producto, moneda, depósito, fecha | Reglas de acceso también en consultas SQL y exports |

## Estados, efectos y seguridad

- Comparar total de detalle y agrupado por igual corte y moneda.
- Notas de crédito y devoluciones tienen signo explícito y vínculo al original.
- Stock actual y stock a fecha son consultas diferentes; el histórico se deriva de movimientos.
- No depender de account_reports Enterprise; usar modelos/reportes Community. Habilitar cada informe sólo si su modelo fuente está instalado; Informes no obliga a instalar todos los circuitos.
- Aplicar precisión de moneda/unidad, sin redondear cada agrupación de forma inconsistente.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.

## Implementación del incremento1.0

arg.pyme.report.query: TransientModel de filtros (hecho, compañía, moneda, fecha desde/hasta,
tercero, texto producto/ubicación, agrupación, página). Reglas globales por dueño/compañía y ACL Informes
ARG/Administrador ARG. No concede ACL a fuentes nativas ni copia filas a tablas de negocio.
arg.pyme.report.engine: AbstractModel que lee ORM y genera metadatos/filas/totales en memoria del servidor.
Las rutas CSV y el modelo QWeb reciben sólo el ID de consulta; no aceptan resultados del cliente.

Hechos implementados: ventas/compras por línea de factura publicada; líneas de PED/PPC confirmado;
liquidez publicada; residuales clientes/proveedores actuales por cuota; aplicaciones contables vigentes;
movimientos físicos terminados; quants actuales; reconstrucción stock a fecha por extremos internos.
La moneda se fija por consulta; aplicaciones usa moneda de compañía. Sin conversión gerencial implícita.
Stock usa UOM base y quantity_product_uom almacenado nativo; agrupaciones conservan unidad y circuito.
Notas/retornos conservan signo y enlace al documento original. Ejes ARG se consultan sin escribirse.
