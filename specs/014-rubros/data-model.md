# Data model: Extensiones por rubro y personalizaciones ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Rubro | `specs/NNN-rubro-nombre` | casos, documentos, dimensiones, dependencias | No seleccionar rubro inicial sin decisión de producto |
| Extensión | `addons/arg_pyme_rubro_nombre` | campos, métodos, vistas y permisos | No bifurcar core |
| Composición | `manifest de instalación` | versiones y módulos compatibles | Incompatibilidades explícitas |

## Estados, efectos y seguridad

- Indumentaria, comercio, servicios y otros rubros son candidatos, no funciones prometidas en el núcleo.
- Una regla exclusiva de cliente permanece en su personalización.
- Toda integración externa nueva se registra en Integraciones ARG.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.
