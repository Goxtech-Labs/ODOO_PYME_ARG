# Contrato de operaciones: Catálogo y precios ARG

**Alcance**: Gestionar productos y servicios genéricos, listas de precios y atributos opcionales mediante fichas y matrices simples.

## Recorridos y datos mínimos

### Operación 1: Crear producto o servicio

Como operador necesito identificar qué vendo o compro con los mínimos datos.

**Resultado**: Crear un producto de ejemplo con nombre, tipo, unidad y precio sin completar atributos de un rubro ajeno.
**Excepción**: Exigir lote o depósito sólo cuando la capacidad y el producto lo requieran.

### Operación 2: Actualizar precios

Como responsable necesito editar listas en una matriz sin perder correspondencia producto/lista.

**Resultado**: Filtrar productos y editar precios en columnas alineadas, revisando antes de guardar.
**Excepción**: Conservar cambios pendientes al filtrar y detectar modificaciones concurrentes.

### Operación 3: Extender sin imponer rubro

Como pyme genérica necesito agregar variantes sólo cuando correspondan.

**Resultado**: Agregar un atributo opcional y conservar el mismo catálogo y sus referencias.
**Excepción**: Evitar generar combinaciones innecesarias o reinterpretar un servicio como existencia física.

## Invariantes

- No modificar stock físico como efecto de editar catálogo o tarifa.
- Conservar reglas nativas de precio y descuentos configurados.
- No guardar automáticamente al aplicar filtros.
- Evitar enviar todas las imágenes o variantes al navegador.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.
