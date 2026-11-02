# Data model: Experiencia y presentación ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Preferencias visuales | `res.users/res.company extendidos` | tema, densidad y preferencias | Guardar y Descartar mantienen significado semántico en ambos temas |
| Contexto de navegación | `menuService y acciones OWL` | área, acción, filtros, retorno | Respetar permisos y guardas nativas de salida |
| Bot | `base.partner_root + mail.bot` | nombre/avatar/textos vigentes e inventario | No crear otro usuario ni cambiar XML IDs del bot |

## Estados, efectos y seguridad

- Guardar no confirma entregas, contabilización, cobros ni emisión fiscal.
- Conservar callbacks y validaciones nativas de formularios.
- No ocultar errores mediante sudo o eliminación de grupos.
- Mantener texto e icono además del color; proponer contraste 4,5:1 para texto normal.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.
