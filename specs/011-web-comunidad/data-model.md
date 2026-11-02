# Data model: Portada y documentación pública ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Página | `Markdown/SVG` | README, manifiesto, identidad y mapa | No publicar fotos/capturas ajenas sin permiso |
| Tutorial | `catálogo editable Base ARG y YAML editorial` | módulo, versión, URL, fecha de revisión, reemplazo | No URL ficticia activada |
| Aporte | `issue/PR documental` | spec, cambio propuesto, evidencia, autor | Publicación y envío externos requieren autorización correspondiente |

## Estados, efectos y seguridad

- El repositorio conserva documentación original y fuentes públicas con atribución.
- El sitio GitHub Pages es opcional posterior; README funciona sin desplegar otro servicio.
- No publicar credenciales, dumps, filestore ni referencias privadas de infraestructura.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.
