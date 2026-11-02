# Data model: Motor documental e impresión ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Identidad | `mixin abstracto arg.pyme.document.mixin` | company_id, arg_document_type_id, arg_number y display code | Número único por compañía/tipo |
| Relación | `campos relacionales específicos y adaptador de navegación` | quote_id, quotation_line_id, sale_line_id y relaciones nativas | No usar sólo origin textual |
| Impresión | `ir.actions.report/QWeb` | layout, marca, totales y metadatos | Documento fiscal sólo con estado/autorización válidos |

## Estados, efectos y seguridad

- Presupuesto y pedido son documentos distintos, no dos vistas o estados del mismo sale.order.
- Los documentos nativos conservan su name técnico cuando sea necesario; arg_number se muestra como identificador interno ARG.
- Confirmar PRE preserva condiciones y no genera PED automáticamente; Generar pedido es la acción explícita posterior e idempotente. Ninguna de las dos registra por sí sola asiento, cobro ni movimiento de stock.
- Códigos estables; nunca renumerar documentos existentes al cambiar configuración.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.

Identidad almacenada sólo en Base: mixin.arg_identity_id y campos relacionados de sólo lectura.
No asignar otro contador al mismo documento. Aplicar contrato de identidad de specs/002-base-arg/data-model.md.
