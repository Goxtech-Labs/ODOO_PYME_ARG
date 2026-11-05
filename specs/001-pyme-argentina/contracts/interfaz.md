# Contrato visual y de interacción

## Separación visual

Mantener cinco áreas: Ventas, Compras, Stock, Administración e Informes.
Ubicar Configuración y Ayuda como accesos auxiliares; agregar Integraciones ARG en una etapa posterior.
Mantener navegación de área, cinta contextual, listado y ficha en niveles distinguibles.
Conservar listado y filtros al cerrar una ficha y permitir volver sin perder contexto.

## Orden común

| Nivel | Orden estable |
| --- | --- |
| Área | Resumen → documentos/operaciones → maestros → configuración del área |
| Listado | Título/tipo → acciones → búsqueda/filtros → tabla → paginación/totales |
| Documento | Fecha → tercero → identificación del documento → conceptos/artículos → totales → acciones de negocio |
| Ficha maestra | Identificación → contacto → condiciones → información adicional |
| Informe | Hecho/medida → período → dimensiones/filtros → resultado → origen/exportación |

Mantener acciones de guardado en una ubicación fija y distinguirlas de confirmar efectos de negocio.
Evitar formularios diferentes para documentos equivalentes entre compras y ventas.
Usar secciones avanzadas para datos infrecuentes, conservando el orden de lectura.

## Practicidad argentina · decisión 2026-11-05

El recorrido principal responde cuándo, a quién y qué se registra. Proponer fecha de hoy al crear,
usando la zona horaria efectiva del usuario. No modificar fechas ya elegidas, históricas, importadas
o heredadas del origen al abrir, recargar, revisar o confirmar. Vencimiento no equivale a fecha de registro.
El tipo se deduce de la tarea abierta; código y numeración propios se asignan automáticamente.
Pedir sólo referencias externas necesarias y no obligar a volver a elegir información conocida.
Conceptos/artículos ocupan el detalle principal. Condiciones adicionales quedan en secciones secundarias;
compañía, moneda, depósito, listas, impuestos y diarios se resuelven desde configuración válida.
Un valor desconocido no se inventa: explicar qué falta y pedirlo cuando sea indispensable para el efecto.
Una sola persona puede completar el circuito con los roles permitidos. Conservar controles y trazabilidad,
sin imponer una estructura de personal grande. La adopción en pantallas instaladas debe verificarse por entrega.

## Acciones

Mostrar Nuevo, Editar, Guardar, Guardar y nuevo, Guardar y cerrar, Descartar y Volver según contexto.
Mantener Guardar verde, Descartar rojo y acciones auxiliares neutras recuadradas.
Mostrar una acción principal por estado y nombrar su efecto: confirmar pedido, validar entrada, registrar cobro.
Conservar validaciones, atajos, cambios enfocados y guardas nativas ante salida sin guardar.
Reservar eliminación para borradores permitidos; indicar motivo cuando una acción no esté disponible.

## Matrices

Mantener encabezados alineados, SKU textual, importes alineados a la derecha y unidad/moneda visibles.
Permitir teclado, filtros combinados, selección explícita y guardado consciente de cambios.
Conservar cambios pendientes al filtrar o navegar; advertir antes de descartarlos.
Paginar en servidor y distinguir cero, vacío y dato desconocido.
Definir matriz general de líneas y precios; agregar talle/color sólo mediante extensión sectorial.

## Accesibilidad y adaptación

Usar texto e icono además de color para estados y errores.
Proponer contraste mínimo 4,5:1 para texto normal y foco visible en ambos temas.
Mantener controles operables por teclado y etiquetas persistentes.
Preparar revisión posterior a 1280, 768 y 390 px y altura de 720 px.
Adaptar la cinta mediante grupos desplegables sin alterar su orden lógico.

## Marca

Aplicar [diseño visual](../../../docs/DISENO-VISUAL.md).
Priorizar datos y marca de la pyme en documentos; ubicar firma Goxtech en ayuda o pie discreto.
No insertar publicidad ni acciones comerciales ajenas dentro de operaciones diarias.

## Ayuda y soporte

Mantener Ayuda → Tutoriales en cada módulo y Soporte ARG como entrada general del sistema.
Mostrar videos, manuales, versiones compatibles y estado desde el catálogo central editable.
Dirigir soporte al centro ARG administrado por el responsable, con correo, WhatsApp o tickets configurados.
Inventariar y adaptar entradas de soporte presentes en la composición instalada mediante extensiones propias.
Aplicar el [contrato de ayuda y soporte](../../../docs/AYUDA-TUTORIALES-SOPORTE.md).
Mostrar GOXTECHBOT como identidad visible del bot nativo, con avatar y textos propios discretos.
Conservar identidades técnicas del bot y ARG como marca principal del producto.
