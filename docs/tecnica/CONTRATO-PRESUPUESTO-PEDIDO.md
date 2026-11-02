# Presupuesto y pedido: documentos distintos — contrato v1.1

2026-11-01 · consumidores: Base, Documentos, Ventas, Informes y futuros rubros.
Incluye confirmaciones y generación parciales, sin duplicar compromisos entre revisiones.

## Presupuesto PRE

Modelo propio arg.pyme.quotation y líneas arg.pyme.quotation.line.
Cabecera: company_id, identity_id, partner_id, currency_id, pricelist_id, date, valid_until,
state, revision_number, previous_revision_id, commercial_root_id, confirmed_at, confirmed_by y order_ids.
Línea: quotation_id, commercial_line_key, sequence, product_id, description, uom_id, quantity,
accepted_quantity, ordered_quantity_net, unit_price, discount, tax_ids y totales por motor nativo de impuestos.
Importes con precisión de moneda; cantidades con precisión de unidad. No sumar unidades incompatibles.

Estados propios: draft, issued, partially_confirmed, confirmed, rejected, expired, canceled.
Borrador admite datos incompletos salvo compañía/identidad. Emitir y aceptar requiere cliente, moneda,
líneas válidas, unidades, precios e impuestos coherentes. Precio cero exige aceptación explícita.
Confirmar aceptación permite seleccionar cantidades por línea, entre cero y el pendiente de aceptación.
Estado parcialmente confirmado si hay aceptación sin completar todas las líneas; confirmado al aceptar todas.
Registrar actor, fecha y cantidades de cada aceptación. No aceptar cantidades vencidas sin nueva revisión.

Desde la primera aceptación, congelar condiciones y líneas en servidor. Se puede aceptar otra cantidad
bajo las mismas condiciones; renegociar requiere una revisión nueva, conservando el original consultable.
Guardar snapshot de nombre/domicilio del tercero, direcciones de entrega/facturación, condición de pago,
posición fiscal, moneda/tasa/fecha, lista y definición/importe de impuestos por línea aceptada.
IDs vivos de partner, pricelist o tax no sustituyen esa evidencia histórica.

## Generar un pedido PED

Acción explícita Generar pedido para cantidades aceptadas todavía no comprometidas.
Crear otro documento sale.order, con identidad PED, arg_quotation_id y arg_generation_key.
Cada sale.order.line conserva arg_quotation_line_id y commercial_line_key, cantidades y condiciones aprobadas.
Un PRE puede generar varios PED parciales, cada uno con número propio y clave de generación diferente.
El pedido nace en borrador operativo. Confirmar pedido es una acción posterior con políticas nativas.
No llamar sale.order.action_confirm al confirmar PRE ni durante generación del PED por defecto.

Bloquear raíz comercial y líneas; revalidar permisos, compañía, versión, aceptado y comprometido neto.
Cantidad seleccionada no excede aceptado menos ya comprometido. Usar clave idempotente estable de la operación
y unicidad SQL (company_id, arg_quotation_id, arg_generation_key). Reintento devuelve el PED existente.
Crear pedido, líneas y vínculos en una misma transacción; rechazar doble clic o concurrencia duplicada.
Comparar condiciones/totales de PED con snapshot aprobado. No recalcular silenciosamente por cambios de maestros:
conservar acuerdo y bloquear divergencia fiscal/técnica incompatible para revisión explícita.
No modificar motor fiscal para forzar valores históricos inválidos.

Pedidos directos, si están habilitados por permiso/configuración, muestran origen Directo sin PRE ficticio.
No cancelar PRE al generar PED. Ambos permanecen navegables por cabecera y líneas.

## Revisiones y compromiso neto

Toda cadena comparte commercial_root_id; cada línea conserva commercial_line_key.
Una revisión sustituye sólo condiciones/cantidades todavía no comprometidas. Calcular compromisos a través
de todos los PED de la raíz, con bloqueo común, para impedir PRE1→PED1 y PRE2→PED2 sobre la misma cantidad.
Un negocio adicional crea otro PRE raíz explícito, sin aparentar ser revisión de uno existente.

Cancelar PED no reabre ni cambia condiciones del PRE. Liberar cantidad para un nuevo PED sólo mediante
operación explícita registrada, si la cancelación/reversión es efectiva y no queda entrega/facturación activa.
Conservar también la operación idempotente anterior; no permitir que un reintento regenere el cancelado.
Bloquear renegociación de cantidad comprometida hasta corregir sus derivados de forma trazable.

## Efectos

Confirmar/aceptar PRE: ninguna existencia, reserva, factura, asiento ni cobro.
Generar PED borrador: ningún movimiento físico, reserva ni asiento.
Confirmar PED: compromiso y reservas/movimientos previstos según configuración; no entrega física ni cobro.
Validar REM: movimiento físico. Publicar FAC: cuenta por cobrar/contabilidad. Confirmar REC: dinero/aplicación según configuración.
Estado comercial, físico, contable, financiero y fiscal se muestran por separado.
Aplicar ESTADOS-Y-PENDIENTES.md: pendiente, parcial y completo en cada eje aplicable, con cantidades/importes.

## QA posterior preparado

Aceptación parcial, varios PED, doble clic/concurrencia, revisión con PED activo, cancelación con entrega activa,
reintento tras cancelación, servicio sin remito, cambio de tarifa/impuestos, moneda distinta, permiso restringido y segunda compañía.
Son escenarios preparados; no acreditan implementación ni operaciones ejecutadas.

## Base de cantidades e idempotencia de aceptación

Las cantidades elegibles y aceptadas se expresan como objetivos acumulados por raíz y commercial_line_key,
en unidad canónica compatible. Una revisión nunca guarda el saldo 6 como si fuera un nuevo objetivo total.
Campos: target_quantity_total, accepted_target_total, committed_quantity_net y carried_committed_quantity.
Al crear revisión, arrastrar compromiso vigente como mínimo aceptado; nuevas aceptaciones incrementan sólo
la porción adicional hasta el objetivo. Generable = max(0, accepted_target_total - committed_quantity_net).
La UI puede mostrar saldo revisable, pero lo etiqueta como saldo y no lo persiste como objetivo total.

Ejemplo: objetivo original 10, PED vigente 4, revisión del saldo 6. Nueva revisión conserva objetivo total 10,
compromiso arrastrado 4 y aceptación acumulada inicial 4. Aceptar las 6 restantes fija aceptado total 10;
se pueden generar 6 (10 - 4), no 2. Si el nuevo acuerdo total fuera 8, saldo nuevo 4 y generable final 4.
No permitir objetivo menor al compromiso efectivo sin reversión previa.
Precios/condiciones nuevas se aplican sólo al saldo; la impresión distingue compromiso previo con su PED y
condiciones históricas de la propuesta pendiente. No revalorizar lo comprometido con la tarifa de la revisión.

Cada aceptación parcial usa acceptance_key estable del gesto/operación, bloqueo de raíz y restricción única
(company_id, quotation_id, acceptance_key) en arg.pyme.quotation.acceptance, con líneas/cantidades objetivo,
actor, fecha y resultado. El reintento devuelve el evento ya creado y no incrementa nuevamente cantidades.
Las liberaciones de compromiso también tienen clave estable y evento inverso, no un decremento repetible.
