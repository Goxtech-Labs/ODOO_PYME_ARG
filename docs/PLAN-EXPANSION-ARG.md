# Expansión funcional Pymes ARG · 2026-11-05

Estado: alcance definido para desarrollo e implementación por entregas. Este documento es el plan;
no acredita que sus funciones estén instaladas. El objetivo activo incluye implementarlas, no sólo documentarlas.

## Principios que gobiernan todas las entregas

1. Recuperar procesos útiles de FactuSOL y traducirlos a la operación argentina, sin copiar legislación,
   ficheros bancarios españoles, nombres engañosos ni recursos propietarios.
2. Carga principal: **fecha de hoy propuesta → a quién → documento → conceptos/artículos**. Lo conocido
   se deduce de configuración válida y lo secundario queda aparte. Conservar fechas corregidas y de origen.
3. Pensar en una persona con varios roles. No exigir departamentos, técnicos o aprobadores adicionales
   donde no sean necesarios; sí conservar permisos, validaciones y acciones explícitas.
4. Un documento representa un hecho. PRE y PED siguen separados; guardar no confirma ni envía.
5. Contabilidad y existencias nativas son las fuentes. No crear saldos financieros ni stocks paralelos.
6. Integraciones ARG es el único addon de proveedores externos. Los módulos especializados son opcionales.
7. Código, instalación, configuración, ejemplo, QA y aceptación son hitos distintos. No activar bancos,
   mensajería, tienda pública o emisión fiscal por instalar un módulo.

## Alcance completo y matriz de adaptación

| ID | Proceso de referencia | Adaptación/entrega ARG | Destino y estado inicial |
| --- | --- | --- | --- |
| F01 | Partes de reparación | Recepción de equipo ajeno, diagnóstico, presupuesto, autorización, repuestos/horas, entrega y factura | [018 Reparaciones](../specs/018-reparaciones/plan.md), nuevo opcional |
| F02 | Obras y capítulos | Partes de materiales/horas, costos previstos/reales, avance e hitos comerciales | [019 Obras](../specs/019-obras/plan.md), nuevo opcional |
| F03 | Agentes/comisiones | Reglas vigentes, propuesta, liquidación y pago, ajustes por devoluciones/rechazos | [021 Comisiones](../specs/021-comisiones/plan.md), nuevo opcional |
| F04 | Compuestos/fabricación | Kit distinto de fabricación real, materiales/mermas y producción nativos | [020 Fabricación](../specs/020-fabricacion/plan.md), nuevo opcional |
| F05 | Cheques | Cartera argentina propia/terceros, papel/ECHEQ, recepción, emisión, entrega, endoso, depósito, descuento, rechazo/recupero | [017 Valores](../specs/017-cartera-valores/plan.md), nuevo opcional |
| F06 | Remesas/pagarés | OPA, lotes de pagos y transferencias para el uso cotidiano del titular; pagaré jurídico como instrumento separado cuando se use | 017 + Administración existente, ampliación |
| F07 | Facturación periódica | Abonos y ocurrencias por período; borradores idempotentes y emisión explícita | [022 Servicios](../specs/022-servicios/plan.md), nuevo opcional |
| F08 | Reservas | Agenda de recursos/capacidad, horarios y cancelaciones; no confundir con reserva física | 022, nuevo opcional |
| F09 | Expedientes | Carpeta de documentos por cliente/trabajo, vínculos a obras y reparaciones | 022 con vínculos a 018/019, sin duplicar documentos |
| F10 | Diseñador documental/informes | Primero plantillas y bloques parametrizados seguros; después composición visual acotada | [023 Diseñador](../specs/023-disenador/plan.md), nuevo opcional |
| F11 | Tienda conectada | Pedidos, productos y existencias con contratos de sincronización; tienda Odoo o proveedor elegido | [012 Integraciones](../specs/012-integraciones/plan.md), adaptadores internos pendientes |
| F12 | WhatsApp/documentos | Envío explícito, destinatario revisable, versión documental y estado; soporte no equivale a envío integrado | 012, pendiente; no mensajes automáticos de ejemplo |
| F13 | Talles/colores | Variantes nativas, matriz por atributos, cantidades y etiquetas por variante | [005 Catálogo](../specs/005-catalogo/plan.md), base existente, ampliar UX especializada |
| F14 | Series/lotes | Consulta de cadena, búsqueda y carga simples; conservar conteos/movimientos existentes | [008 Stock](../specs/008-stock/plan.md), base existente, ampliar |
| F15 | Mínimos/máximos | Reposición nativa con propuesta revisable antes de compra/fabricación | 008 + [007 Compras](../specs/007-compras/plan.md), configurar/ampliar |
| F16 | Riesgo de clientes | Exposición, deuda vencida, valores pendientes, límites y excepciones por moneda | 004/006/009 y Valores; sin otro saldo contable |
| F17 | Etiquetas/códigos de barras | Modelos de impresión, variantes, precios y cantidades; sin imponer hardware específico | 005 + 015 Documentos; base nativa, experiencia pendiente |
| F18 | Punto de venta | Venta, cobro, ticket, devoluciones y cierre nativos con enlaces ARG sin doble efecto | [024 POS](../specs/024-punto-venta/plan.md); POS nativo ya instalado, integración ARG pendiente |
| F19 | Ofertas/condiciones especiales | Listas y reglas por cliente/producto/cantidad/vigencia; explicación del precio, no sobrescribir historia | 005/006, base de listas existente, completar experiencia |
| F20 | Facturación agrupada | Propuesta desde pedidos/remitos compatibles, parciales y varias fuentes por línea; sin doble factura | 006/007, ampliar sobre generadores actuales |
| F21 | Estadísticas comerciales | Márgenes, consumo por cliente, comparativos e indicadores explicables; distinguir costo histórico y actual | 010 Informes, ampliar hechos y métricas |
| F22 | Importación de tarifas/maestros | Vista previa, mapeo, moneda/impuestos, diferencias y clave de actualización; idempotencia y archivo original | 005/004, base nativa de importación, asistente ARG pendiente |

La lista cubre todos los faltantes y bases identificados y agrega cierres comerciales complementarios.
El contraste con el manual de FactuSOL se mantiene por función; no promete clonar todas sus ediciones
ni incorpora por este plan Contasol, Nominasol o reglas fiscales españolas.

## Recibo, órdenes de pago y valores: decisión del titular

**REC argentino** reúne medios de pago y cobra una o varias facturas. Admite efectivo, transferencias,
cheques y los medios habilitados, con importes parciales y cobros a cuenta existentes.

Ejemplo de aceptación: factura de 120000 ARS; REC con 20000 efectivo y cheque de 100000. Aplicación
de deuda 120000, efectivo 20000, valor en cartera 100000 y acreditación bancaria del cheque 0.
Depositar no cobra de nuevo la factura; acreditar reclasifica el valor. Rechazar exige corrección/reclamo
trazable del valor sin revertir los 20000 de efectivo ni duplicar deuda.

**OPA** es la orden/comprobante de pago a proveedor; puede incluir varios medios y aplicaciones.
Un **lote de pagos** agrupa OPA/instrucciones, pero no genera otra salida de dinero. Una **transferencia**
es el medio/operación bancaria con referencia, origen y destino: preparada no equivale a ejecutada.
El uso práctico de remesas/pagarés descrito por el titular se resuelve con estas operaciones argentinas;
no se importan SEPA/IBAN como requisito. Si se usa un pagaré legal, se registra su instrumento y
vencimiento, separado de OPA, sin convertir cada orden en un título firmado.

## Etapas y dependencias

| Etapa | Entrega | Depende de | Criterio de salida de implementación |
| --- | --- | --- | --- |
| E0 | Inventario real, principios y contratos monetarios | Núcleo actual | Composición técnica releída, decisiones y tareas trazables |
| E1 | Carga básica y bases comerciales F13–F17/F19–F22 | E0 | Fechas/contexto, fichas, catálogos y derivaciones implementados sin perder datos |
| E2 | REC/OPA ampliados y cartera F05/F06 | E0 y fuentes nativas | Eventos/instrumentos, deuda y liquidez separados; instalado con configuración explícita |
| E3 | Reparaciones F01 | E1 y revisión de hooks stock/ventas | Recepción y circuito completo, sin contabilizar equipo ajeno como propio |
| E4 | Obras y fabricación F02/F04 | E1/E3 sólo por vínculos opcionales | Costos/producción nativos y contratos de consumo compatibles |
| E5 | Comisiones y servicios F03/F07–F09 | E2 para cobros efectivos; E1 para ventas | Liquidación y ocurrencias idempotentes; reservas sin sobreasignación |
| E6 | POS y diseñador F18/F10 | E1/E2 y composición POS | Sin duplicar cobros/stock, impresión segura y trazable |
| E7 | Canales F11/F12 y conectores bancarios | 012 y contratos de cada área | Adaptadores implementados, desactivados hasta configuración/activación específica |

Las etapas son orden de trabajo, no fechas comprometidas. La implementación se entrega por incrementos;
QA funcional/visual y aceptación se registran después, conforme al flujo acordado, sin ejecutar movimientos
ficticios en la demo compartida. No hay autorización implícita para envíos, cobros bancarios o CAE reales.

## Composición y arquitectura

La consulta del 2026-11-05 encontró 101 módulos instalados y POS nativo. El lock publicado describe la
entrega histórica de 91; no actualizarlo como si el inventario nuevo fuese una promoción verificada.
Antes de otra entrega hay que fijar versiones/hashes y procedencia de los diez módulos adicionales.
Entre los candidatos revisados no están instalados repair, mrp, project, hr_timesheet, sale_commission,
l10n_ar_check, account_batch_payment ni website_sale. Su ausencia no autoriza instalar sin inspección.

Nuevos addons propios propuestos: arg_pyme_valores, arg_pyme_reparaciones, arg_pyme_obras,
arg_pyme_fabricacion, arg_pyme_comisiones, arg_pyme_servicios, arg_pyme_disenador y arg_pyme_pos.
El núcleo nunca depende de ellos. Integraciones externas siguen exclusivamente en arg_pyme_integraciones,
con adaptadores internos para bancos/ECHEQ, comercio electrónico y WhatsApp, no un addon por proveedor.

Puntos de integración a resolver: hooks ARG globales de movimientos/quants para repair/mrp/POS;
guardas de creación/cambio de PED para recurrencia/eCommerce; motor de tesorería y money_application
para distinguir instrumento de liquidez. No sortearlos con sudo o flags RPC falsificables.

## Formato de cada entrega

Spec y contrato por módulo → implementación → revisión exacta de cambios y controles técnicos → paquete
fijado → respaldo → instalación/arranque → manual/ejemplos → QA posterior → aceptación personal.
No borrar ni reemplazar documentos del usuario. Migración de medios manuales anteriores exige inventario,
clasificación y conciliación; nunca inferir que un pago antiguo era cheque por su texto libre.
Cada módulo incluye ficha de tutorial YouTube con versión/estado; un canal general no acredita video publicado.

## Fuentes y trabajo programable

[Spec coordinadora](../specs/016-expansion-argentina/spec.md), [plan técnico](../specs/016-expansion-argentina/plan.md),
[tareas](../specs/016-expansion-argentina/tasks.md) e [investigación](../specs/016-expansion-argentina/research.md).
Las fuentes oficiales argentinas orientan el diseño; las políticas contables y de proveedor se versionan
y se revalidan al implementar. Este plan no certifica validez jurídica de títulos emitidos por el sistema.
