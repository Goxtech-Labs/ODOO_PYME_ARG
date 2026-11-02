# Implementation Plan: ODOO PYMES ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Producto comunitario genérico y modular para pymes argentinas.

## Summary

Construir gestión documental básica mediante addons propios sobre Odoo Community.
Entregar primero Ventas, Compras, Stock, Administración e Informes.
Mantener identidad argentina, carga mínima y orden visual/lógico constante.
Agregar conectores y rubros después de estabilizar los circuitos comunes.
Agrupar todos los servicios externos en un único addon `arg_pyme_integraciones`, con adaptadores internos.
Conservar instalación autónoma, documentación pública y acceso avanzado por permisos.
Aplicar identidad ARG sólo a este proyecto y ampliar adopción mediante YouTube y guías versionadas.
Incluir tutoriales por módulo, catálogo editable, soporte general administrado y branding suave GOXTECHBOT.
Documentar alojamiento en infraestructura elegida y personalización por personas o agentes de IA.
Conservar acceso abierto a conocimiento técnico y de gestión como propósito comunitario.
Visibilizar autoría de Gonzalo Sarubilo y su experiencia declarada, con servicios profesionales secundarios y opcionales.

## Technical Context

**Language/Version**: Python 3.12 instalado en demo; JavaScript/OWL, XML y SCSS según Odoo 20.0.
**Primary Dependencies**: Odoo 20 Community instalado en demo; módulos nativos `base`, `web`, `contacts`,
`sale_management`, `purchase`, `stock`, `account` y puentes según cada capacidad.
**Storage**: PostgreSQL 16 instalado en demo; filestore y configuración recuperable fuera de Git.
**Testing**: Controles técnicos durante implementación; escenarios funcionales y visuales para QA posterior.
**Target Platform**: Linux propio y navegador; escritorio primero, adaptación móvil.
**Project Type**: Distribución de addons y documentación pública estática.
**Performance Goals**: Proponer listados comunes visibles en menos de dos segundos.
Medir después con 10 usuarios concurrentes, 10.000 productos y 100.000 líneas sintéticas.
**Constraints**: Sin Enterprise obligatorio, servicios Goxtech obligatorios ni modificaciones directas al core.
Sin conectores, rubros, emisión fiscal real ni migración real en la entrega inicial.
**Scale/Scope**: Una pyme por instalación como perfil inicial; preservar aislamiento multiempresa nativo.
Usar documentos de 100 líneas como referencia; no garantizar capacidad antes de medir.

## Constitution Check

| Principio | Diseño previo | Diseño posterior |
| --- | --- | --- |
| Gratuidad | Addons abiertos y sin cuotas propias | Licencias adoptadas AGPL-3.0-only y CC-BY-SA-4.0; NOTICE conserva excepciones |
| Soberanía | Instalación y recuperación autónomas | Respaldo de demo restaurado aisladamente; escenarios con documentos para QA posterior |
| Desarrollo nuevo modular | Addons nuevos sobre plataforma nativa | Catálogo por responsabilidad |
| Separación documental | Tipos y efectos distintos | Contratos con trazabilidad y granularidad |
| Carga mínima | Valores predeterminados y orden estable | Criterios verificables de UX |
| Identidad argentina | Tokens y branding discreto | Brandkit propuesto; QA visual posterior |
| Extensibilidad | Rubros y puentes opcionales | Integraciones posteriores al núcleo |
| Documentación | Spec Kit por entrega | Núcleo implementado; composición/entregas identificadas |

No confundir cumplimiento documental con validación funcional.
Elegir licencia antes de publicar código; registrar revisión/composición en cada entrega; ver docs/tecnica/ENTORNO-DEMO.md.

## Project Structure

### Documentation (this feature)

```text
.specify/memory/constitution.md
specs/001-pyme-argentina/
  spec.md
  plan.md
  research.md
  data-model.md
  contracts/documentos.md
  contracts/interfaz.md
  contracts/soberania.md
  quickstart.md
  tasks.md
  checklists/requirements.md
docs/
  PLAN-MAESTRO.md
  DISENO-VISUAL.md
  REFERENCIAS-FACTUSOL.md
  CATALOGO-MODULOS.md
  ALCANCE-YOUTUBE.md
  AYUDA-TUTORIALES-SOPORTE.md
  GONZALO-SARUBILO.md
  plantillas/modulo.md
```

### Source Code (repository root)

Estructura objetivo; crear código solamente al comenzar cada módulo.

```text
addons/arg_pyme_base/
addons/arg_pyme_ui/
addons/arg_pyme_terceros/
addons/arg_pyme_catalogo/
addons/arg_pyme_ventas/
addons/arg_pyme_compras/
addons/arg_pyme_stock/
addons/arg_pyme_administracion/
addons/arg_pyme_informes/
addons/arg_pyme_documentos/
composition/versions.lock.json
docs/usuario/
docs/tecnica/
docs/comunidad/
docs/web/
```

**Structure Decision**: Un repositorio de producto con módulos por responsabilidad.
Usar puentes pequeños para conectar capacidades opcionales y evitar dependencias circulares.
Permitir Ventas sin Stock para empresas de servicios.
Extender modelos nativos; evitar libros contables o inventarios paralelos.
Crear modelo documental propio de presupuesto ARG; generar pedido `sale.order` distinto desde presupuesto confirmado.
Conservar la funcionalidad nativa del pedido y sus movimientos, sin usar un mismo registro para presupuesto y pedido ARG.

## Fases y entregas

1. Fundamentos: identidad, lenguaje documental, contratos, portada y especificaciones.
2. Base: navegación, roles, compañías, preferencias y componentes comunes.
3. Maestros: terceros, productos/servicios, listas y valores predeterminados.
4. Ventas: presupuestos, pedidos, remitos, facturas y devoluciones mediante puentes necesarios.
5. Compras: pedidos a proveedor, entradas, facturas recibidas y devoluciones.
6. Stock: movimientos, depósitos, transferencias e inventarios.
7. Administración: recibos, cobros, pagos, caja, bancos e imputación.
8. Informes: hechos, dimensiones, consultas conciliables y documentos imprimibles.
9. Consolidación: documentación, instalación reproducible, respaldo y QA posterior.
10. Ampliaciones: conectores y rubros mediante especificaciones independientes.

Preparar tutoriales de YouTube por circuito después de revisar cada recorrido mostrado.
Conservar videos vinculados a versiones y manuales; definir canal antes de publicar.
Preparar ayuda por módulo y soporte general en Base ARG y presentación ARG desde sus especificaciones.
Mantener las futuras conexiones API de soporte o YouTube dentro de Integraciones ARG.
Inventariar acciones de asistencia y superficies del bot en la composición instalada antes de adaptarlas.

Mantener proveedores externos dentro de Integraciones ARG; separar módulos especializados de gestión según necesidad.

Desarrollar módulo por módulo; no asignar fechas sin capacidad y alcance detallados.
Separar venta sin stock de entrega física: integrar ésta después de entregar Stock.
Definir cada circuito antes de programar sus dependencias y puntos de conexión.

## Flujo por módulo

Crear spec propia con alcance, datos mínimos, documentos, hechos, dimensiones y ejemplos.
Generar plan, contratos y tareas con rutas concretas.
Desarrollar código nuevo conservando invariantes nativas.
Completar controles técnicos de instalación y registrar versión.
Realizar QA funcional y visual posteriormente con el usuario.
Entregar manual funcional, guía técnica y cambios junto con cada módulo.
Separar desarrollado, instalado, revisado, aceptado y publicado.

## Riesgos y decisiones pendientes

- Licencia resuelta por el titular; conservar textos y avisos en cada paquete.
- Verificar composición, fuente/paquete/runtime y respaldo en cada entrega.
- Conservar presupuesto propio, revisiones aprobadas y pedido separado sin duplicar efectos de contabilidad o stock.
- Mantener factura interna separada de autorización fiscal hasta desarrollar el conector.
- Paginar matrices grandes y conservar cambios pendientes ante filtros.
- Revisar derechos antes de redistribuir referencias FactuSOL; crear assets propios.
- Mantener nombre de trabajo ODOO PYMES ARG hasta definir identidad nominal definitiva.

## Complexity Tracking

Evitar microservicios, almacén analítico separado, diseñador gráfico completo e infraestructura distribuida.
Agregar modelos sólo ante necesidades demostradas; no registrar excepciones a la constitución.
