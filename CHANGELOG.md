# Cambios

## 0.1.6-dev — 2026-11-06

- Valores1.2, Reparaciones1.2, Administración1.1.4 y Compras1.0.6 promovidos a demo.
- 103 módulos/14 ARG;285 fuentes comprobadas, POS nativo y configuración existente conservados.
- Respaldo fresco restaurado en copia aislada; instalación/upgrade y arranque técnicos comprobados.
- [Entrega y límites](docs/entregas/EXPANSION-PROMOCION.md). QA funcional/visual, PDF y aceptación pendientes.

## Instalación aislada de la expansión — 2026-11-06

- Valores1.2/Administración1.1.4, Reparaciones1.2 y Compras1.0.6 instalados con controles técnicos.
- REP borrador, cliente, repuesto y servicio ficticios cargados sin efectos operativos.
- [Evidencia y límites](docs/entregas/EXPANSION-INSTALACION-AISLADA.md). Demo compartida sin promoción; QA pendiente.

## Carga documental de Compras — 2026-11-06

- Compras20.0.1.0.6 en fuente: fecha del proveedor antes de tercero/referencia, condiciones contables
  diferenciadas y todos los campos nativos conservados. Sin instalación ni QA acreditadas.
- [Estado de la entrega](docs/entregas/016-compras-carga-basica.md).

## Desarrollo de especializaciones — 2026-11-05

- Reparaciones20.0.1.2.0 en fuente: corrección trazable de datos, nuevas visitas con REP independiente
  y reporte de correcciones/hechos. No instalado; [estado](docs/entregas/018-correcciones-visitas.md).

- Reparaciones20.0.1.1.0 en fuente: PRE/PED/autorización, PTM de servicios, repuestos nativos,
  listo/retomar/entrega, correcciones de trabajo y hechos por origen. Sin instalación/QA acreditadas.
- [Entrega de trabajo autorizado](docs/entregas/018-trabajo-autorizado.md).

- Reparaciones ARG20.0.1.0.0: primer código REP de recepción, diagnóstico y devolución sin reparar;
  equipo ajeno sin existencias propias, hechos conservados, rol e impresión de custodia.
- Manual, contrato y catálogo tutorial preparados. Instalación y QA pendientes; presupuesto,
  autorización, intervención, repuestos, horas y facturación siguen en desarrollo.
- [Estado de la entrega](docs/entregas/018-reparaciones.md).

## 0.1.5-dev — 2026-11-05

- Plan de expansión completo:22 capacidades, specs016–024,27 tareas coordinadoras y115 por módulo; conteos de avance no aditivos.
- Principio argentino de carga práctica: hoy propuesto, tercero, documento y conceptos/artículos.
- Primer incremento: fecha primero en formularios propios y default de fecha en facturas/notas.
- REC multimedio y cartera argentina especificados; módulos avanzados pendientes de implementar.
- [Controles técnicos y límites](docs/entregas/CARGA-BASICA-ARG.md).

## 0.1.4-dev — 2026-11-02

- Azul ARG en variables nativas de marca, paletas de calendario, enlaces, selección y foco.
- Favicon ARG predeterminado respetando el de empresa; color azul del navegador.
- Contraste corregido en buscador/calendario y botones neutros del tema oscuro.
- [Revisión visual y límites](docs/entregas/TEMA-ARG.md).

## 0.1.3-dev — 2026-11-02

- Cinta por circuitos, Lucide local, portada/acceso industrial argentino y campos delimitados.
- Tema/densidad en Mis preferencias; mejoras de contraste y pantalla estrecha.
- Compatibilidad Odoo20: precisión de cantidades y valores QWeb impresos.
- Recorrido aislado PRE→PED→REM parcial→FAC interna parcial verificado; aceptación pendiente.
- [Pruebas y límites](docs/entregas/INTERFAZ-Y-VENTAS.md).

## 0.1.2-dev

- Web y canal general editables desde Gestión ARG; enlaces compartidos en Ayuda, Soporte y Acerca de.
- Contactos oficiales Goxtech elegidos por el titular, con WhatsApp principal y correo alternativo.
- Canal general separado de los tutoriales específicos aún pendientes.
- Registro de publicación actualizado tras integrar el núcleo a main.


## 0.1.1-dev — 2026-11-01

Correcciones de cierre contractual: registro/migración AJU, pendientes físicos antes de validar,
orden común de ejes, límites de atribución de facturación/dinero, precisión de informes y SVG
con texto/Acerca de ARG. [Detalle y estado técnico](docs/entregas/CIERRE-DE-CONTRATOS.md).

## 0.1.0-dev — 2026-11-01

Primera composición de Odoo Pymes ARG sobre Odoo 20 Community. Doce addons originales: Base,
Interfaz, Terceros, Catálogo, Documentos, Ventas, Compras, Stock, Administración, Informes y dos
puentes físicos. Cinco circuitos con datos mínimos, documentos identificados, pendientes por eje,
PRE separado de PED, fuentes nativas de stock/contabilidad y exportaciones de informes CSV/PDF.

Portada documental, identidad celeste/blanco, GOXTECHBOT, ayuda versionada y soporte configurable.
Licencias adoptadas: AGPL-3.0 para código y CC BY-SA 4.0 para documentación/recursos originales.
Guías abiertas de instalación, operación, recuperación, exportación y personalización; Spec Kit
por módulo. Catálogo agrega acceso al mismo maestro desde Ventas y Compras, versión20.0.1.0.5.

Entrega de desarrollo e instalación técnica con ejemplos. QA funcional/visual, aceptación y
publicación remota se registran por separado. Integraciones, ARCA y rubros son etapas posteriores.
Ver [release](docs/entregas/RELEASE.md) para composición y límites.
