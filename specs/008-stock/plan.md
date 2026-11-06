# Implementation Plan: Circuito Stock ARG

**Branch**: `codex-notebook/plan-001` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Consultar existencias y operar entradas, salidas, transferencias, inventarios y ajustes con trazabilidad nativa.

## Summary

Aplicar los contratos comunes y los recorridos específicos sin duplicar fuentes operativas.
Conservar interfaz simple para personal no especializado y capacidades avanzadas progresivas.

## Technical Context

**Language/Version**: Odoo 20 Community; Python 3.12; OWL/XML/SCSS cuando corresponda.
**Primary Dependencies**: `arg_pyme_base`, `arg_pyme_ui`, `arg_pyme_catalogo`, `arg_pyme_documentos`, `stock`.
**Storage**: PostgreSQL 16 y filestore nativos; configuración y secretos fuera del repositorio.
**Testing**: Controles técnicos de instalación/upgrade; escenarios de aceptación reservados para QA posterior.
**Target Platform**: Linux propio/homelab/VPS y navegador; entorno de ejemplo demo.
**Project Type**: Addon Odoo o incremento documental/de proveedor según alcance.
**Performance Goals**: Mantener paginación en servidor y evitar carga completa de catálogos en navegador.
**Constraints**: No modificar core ni exigir Enterprise; no ejecutar operaciones externas reales en ejemplos.
**Scale/Scope**: Micropymes y pymes; roles combinables, 100 líneas de documento como escenario inicial.

## Constitution Check

| Regla | Decisión de diseño |
| --- | --- |
| Gratuidad y soberanía | Código/documentación abiertos; instalación y datos bajo control de la pyme |
| Módulos propios | Extender modelos nativos y justificar modelos nuevos en data-model.md |
| Simplicidad | Datos mínimos, orden común y roles combinables |
| Identidad | ARG como producto; GOXTECHBOT como excepción suave; autoría Gonzalo Sarubilo |
| Etapas | Programar por tareas; diferir QA funcional y registrar instalación por separado |
| Integraciones | Mantener proveedores externos dentro de un único módulo Integraciones ARG |

Revisión antes y después del diseño: compatible por contrato; no acredita funcionamiento instalado.

## Project Structure

### Documentation (this feature)

spec.md, plan.md, research.md, data-model.md, contracts/operaciones.md, quickstart.md, tasks.md y checklists/requirements.md.

### Source Code (repository root)

Objetivo técnico: `addons/arg_pyme_stock`.
Rutas propuestas a crear durante implementación:

- `addons/arg_pyme_stock/models/stock_quant.py`
- `addons/arg_pyme_stock/views/stock_matrix_views.xml`
- `addons/arg_pyme_stock/models/stock_picking.py`
- `addons/arg_pyme_stock/views/stock_picking_views.xml`
- `addons/arg_pyme_stock/models/inventory_count.py`
- `addons/arg_pyme_stock/views/inventory_count_views.xml`

**Structure Decision**: Mantener una responsabilidad por addon; conservar origen y trazabilidad nativos.

## Decisiones específicas

- Conservar stock.quant y movimientos nativos como única fuente de existencias.
- El documento ARG de conteo agrupa decisiones y evidencia; sus efectos se registran en movimientos nativos.
- Activación de stock con ventas/compras previas exige previsualizar hooks sale_stock/purchase_stock y respaldo recuperable.

## Entrega y orden

Completar dependencias del catálogo antes de programar este módulo.
Aplicar las tareas por historia, en secuencia; revisar el contrato antes de cambiar una interfaz compartida.
Registrar manifest, sintaxis, carga de vistas, instalación/upgrade y arranque como controles técnicos.
Actualizar manual, tutoriales por versión y estado de entrega. Realizar QA funcional/visual posteriormente.

## Complexity Tracking

No incorporar motores, servicios ni tablas paralelas para funciones ya provistas por la fuente nativa.
Justificar toda extensión adicional mediante una decisión documentada en esta feature.

## Incremento F14 ·2026-11-06

Servicio abstracto models/traceability.py para selectores/páginas/acciones y asistente transitorio
models/lot_create.py para alta mínima. OWL estático traceability.js/xml, DateTimeInput nativo para
filtros opcionales y estado local al volver de maestros. Modelos de stock nativos son las fuentes.
No usar stock.lot.location_id editable: su inverse mueve quants; ni action_lot_open_transfers como
historia completa, porque esa acción sólo muestra entregas. Usar acción nativa de trazabilidad para
la exploración avanzada. [Contrato](contracts/trazabilidad-series-lotes.md).

Interfaz simplificada paginada; stock.move.line conserva hechos y quantity_product_uom en unidad
base. Asistente de alta no invoca ajustes ni validaciones. Concurrencia mediante fila del asistente
y lock técnico de producto existente; no sudo de negocio. Native core conserva validación de lotes.
Versión nueva de Stock por capacidad; no cambiar Catálogo ni los puentes. F15 se diseña por separado.

La extensión de stock.lot en models/lot_create.py toma el mismo lock técnico para altas y cambios
de identidad de todos los orígenes; exige permisos nativos antes del lock y conserva super().
Así la garantía no depende de que todos usen el asistente ARG. Afecta el maestro nativo consumido
por Stock y POS/otros módulos instalados; no cambiar su semántica ni exigir roles ARG globalmente.
Total y quants comparten el dominio nativo de ubicaciones, sin incluir almacenes externos al total.

Comprobación técnica de roles halló que stock.group_production_lot no estaba activo en usuarios
ARG de demo. Patch Stock1.1.1 agrega ese implied_id a Stock ARG, sin activar tracking por producto.
Campos lot_id/lot_name de stock_move y picking están condicionados por ese grupo nativo.

## Incremento F15 · configuración, propuesta y ejecución de reposición

Ampliar esta feature008, conservando FR-001–011 y F14 instalado. US6/US7 y FR-012–017
requieren compra y fabricación. [Contrato](contracts/reposicion.md). No declarar completo F15
por configurar reglas, mostrar sugerencias o habilitar una sola ruta.

### Arquitectura y composición

- Core `arg_pyme_stock/models/replenishment.py`: servicio de consulta/propuesta, extensión de
  orderpoint y orquestación atómica con permisos/contexto explícitos; no otro motor de cálculo.
- `models/replenishment_operation.py`: evidencia inmutable de ejecución y resultados/deltas;
  clave/payload únicos por compañía, sin otra tabla de existencias ni documento financiero.
- `static/src/replenishment.js/xml` y `views/replenishment_views.xml`: consulta paginada30,
  configuración simple y confirmación explícita. Modalidad, ámbito y efectos visibles; maestros
  avanzados accesibles sin perder selección/cantidades. Campos delimitados, Lucide y paleta ARG.
- Compra: ampliar el puente existente `arg_pyme_compras_stock/models/replenishment.py` para
  capacidades/proveedor y guardas/recibo sobre `purchase.order` y líneas nativos. No conector externo.
- Fabricación: puente opcional `arg_pyme_stock_mrp` con dependencias Stock ARG + `mrp`,
  `auto_install=True` sólo con ambas instaladas. `models/replenishment.py` y `mrp_production.py`
  autorizan BOM/MO/cambios de cantidad/componentes, conservando los métodos nativos y sus estados.
  No forzar MRP en una instalación genérica de Stock. Su habilitación explícita en la composición
  de demostración y el registro de ambos caminos pertenecen a la entrega F15 completa.
- Captura técnica por objeto Python privado, hashable, en contexto: reglas/actor/compañía/clave,
  decisiones aceptadas y collector. Un RPC no puede fabricar ese objeto. No crear una referencia
  comercial única para rastreo, porque altera la agrupación nativa de PO/MO.

### Seguridad, atomicidad y efectos

Abrir una acción propia sobre orderpoints existentes: `_get_orderpoint_action()` crea/borra datos.
ARG crea reglas manuales explícitas; no convierte las existentes ni cambia el scheduler. Consulta
sin `action_replenish`, sin nuevo cursor ni commits. Limpiar contexto heredado y usar la compañía actual.
Mantener `qty_on_hand`, `qty_forecast`, `_quantity_in_progress()` y `_get_qty_to_order()` nativos,
con horizonte, unidades, proveedor/BOM y rutas efectivas. No restar físico al máximo como motor nuevo.

Confirmar como responsable ARG con permisos nativos de regla/destinos. Bloquear reglas, productos
implicados y maestros necesarios en orden estable con UPDATE efectivo compatible con RR; releer.
Autorizar y buscar el recibo existente ANTES de comparar previsión actual; misma clave/payload
retorna el resultado, distinta carga falla. Para una operación nueva comparar huella de propuesta
incluyendo configuración/cantidades/ruta/abastecimiento en curso, luego fijar cantidades elegidas y
llamar `_procure_orderpoint_confirm(use_new_cursor=False, company_id=company, raise_user_error=True)`
con `manual_replenishment=True`. Escribir `qty_to_order_manual` positiva directamente y verificar `qty_to_order` con precisión nativa;
no usar su inverse, que borra manual en trigger auto. La propuesta muestra el manual previo y su
consumo: al completar la operación se limpia el override manual usado, sin cambiar trigger.
No usar `action_replenish` para ejecutar: reemplaza cantidad por manual/to_max y limpia reglas.

El core nativo usa sudo internamente: no prometer que llamar super basta para aplicar permisos.
Guardas bajo el objeto privado en create/write de destinos revalidan como actor original antes de
mutaciones y antes de devolver resultados. El collector recoge referencias/deltas autorizados en
la misma transacción y exige postcondiciones por rama/ruta, no sólo retorno sin excepción o count.
Abarcar ampliaciones de PO/MO, lotes de fabricación y kits phantom/componentes; no sumar unidades
incompatibles ni prometer siempre borradores. Rutas encadenadas deben explicar también planificación
intermedia/reservas nativas. Fallo revierte toda la operación, sin anunciar un éxito parcial.

### Orden y controles

Contrato/revisión → reglas/consulta → propuesta/huella → orquestación/recibo → guardas y compra
→ puente MRP y efectos → interfaz/manuales → controles estáticos/composición → respaldo consistente
y snapshot soportado del CT definitivo → instalación/verificación en ese mismo CT → fuente/documentación main. No cerrar parent016T009
hasta completar F14/F15. Controles técnicos y QA/aceptación permanecen separados.

La [política vigente de CT](../../docs/tecnica/POLITICA-CT.md) sustituye el gate anterior de un CT
aislado para los pasos futuros. No crear CT de QA, clonación ni restauración, ni reutilizar otros
como staging. Recuperar sólo el mismo CT cuando corresponda; verificar respaldo sin sobrescribir
datos activos para un ensayo. No reescribir resultados históricos de las entregas ya realizadas.

### Constitution Check después del diseño F15

Fuente nativa única, fabricación opcional, sin nuevos servicios externos ni dependencia comercial.
La evidencia es técnica e inmutable; los hechos de compra/fabricación/stock quedan en sus documentos.
La propuesta no tiene efectos por consulta; confirmar conserva trazabilidad y carga mínima. Compatible
con los principios por diseño; no acredita implementación, instalación o QA.


F15: `_post_process_scheduler()` MRP confirma también MO borrador previas de las reglas seleccionadas
si su tipo habilita auto_confirm_production. Incluir ese conjunto en propuesta/huella/autorización y
capturar cambios de estado; hook `mrp.production.action_confirm` antes de super. El wizard nativo
`change.production.qty.change_prod_qty` modifica movimientos/componentes/subproductos, órdenes de
trabajo y planificación/reservas, y dispara `_trigger_scheduler` de insumos. La confirmación MRP
también dispara abastecimiento hijo. No activar el scheduler global ni cambiar su configuración;
conservar estas llamadas encadenadas dentro de la misma operación ARG y su collector. El override
protegido de `_procure_orderpoint_confirm` exige `use_new_cursor=False` y `raise_user_error=True`
incluso si el disparador hijo nativo solicita False; validar actor/compañía, alcance revisado y
postcondiciones de cada rama. Configuración ajena al grafo revisado exige nueva propuesta y revierte.
La propuesta distingue cantidades raíz aceptadas y cantidades derivadas por motor nativo; no
promete una cifra exacta para cada consecuencia dependiente de la ejecución. Explica estados,
capacidad de ampliar/confirmar previos y posibles reservas/abastecimientos de insumos.

### Frontera concurrente de fuentes nativas

El lock del recibo o de la regla sólo serializa el reintento, no todo el abastecimiento. Inventariar
los mutadores reales de la composición que cambian físico/previsión/pipeline o selección de ruta,
proveedor/BOM: movimientos y fechas/estados/unidades, PO/líneas/estados, MO/cantidad/estado y BOM,
proveedores/unidades/rutas de maestros. Reutilizar el UPDATE efectivo de producto existente y
bloquear plantillas/maestros al revisar. Los hooks nativos de esos mutadores participan también
sin collector, conservando permisos nativos y super, para que las altas automáticas y operaciones
ajenas al flujo ARG no esquiven la serialización. No exigir rol ARG a todos los consumidores nativos.
El collector añade autorización/alcance/evidencia sólo al flujo ARG; no convertir un flag RPC en permiso.
Registrar en research.md la matriz concreta de mutadores/hook/campos antes de cerrar T027/T029;
no atribuir cobertura concurrente global a un lock de wizard o a una huella leída sin esa frontera.

La evidencia persistida no tiene ACL de read/export raw para usuarios de gestión. El servicio usa
lectura elevada SÓLO de evidencia técnica tras autorizar rol/compañía; antes de responder o hacer
replay valida sin sudo todas sus dimensiones y referencias nativas como solicitante ACTUAL. El actor
histórico permanece para atribuir ejecución y no presta permisos al lector. Un acceso perdido bloquea
la representación completa con mensaje genérico, también al actor original, sin reejecutar la
operación. No exponer JSON crudo por read/search_read/web_read/export/read_group o campos relacionados.
No usar sudo para negocio oculto. Cubrir esta frontera explícitamente en T026/T030 y QA posterior.
