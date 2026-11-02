# Data model: Integraciones ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Conector | `arg.pyme.integration.connector` | compañía, proveedor, ambiente, habilitado y referencia de secreto | Proveedor como adaptador interno; no nuevo addon por proveedor |
| Operación | `arg.pyme.integration.job` | clave, estado, hash de petición, intentos y referencia externa | Clave única por compañía/proveedor/ambiente/clave de operación comercial, independiente de rotación del conector |
| Adaptador | `services/providers/*` | prepare, validate, execute, lookup, redact | Error incierto no equivale a rechazo |

## Estados, efectos y seguridad

- No conservar payload sensible completo en logs.
- Estados draft, queued, processing, succeeded, failed, uncertain y canceled con transiciones explícitas.
- Timeout requiere lookup y conciliación antes de reintentar efectos irreversibles.
- Deshabilitar proveedor conserva jobs e historia. La desinstalación del addon requiere política explícita de conservación/exportación y no equivale a deshabilitar.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.
