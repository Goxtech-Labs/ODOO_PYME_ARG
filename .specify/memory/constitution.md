<!-- Sync Impact Report
Version: 1.3.0 -> 1.3.1.
Changed: owner adopted AGPL-3.0-only for original code and CC-BY-SA-4.0 for original documentation/artwork.
Preserved: third-party licenses, deferred functional/visual QA, ARG identity and scope.
Templates unchanged; NOTICE.md and license files record the decision.
-->
# ODOO PYMES ARG Constitution

## Core Principles

### I. Gratuidad y comunidad
Compartir conocimiento técnico y de gestión con la mayor cantidad posible de pymes.
Mantener documentación, tutoriales y ejemplos del proyecto abiertos y accesibles sin pago obligatorio.
Incorporar experiencias y necesidades de usuarios para aprender y mejorar comunitariamente.
Publicar gratuitamente las funciones de gestión del proyecto y su código fuente.
Evitar límites comerciales propios por usuario, documento o módulo.
Mantener instalación autónoma y participación comunitaria sin contratar servicios Goxtech.
Identificar por separado costos opcionales de alojamiento, asistencia y proveedores externos.

### II. Soberanía de datos
Permitir elegir homelab, servidor propio, VPS u otra infraestructura compatible.
Permitir elegir infraestructura, administrador y proveedor de soporte.
Documentar exportación, respaldo completo y restauración en otra instalación.
Incluir base de datos, adjuntos, configuración reproducible y versiones en la recuperación.
Evitar cuentas Goxtech, telemetría o servicios externos obligatorios para la gestión local.
Solicitar activación explícita de cada integración y explicar sus datos compartidos.

### III. Núcleo genérico y módulos propios
Desarrollar desde cero los addons propios, módulo por módulo.
Usar Odoo Community como plataforma y conservar sus mecanismos nativos compatibles.
Separar núcleo, presentación, gestión, especializaciones e integraciones.
Evitar copiar addons de otros clientes o sus reglas comerciales.
Declarar dependencias, licencias, versiones y efectos de instalación de cada módulo.

### IV. Documentos y áreas claramente separados
Organizar Ventas, Compras, Stock y Administración como áreas diferenciadas.
Dar identidad, listado, acciones y estados explícitos a cada tipo documental.
Modelar Presupuesto ARG y Pedido de cliente ARG como documentos distintos.
Generar pedido desde presupuesto confirmado, con código propio y relación explícita al origen.
Conservar presupuesto e historia; no convertirlo ni reemplazarlo por el pedido.
Vincular documentos por origen, destino, cantidades e importes pendientes.
Separar efectos comerciales, físicos, contables, financieros y fiscales.
Conservar los mecanismos contables y de existencias nativos como fuente de verdad.
Identificar documentos mediante código corto y secuencia propia por compañía y tipo.
Separar identificación interna y numeración fiscal.
Definir hechos, granularidad y dimensiones explícitas para cada informe.

### V. Carga mínima y orden estable
Mantener tercero, datos generales, detalle, totales y acciones en ese orden.
Solicitar únicamente datos indispensables para la operación y su estado actual.
Completar valores conocidos desde compañía, tercero, producto y documento de origen.
Conservar correcciones explícitas y mostrar campos avanzados progresivamente.
Evitar solicitar nuevamente datos disponibles o trasladables entre documentos.

### VI. Identidad argentina y consistencia visual
Visibilizar a Gonzalo Sarubilo como impulsor y autor de sus aportes personales.
Comunicar su experiencia declarada en tecnología y gestión de pymes sin agregar credenciales no aportadas.
Mantener consultoría y servicios profesionales como actividad opcional secundaria al propósito comunitario.
Usar ARG como identidad de interfaces, módulos, objetos y documentación de este proyecto.
Usar GOXTECHBOT como excepción explícita de branding suave para la identidad visible de OdooBot.
Aplicar nombres técnicos nuevos con prefijo `arg_pyme_` y nombres visibles terminados en ARG.
Limitar esta convención a Odoo Pymes ARG; no renombrar otros productos ni módulos instalados.
Usar celeste, blanco y un acento solar discreto.
Mantener branding Goxtech secundario frente a la identidad de cada pyme.
Unificar botones, iconos, matrices, filtros, estados y mensajes entre módulos.
Mantener Guardar verde, Descartar rojo y significado acompañado por texto.
Conservar contraste, navegación por teclado y adaptación a pantallas pequeñas.

### VII. Personalización por extensión
Documentar personalización para personas y agentes de IA mediante especificaciones, contratos y ejemplos públicos.
Mantener elección de herramientas y proveedores de IA; evitar suscripciones de IA obligatorias para la gestión.
Conservar Gestión ARG simplificada como entrada principal y Odoo avanzado según permisos.
Agregar módulos por rubro sin condicionales por nombre de cliente.
Centralizar ajustes externos en Integraciones ARG y conservar operaciones en sus áreas.
Agrupar todos los servicios externos dentro de un único addon de Integraciones ARG.
Organizar adaptadores internos por servicio; no crear un addon independiente por conector.
Mantener una única configuración efectiva de cada conector por compañía y ambiente.
Documentar contratos y compatibilidad antes de incorporar extensiones.

### VIII. Documentación y entregas trazables
Especificar cada módulo antes de programarlo mediante Spec Kit.
Entregar guía funcional, documentación técnica, ejemplos y cambios con cada módulo.
Usar YouTube como canal de aprendizaje y alcance, enlazando guías públicas versionadas.
Vincular tutoriales y manuales desde cada módulo mediante un catálogo editable y versionado.
Revisar contenido afectado por cambios y distinguir vigente, pendiente, por revisar y reemplazado.
Ofrecer soporte general ARG con canales administrados por el responsable del proyecto.
Dirigir accesos de asistencia al mismo centro, con correo, WhatsApp o tickets configurables.
Separar desarrollado, instalado, revisado funcionalmente y aceptado por el usuario.
Conservar datos de demostración identificados y ajenos a operaciones reales.

## Alcance y restricciones

Aplicar el propósito de conocimiento compartido y aprendizaje comunitario documentado en `docs/MANIFIESTO.md`.

Diseñar un producto comunitario argentino genérico y modular para pymes.
Entregar primero Ventas, Compras, Stock, Administración e Informes.
Reservar integraciones y especializaciones sectoriales para etapas posteriores.
Tomar FactuSOL como referencia funcional de separación y simplicidad documental.
Evaluar patrones y soluciones de otros proyectos Odoo Goxtech como referencias técnicas.
Preservar identidad y composición propias; revisar licencias antes de incorporar soluciones ajenas.
Crear identidad, assets y código propios; conservar atribuciones y licencias de terceros.
Proponer la última versión estable Community y verificar compatibilidad por módulo.
Evitar prometer cobertura fiscal integral, servicios gratuitos externos o personalización sin límites técnicos.
Documentar restricciones reales y caminos de extensión.

## Development Workflow

Aplicar constitución → especificación → aclaraciones necesarias → plan → tareas → implementación.
Generar una especificación independiente por módulo o integración, conservando contratos compartidos.
Completar controles técnicos de instalación y arranque durante el desarrollo autorizado.
Registrar QA funcional y visual como fase posterior, siguiendo la preferencia vigente del usuario.
Preparar escenarios de aceptación durante la especificación, sin ejecutarlos anticipadamente como QA.
Registrar publicación, despliegue y activación de integraciones como estados independientes.

## Governance

Aplicar las decisiones explícitas del usuario antes de supuestos documentales.
Registrar propuestas pendientes sin presentarlas como aprobadas.
Modificar principios mediante decisiones fechadas y análisis de módulos afectados.
Versionar cambios incompatibles como mayores; agregar principios como menores; corregir redacción como parches.
Revisar cumplimiento en cada especificación y entrega.

**Version**: 1.3.1 | **Ratified**: 2026-11-01 | **Last Amended**: 2026-11-01

Los documentos muestran ejes de cumplimiento independientes con pendiente/parcial/completo y trazabilidad de cantidades/importes; no equiparar cierre de faltante con cumplimiento.

Licencias adoptadas el 1 de noviembre de 2026: AGPL-3.0 para código original (SPDX AGPL-3.0-only), CC BY-SA 4.0 para documentación/recursos originales. Conservar excepciones y avisos de terceros según NOTICE.md.
