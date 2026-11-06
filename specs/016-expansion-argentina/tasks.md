# Tasks: Expansión argentina coordinada

Tareas padre: referencia de entregas; no sumarlas como implementación adicional a las tareas017–024.
Estado inicial: plan de trabajo. Revisiones funcionales posteriores están en quickstart.md.


## E0

- [x] T001 Releer101 módulos, versiones/procedencia y hashes de runtime sin sobrescribir lock histórico; registrar en docs/entregas/EXPANSION-COMPOSICION.md
- [x] T002 Adoptar principio fecha/destinatario/documento/conceptos en .specify/memory/constitution.md y contratos, conservando fechas elegidas
- [x] T003 Cerrar contrato REC/OPA y cartera en specs/017-cartera-valores/contracts/cartera-argentina.md con deuda/liquidez/exposición separados

## US1

- [x] T004 [US1] Aplicar fecha y orden básico en formularios propios de addons/arg_pyme_ventas/views/quotation_views.xml y sale_order_views.xml, sin quitar campos
- [x] T005 [US1] Completar fechas por contexto sólo cuando falten en addons/arg_pyme_ventas/models/account_move.py y addons/arg_pyme_compras/models/account_move.py
- [x] T006 [US1] Aplicar patrón de carga en addons/arg_pyme_compras/views/purchase_order_views.xml y account_move_views.xml
- [x] T007 [US1] Aplicar patrón de carga en addons/arg_pyme_administracion/views/treasury_document_views.xml y addons/arg_pyme_stock/views/stock_picking_views.xml
- [x] T008 [US1] Completar matriz de variantes F13 y precios/condiciones F19 sin doble maestro en addons/arg_pyme_catalogo/models/pricelist_matrix.py y views/product_template_views.xml
- [ ] T009 [US1] Completar trazabilidad/reposición F14/F15 usando stock.lot y orderpoints nativos en addons/arg_pyme_stock/views/stock_matrix_views.xml y models/replenishment.py
- [ ] T010 [US1] Completar etiquetas F17 y tarifas/importación F22 con vista previa y diferencias en addons/arg_pyme_catalogo/wizard/import_pricelist.py y report/labels.xml
- [ ] T011 [US1] Completar riesgo F16 con fuentes monetarias nativas en addons/arg_pyme_terceros/models/res_partner.py y addons/arg_pyme_ventas/models/credit_risk.py
- [ ] T012 [US1] Completar facturación agrupada F20 con propuesta y claves de operación en addons/arg_pyme_ventas/wizard/grouped_invoice.py y addons/arg_pyme_compras/wizard/purchase_bill.py
- [ ] T013 [US1] Agregar estadísticas F21 con base de costo explícita en addons/arg_pyme_informes/report/facts.py y dimensions.py

## US2

- [ ] T014 [US2] Implementar entrega de valores F05/F06 siguiendo specs/017-cartera-valores/tasks.md; verificar clasificación de dinero y medio en addons/arg_pyme_administracion/models/money_application.py

## US3

- [ ] T015 [US3] Implementar Reparaciones F01 conforme specs/018-reparaciones/tasks.md, sin equipo ajeno en stock propio
- [ ] T016 [US3] Implementar Obras F02 conforme specs/019-obras/tasks.md, evitando doble costo compra/consumo
- [ ] T017 [US3] Implementar Fabricación F04 conforme specs/020-fabricacion/tasks.md, distinguiendo kit/producción
- [ ] T018 [US3] Implementar Comisiones F03 conforme specs/021-comisiones/tasks.md, con reglas y liquidaciones históricas
- [ ] T019 [US3] Implementar Servicios F07/F08/F09 conforme specs/022-servicios/tasks.md, períodos y reservas concurrentes

## US4

- [ ] T020 [US4] Implementar Diseñador F10 conforme specs/023-disenador/tasks.md; no ejecutar código de plantilla arbitrario
- [ ] T021 [US4] Implementar POS F18 conforme specs/024-punto-venta/tasks.md; no duplicar REC/asientos/movimientos
- [ ] T022 [US4] Implementar núcleo de proveedores y adaptadores de eCommerce F11 en addons/arg_pyme_integraciones con contrato012 y pruebas técnicas sin publicar tienda
- [ ] T023 [US4] Implementar WhatsApp F12 en addons/arg_pyme_integraciones/providers/whatsapp.py, con destinatario revisable, estado y documento versionado; sin mensajes de ejemplo
- [ ] T024 [US4] Implementar adaptadores bancarios/ECHEQ en addons/arg_pyme_integraciones/providers/banking.py con capacidades/lookup y archivos según banco elegido; no simular operación real

## Polish

- [ ] T025 Actualizar manuales y catálogo tutorial versionado por cada entrega en docs/comunidad/youtube/catalogo.json y docs/usuario/
- [ ] T026 Revisar diff exacto/sintaxis/licencias/secretos y paquete, respaldar e instalar sólo módulos previstos; registrar en docs/entregas/EXPANSION-ENTREGAS.md
- [ ] T027 Fijar composición/hashes y estados de código/instalación/QA/aceptación sin declarar pruebas no ejecutadas en composition/versions.lock.json y docs/ESTADO-MODULOS.md

## Dependencies & Execution Order

E0 → US1 bases → US2 tesorería → US3 especializaciones → US4 herramientas/canales → Polish.
MVP: carga mínima y cartera con REC/OPA; objetivo completo conserva todas las22 capacidades.
El cierre técnico de una entrega no marca QA/aceptación ni activa canales.

## Parallel Examples

US1: manual y diseño de etiquetas en archivos separados; US2: documentación de informes tras fijar ejes.
US3: contratos de cada addon separados tras cerrar hooks comunes; US4: adaptadores separados después de contrato012.
No paralelizar modificaciones de motores compartidos ni instalaciones/promociones.

## Implementation Strategy

Primero contratos y núcleo, luego incrementos completos por módulo. Promover sólo artefactos fijados;
sin -u all ni sobrescrituras de datos. Mantener el objetivo activo mientras haya implementación necesaria pendiente.

## Avance técnico 2026-11-05

E0 y primer incremento de carga instalados con controles técnicos; T006 parcial (PPC fecha primero,
disposición de factura nativa pendiente). T008 en adelante y las tareas017–024 no se acreditan por
esta entrega. QA/aceptación posteriores. El objetivo de implementación completa sigue activo.

Incremento siguiente:017 tiene identidad y registro de borradores instalados técnicamente en aislado,
sin efectos financieros. T014 sigue abierta hasta completar REC/OPA y cartera conforme al contrato.
Ver [entrega de registro](../../docs/entregas/017-cartera-valores.md).

E1T006: Compras20.0.1.0.6 instalada en aislado; ficha contable combinada y procesada comprobada,
manteniendo fecha contable/vencimiento y condiciones visibles. Promoción a demo completada; T006 realizada.
018T002/T004–T011/T013/T014 acreditan código instalado/promovido a demo, sin QA; T015 padre sigue abierta por tutoriales/ejemplos de circuito.
[Promoción](../../docs/entregas/EXPANSION-PROMOCION.md).
[Instalación aislada](../../docs/entregas/EXPANSION-INSTALACION-AISLADA.md).

E1T008: F13 en0.1.7 y F19 de Catálogo1.2 instalados técnicamente en aislado/demo, sin doble maestro.
[Entrega F19](../../docs/entregas/005-precio-condiciones.md). No acredita QA, impresión ni aceptación;
F14–F17/F20–F22 y demás tareas conservan su alcance.

E1T009: F14 de Stock1.1 instalado técnicamente en aislado/demo, con historia y alta mínima de lotes.
[Entrega](../../docs/entregas/008-trazabilidad.md). T009 sigue abierta por F15/reposición; QA/aceptación separadas.
