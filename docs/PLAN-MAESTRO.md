# Plan maestro ODOO PYMES ARG

Crear una gestión gratuita y comunitaria para pymes argentinas sobre Odoo Community.
Combinar separación documental inspirada en FactuSOL, extensibilidad Odoo y experiencia ARG simplificada.
Mantener soberanía de datos, documentación pública y desarrollo propio módulo por módulo.
Compartir experiencia técnica y de gestión con todas las pymes posibles, aprendiendo de nuevos usuarios.
Conservar el [manifiesto](MANIFIESTO.md) como fundamento del producto y sus decisiones.
Visibilizar a Gonzalo Sarubilo como impulsor, con más de 20 años de experiencia en tecnología para pymes.
Presentar su aporte en gestión financiera, dirección, redes, software/desarrollo, gestión, marketing y ventas.
Mantener consultoría y servicios profesionales como actividad opcional secundaria al propósito comunitario.
Aplicar el [perfil y jerarquía de autoría](GONZALO-SARUBILO.md) en portada, documentación y YouTube.

## Decisiones confirmadas el 1 de noviembre de 2026

- Construir un producto genérico y modular; agregar rubros e integraciones posteriormente.
- Organizar cinco circuitos: Ventas, Compras, Stock, Administración e Informes.
- Desarrollar addons propios desde cero, conservando Odoo Community como plataforma.
- Mantener Gestión ARG simplificada como entrada principal y acceso avanzado según permisos.
- Pedir la mínima información necesaria y conservar siempre el mismo orden visual y lógico.
- Separar tipos documentales, sus hechos, dimensiones, estados y efectos.
- Usar códigos cortos y numeración correlativa por tipo documental.
- Crear identidad argentina celeste/blanca y branding Goxtech discreto.
- Presentar el repositorio como portada del proyecto y generar documentación con Spec Kit.
- Agrupar todos los servicios externos en un único módulo de Integraciones ARG.
- Agregar módulos especializados o personalizados separados según corresponda a cada pyme.
- Usar ARG como identidad propia y nomenclatura exclusiva de este proyecto.
- Ampliar alcance y aprendizaje mediante YouTube, vinculado a documentación pública versionada.
- Vincular tutoriales desde cada módulo y mantenerlos mediante un catálogo editable según versiones.
- Ofrecer soporte general administrado por el responsable, con correo, WhatsApp o tickets configurables.
- Presentar OdooBot como GOXTECHBOT, excepción explícita de branding suave.

## Promesa del producto

Ofrecer software del proyecto gratuito, instalable y modificable, sin cuotas propias por usuario o documento.
Permitir elegir infraestructura, conservar respaldos completos y cambiar de proveedor.
Explicar por separado costos opcionales de alojamiento, servicios externos y asistencia.
Publicar guías de usuario, instalación, administración y desarrollo, además de ejemplos y cambios.
Mantener acceso abierto al conocimiento aportado y elegir homelab, servidor propio o VPS para alojar la gestión.
Documentar personalización para personas y agentes de IA sin convertir la IA en dependencia obligatoria.

## Cinco circuitos iniciales

| Circuito | Documentos/objetos principales | Hecho observable |
| --- | --- | --- |
| Ventas | Presupuesto, pedido, remito, factura, notas y devolución | Propuesta, demanda, entrega y venta facturada separados |
| Compras | Pedido proveedor, entrada, factura recibida y devolución | Compra solicitada, recibida y facturada separadas |
| Stock | Entrada, salida, transferencia, inventario y ajuste | Cantidad física por producto y ubicación |
| Administración | Recibo, cobro, orden de pago, pago, caja y banco | Flujo de dinero, deuda e imputación separados |
| Informes | Consulta, agrupación, listado e impresión | Medida conciliable con documentos de origen |

Mantener configuración y ayuda como soporte transversal.
Conservar atajos entre áreas sin duplicar documentos ni sus efectos.
Mostrar moneda, fecha, compañía y estado de cada medida.
Separar factura interna de comprobante autorizado fiscalmente hasta incorporar ARCA.

## Experiencia cotidiana

Usar navegación superior por áreas y cinta de acciones contextual.
Abrir listados con búsqueda, filtros estables y selección de columnas.
Mantener tercero → datos generales → detalle → totales → acciones en documentos.
Completar valores conocidos y mostrar campos avanzados sólo cuando correspondan.
Conservar contexto al volver de fichas, imprimir o generar un derivado.
Usar matrices editables donde reduzcan carga; mantener teclado, filtros y cambios pendientes.

## Orden de construcción

1. Definir contratos, identidad, componentes y catálogo mediante esta planificación.
2. Especificar Base ARG y presentación común como primeros módulos independientes.
3. Incorporar terceros y catálogo de productos/servicios.
4. Desarrollar Ventas y Compras con sus documentos y políticas.
5. Entregar Stock y conectar recepciones/entregas mediante puentes explícitos.
6. Desarrollar Administración y conectar cobros/pagos a documentos existentes.
7. Construir Informes desde hechos y dimensiones definidos.
8. Completar documentación, recuperación e instalación reproducible.
9. Revisar funcionalmente cada entrega con el usuario después de su instalación autorizada.
10. Agregar integraciones y rubros mediante nuevas especificaciones independientes.

Mantener todos los servicios externos dentro del único addon `arg_pyme_integraciones`.
Documentar cada servicio como incremento interno, sin crear módulos separados por proveedor.

## Identidad y alcance

Usar nombres visibles terminados en ARG y nombres técnicos originales `arg_pyme_*`.
Mantener esta convención dentro del proyecto; conservar otros desarrollos Odoo Goxtech sin renombrarlos.
Tomar sus patrones y soluciones como referencias técnicas, revisando compatibilidad y licencias.
Construir identidad argentina propia con presencia discreta de GoxtechLabs como impulsor.
Usar YouTube como canal de difusión y enseñanza, con recorridos reproducibles por circuito.
Enlazar versión, repositorio, guía y ejemplos en cada tutorial.
Consultar [identidad ARG y YouTube](ALCANCE-YOUTUBE.md) para la serie propuesta.
Consultar [ayuda, tutoriales y soporte](AYUDA-TUTORIALES-SOPORTE.md) para acceso y mantenimiento.
Incluir tutoriales versionados por módulo y un acceso general Soporte ARG administrado centralmente.
Revisar videos afectados cuando cambie el producto; permitir actualizar enlaces sin reinstalar módulos.
Aplicar GOXTECHBOT a la identidad visible vigente del bot nativo, con presencia visual discreta.

Mantener el alcance inicial básico. Diferir CRM completo, fabricación, nómina, diseñador visual avanzado,
inteligencia artificial, automatizaciones externas y tienda web hasta justificar módulos propios.
Conservar código, documentación, instalación, QA y aceptación como hitos diferentes.

## Comunidad y mantenimiento

Preparar portada visual, guía de contribución, código de conducta y reporte privado de vulnerabilidades.
Mantener decisiones técnicas, versiones compatibles y roadmap públicos cuando se publique el proyecto.
Aceptar aportes con necesidad reproducible, alcance definido, licencia compatible y documentación.
Mantener ejemplos sin datos reales de clientes y reconocer contribuciones de Odoo y terceros.
Permitir servicios profesionales opcionales sin reservar funciones básicas detrás de un pago.

## Decisiones técnicas propuestas

Odoo 20 Community instalado en entorno demo; composición fijada en composition/versions.lock.json.
Licencias adoptadas: AGPL-3.0 para addons originales y CC BY-SA 4.0 para documentación/recursos; ver NOTICE.md.
Usar modelos nativos de contabilidad y stock con extensiones propias; evitar duplicar sus libros.
Ver [investigación y fuentes](../specs/001-pyme-argentina/research.md).

## Próxima entrega

Portada/documentación 011 completada. Entrega global del núcleo instalado en docs/entregas/RELEASE.md.
La publicación remota se sigue en el [PR #1](https://github.com/Goxtech-Labs/ODOO_PYME_ARG/pull/1).
La revisión funcional/visual y la aceptación siguen pendientes como hitos distintos.
Conservar composición, evidencias técnicas y QA posterior como estados separados.
Usar la [plantilla de módulo](plantillas/modulo.md) y conservar la constitución como contrato común.
No iniciar todos los módulos simultáneamente.
