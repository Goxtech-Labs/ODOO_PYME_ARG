# Contrato de operaciones: Circuito Informes ARG

**Alcance**: Informes con hechos, dimensiones, unidades y corte claros para decidir sin conocimientos contables avanzados.

## Recorridos y datos mínimos

### Operación 1: Leer hechos separados

Como responsable necesito distinguir ventas, entregas, cobros, compras y existencias.

**Resultado**: Consultar facturación neta por fecha, tercero y producto con grano línea de factura.
**Excepción**: No sumar presupuesto con factura ni presentar cobro como venta.

### Operación 2: Filtrar y explicar

Como usuario necesito partir de pocos filtros y abrir el documento de origen.

**Resultado**: Filtrar compañía, período y moneda y abrir las líneas que componen un total.
**Excepción**: Rechazar comparación sin moneda homogénea y respetar acceso al documento original.

### Operación 3: Exportar e imprimir

Como responsable necesito sacar un informe utilizable fuera del sistema.

**Resultado**: Exportar CSV UTF-8 y PDF con filtros, moneda, fecha y totales consistentes.
**Excepción**: Proteger contra fórmulas en CSV y no exportar columnas restringidas.

## Invariantes

- Comparar total de detalle y agrupado por igual corte y moneda.
- Notas de crédito y devoluciones tienen signo explícito y vínculo al original.
- Stock actual y stock a fecha son consultas diferentes; el histórico se deriva de movimientos.
- No depender de account_reports Enterprise; usar modelos/reportes Community. Habilitar cada informe sólo si su modelo fuente está instalado; Informes no obliga a instalar todos los circuitos.
- Aplicar precisión de moneda/unidad, sin redondear cada agrupación de forma inconsistente.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.

Contrato de estados y pendientes: [v1](../../../docs/tecnica/ESTADOS-Y-PENDIENTES.md). Aplicar pendiente/parcial/completo por eje y conservar cantidades/importes explicables.
