# Data model: Terceros ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Tercero | `res.partner` | name, is_company, parent_id, direcciones, contactos, vat, país | Una identidad por tercero; roles cliente/proveedor combinables |
| Roles | `arg.pyme.partner.role y extensión res.partner` | roles de gestión y vínculos nativos disponibles | No depender de customer_rank/supplier_rank cuando account no está instalado |
| Condiciones | `propiedades nativas y extensiones por compañía` | tarifa, plazo, moneda, contactos y domicilios | No inventar identificadores fiscales ni sobrescribir condiciones históricas |

## Estados, efectos y seguridad

- No fusionar registros por coincidencia parcial de nombre.
- Validar formato de CUIT separado de verificación remota de padrón.
- No activar consultas externas al guardar una ficha.
- Permitir importar ejemplos con clave estable y conservar ceros iniciales en códigos.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.
