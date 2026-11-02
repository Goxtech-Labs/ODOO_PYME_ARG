# Identidad visual y objetos comunes

Estado: identidad, assets y componentes comunes instalados; comprobación visual parcial realizada, aceptación pendiente.

## Identidad argentina

Usar ARG como identidad principal y sufijo visible de los módulos de este proyecto.
Aplicar `arg_pyme_*` como namespace técnico original y mantener las convenciones de otros proyectos intactas.

Usar celeste y blanco como identidad general; incorporar un sol geométrico original como acento.
Mantener superficies limpias, bordes suaves y densidad adecuada para gestión administrativa.
Usar la marca de la pyme en documentos comerciales y una firma Goxtech secundaria.
Evitar depender de fuentes, imágenes o iconos alojados externamente para la gestión interna.

| Token / variante | Color | Uso |
| --- | --- | --- |
| `arg-celeste` | `#74ACDF` | Bandas, selección suave y marca |
| `arg-panel` (claro) | `#FFFFFF` | Superficies claras |
| `arg-sol` | `#F6C344` | Acento de identidad; evitar texto blanco sobre este fondo |
| `arg-primary` | `#145B91` | Acción primaria y enlaces sobre fondo claro |
| `arg-text` | `#172B3A` | Texto principal claro |
| `arg-muted` | `#526474` | Texto secundario |
| `arg-border` | `#CCD7E0` | Límites y separadores |
| `arg-save` | `#157347` | Guardar y éxito con texto/icono |
| `arg-danger` | `#B42318` | Descartar y error con texto/icono |
| `arg-bg` (oscuro) | `#111C26` | Fondo oscuro |
| `arg-panel` (oscuro) | `#1B2B38` | Superficie oscura |

Definir variantes completas de texto, foco, borde y selección para ambos temas.
Evitar usar el celeste claro como texto pequeño sobre blanco.
Medir contraste por combinación efectiva durante la revisión visual.

## Objetos visuales

| Objeto | Contrato común |
| --- | --- |
| Área | Nombre estable, icono y posición persistente |
| Cinta contextual | Acciones agrupadas por documento y estado |
| Botón | Texto claro, icono coherente, foco visible y motivo de deshabilitación |
| Estado | Texto + icono + color semántico; significado estable |
| Ficha | Secciones constantes y datos avanzados progresivos |
| Matriz documental | Producto, descripción, unidad, cantidad, precio, descuento, impuesto y total |
| Matriz de precios | Productos por fila y listas por columna |
| Filtro | Campo reconocible, combinación explícita y limpieza accesible |
| Referencia | Código corto legible y acceso al documento relacionado |
| Indicador | Nombre de medida, período, moneda y acceso al origen |
| PDF | Marca de la pyme, identidad documental y totales legibles |
| Mensaje | Problema concreto, campo afectado y siguiente acción |

Crear iconos propios o incorporar una biblioteca abierta con atribución y versión registradas.
Mantener Guardar verde, Descartar rojo y auxiliares neutros en todos los módulos.
Conservar Guardar y nuevo y Guardar y cerrar cuando reduzcan pasos repetitivos.
No equiparar Guardar con confirmar, entregar, contabilizar o enviar.

## Branding mínimo Goxtech

Mostrar GOXTECHBOT como nombre del bot nativo y aplicar avatar/textos propios discretos.
Tratarlo como excepción explícita a la identidad ARG, limitada al branding suave del asistente.
Mantener identidad del producto y nombres de módulos en ARG.

Mostrar «Proyecto comunitario impulsado por Gonzalo Sarubilo · GoxtechLabs» en portada y Acerca de.
Incluir un perfil visible del autor y su experiencia, manteniendo ARG como identidad del producto.
Identificar al presentador en YouTube y conservar la marca de cada pyme en sus documentos.
Reservar consultoría y servicios profesionales para una sección secundaria y opcional.
Evitar marcas de agua, promociones y logos dominantes en pantallas operativas.
Ofrecer firma documental discreta configurable, respetando atribuciones legales aplicables.
Conservar libertad de personalización de la pyme.

## Portada del repositorio

Presentar banner argentino, descripción, principios, circuitos, estado real y acceso a documentación.
Usar enlaces directos como llamadas a aprender, revisar el plan y contribuir.
No mostrar botones de descarga, badges de pruebas o capturas de producto inexistentes.
Planificar web documental estática usando el mismo contenido y sistema visual.

Mostrar columnas/indicadores separados de confirmación, entrega/recepción, facturación y cobro/pago, con pendiente/parcial/completo y cantidades/importes. Ver docs/tecnica/ESTADOS-Y-PENDIENTES.md. No condensar ejes distintos en un solo color.

Los iconos de áreas y acciones comunes usan Lucide 1.66.0 local (ISC/Feather MIT); los estados originales conservan su atribución. Los iconos son decorativos;
el nombre accesible sigue siendo el texto del control. No agregan fuentes o peticiones externas.
Acerca de ARG se ofrece desde el menú de usuario y los pies de ayuda mediante /arg/acerca.

## Cinta de gestión y superficies de entrada

Inicio, Ventas, Compras, Stock, Administración e Informes mantienen un orden fijo. Configuración
se incorpora sólo para roles con acciones permitidas. Las pestañas seleccionan grupos de comandos;
abrir un documento conserva las guardas nativas. La cinta se contrae y se desplaza horizontalmente
en pantallas estrechas. Documentos/operaciones se separan de datos/catálogos y ayuda comunitaria.

Texto, números y fechas editables usan borde visible y fondo de escritura; selecciones conservan
flecha y autocompletar nativos. La lectura conserva etiquetas; no se convierte un valor protegido
en entrada ni se ocultan validaciones. Foco y texto acompañan el color de cada acción.

Celeste #74ACDF, azul operativo #145B91, blanco y acento solar #F6C344; superficies oscuras adaptadas.
Lucide se sirve desde el addon sin CDN. [Recursos y procedencia](RECURSOS-VISUALES.md).
