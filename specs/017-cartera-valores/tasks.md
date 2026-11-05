# Tasks: Cartera de valores y tesorería argentina

Estado: base de registro instalada en aislado; efectos financieros pendientes. QA/aceptación posteriores en quickstart.md.


## Setup

- [x] T001 Inspeccionar candidato nativo, licencia/APIs y hooks de esta composición; registrar decisión en specs/017-cartera-valores/research.md

## Foundation

- [x] T002 Fijar identidad, campos y transiciones del contrato en specs/017-cartera-valores/data-model.md
- [x] T003 Crear manifest/dependencias opcionales sin ciclo ni core modificado en addons/arg_pyme_valores/__manifest__.py

## US1

- [ ] T004 [US1] Implementar carga básica, valores por contexto y las invariantes: El nominal es positivo, en la moneda del instrumento, y no cambia después del primer evento confirmado. Destino addons/arg_pyme_valores/models/value_instrument.py
- [x] T005 [US1] Crear roles y reglas multiempresa; sin sudo para operaciones del usuario en addons/arg_pyme_valores/security/ir.access.csv
- [x] T006 [US1] Presentar fecha/tercero/documento/detalle y secundarios progresivos en addons/arg_pyme_valores/views/value_views.xml

T004 parcial: carga/defaults/validación positiva y cancelación de borrador implementadas. Inmovilidad
tras el primer evento financiero sigue pendiente de US2. T007 tiene infraestructura append-only de
borradores, sin las operaciones financieras del contrato. No marcar ambas como completadas.

## US2

- [ ] T007 [US2] Implementar operaciones y relaciones descritas en contracts/operaciones.md con idempotencia/corrección; destino addons/arg_pyme_valores/models/value_event.py
- [ ] T008 [US2] Implementar operaciones y relaciones descritas en contracts/operaciones.md con idempotencia/corrección; destino addons/arg_pyme_valores/models/treasury_value.py
- [ ] T009 [US2] Implementar operaciones y relaciones descritas en contracts/operaciones.md con idempotencia/corrección; destino addons/arg_pyme_valores/models/payment_batch.py
- [ ] T010 [US2] Implementar operaciones y relaciones descritas en contracts/operaciones.md con idempotencia/corrección; destino addons/arg_pyme_valores/models/bank_transfer.py
- [ ] T011 [US2] Implementar operaciones y relaciones descritas en contracts/operaciones.md con idempotencia/corrección; destino addons/arg_pyme_valores/models/promissory_note.py
- [ ] T012 [US2] Hacer cumplir en servidor: Un instrumento no puede estar reservado o comprometido simultáneamente por dos salidas.; Transmitir el título no fracciona su identidad; imputar su importe a varias facturas es otra operación.; El nominal en cartera no es dinero bancario disponible ni se vuelve a cobrar al liquidarlo.; Evento confirmado es inmutable; reversión explícita enlazada conserva historia y revisa su efecto contable.; La integración bancaria no se ejecuta desde un formulario de cartera ni se infiere de una referencia manual. Destino addons/arg_pyme_valores/models/operaciones.py

## US3

- [ ] T013 [US3] Exponer consulta/estados/origen y adaptador de hechos sin doble suma en addons/arg_pyme_valores/models/report_adapter.py
- [ ] T014 [US3] Crear informe/documento con moneda, estado y evidencia en addons/arg_pyme_valores/report/document.xml

## Polish

- [ ] T015 Documentar manual, ejemplos, límites y ficha de tutorial versionada en docs/usuario/017-cartera-valores.md
- [ ] T016 Resolver sintaxis, carga de vistas e instalación/arranque de composición; registrar sin atribuir QA en docs/entregas/017-cartera-valores.md
- [ ] T017 Fijar paquete/versiones, respaldo y promoción autorizada con hashes en composition/versions.lock.json

## Contrato financiero específico

Aplicar contracts/cartera-argentina.md como requisito de US2: REC multimedio aplica facturas,
valor pendiente no acredita banco, transmisión/negociación no duplica cobro y rechazo es trazable.

## Dependencies & Execution Order

Setup → Foundation → US1 → US2 → US3 → Polish. US2 depende de contrato/roles US1; US3 usa efectos ya definidos.
MVP: carga y circuito mínimo completo, sin activar canales externos. No delegar escrituras de archivos compartidos en paralelo.

## Parallel Examples

Con contratos fijados, manual y recursos de ayuda pueden prepararse en archivos separados mientras se implementa cada historia.
US1: fichas/roles separados; US2: adaptadores separados sólo tras fijar interfaz; US3: manual e informe con grano acordado.

## Implementation Strategy

Entregas pequeñas completas y composición fijada. Las tareas de implementación permanecen sin marcar hasta evidencia de código/instalación.
QA funcional/visual y aceptación no forman parte del conteo de implementación; se registran después mediante quickstart.md.
