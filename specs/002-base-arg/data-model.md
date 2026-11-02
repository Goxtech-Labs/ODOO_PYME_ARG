# Data model: Base ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Tipo documental | `arg.pyme.document.type` | code, name, model, compañía, secuencia | Prefijo de 2 a 4 letras ASCII; secuencia independiente por compañía y tipo |
| Referencia | `arg.pyme.document.identity` | tipo, compañía, número, registro origen, código mostrado | Unicidad por compañía, tipo y número; código asignado inmutable |
| Ayuda | `arg.pyme.help.resource` | módulo, tarea, URL, versión, guía, estado, revisión, sustituto | No mostrar un enlace ficticio como tutorial disponible |
| Soporte | `res.config.settings + ir.config_parameter` | URL general, canal principal, correo, WhatsApp, tickets | Sólo administradores modifican destinos; no guardar credenciales de proveedores aquí |

## Estados, efectos y seguridad

- No reutilizar códigos anulados ni reiniciar por ejercicio implícitamente.
- Conservar código interno separado del número fiscal y del proveedor.
- Mantener compañía, zona horaria e idioma explícitos.
- Compartir configuración única de soporte; capturar contexto opcional sin exigirlo al usuario.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.

## Contrato de identidad v1

Base mantiene arg.pyme.document.identity con company_id, document_type_id, number (entero),
code (texto almacenado), document_model y document_res_id. Unicidad compañía/tipo/número y registro origen/tipo.
El mixin de Documentos guarda identity_id y expone arg_number/tipo como relacionados de sólo lectura,
no un segundo contador. Asignación y vínculo en la misma transacción; secuencia nativa con huecos admitidos.
No guardar importes, líneas ni saldos en el registro de identidad. El origen conserva permisos y compañía.
La navegación genérica verifica allowlist de modelos documentales y acceso al registro sin sudo.
Códigos iniciales de tres letras según docs/tecnica/DICCIONARIO-DOCUMENTAL.md; nuevas definiciones pueden usar 2–4 letras.
