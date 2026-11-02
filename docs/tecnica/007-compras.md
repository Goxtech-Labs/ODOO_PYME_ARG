# Compras ARG — implementación comercial

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

`arg_pyme_compras` 20.0.1.0.3 depende de Base/UI/Terceros/Catálogo/Documentos y purchase, sin dependencia de
Ventas ni Stock. PPC extiende purchase.order; FRC/NCP extienden account.move. No hay otro libro de cantidades,
contabilidad, residual o existencias. Los modelos nuevos son wizard transitorio y evidencia de preparación.

## Estados y preparación

Los estados nativos draft/sent/to approve/purchase/cancel se conservan. Se exige responsable ARG en confirmar,
aprobar, cancelar o volver a borrador, además del permiso nativo. Se respetan _approval_allowed y doble aprobación.
No se admiten cambios RPC de estado ni evidencia mediante write o defaults de contexto. No se copia una acción
con un token privado serializable: los marcadores internos son objetos Python y se limpian de los retornos.

La confirmación congela tercero, compañía, moneda/tasa, condiciones, impuestos, líneas, unidades y totales.
El reporte PPC consulta esos valores. Los impuestos se verifican antes de facturar; modificar una definición
acordada exige revisar el pedido. Las líneas confirmadas quedan protegidas. Volver a borrador exige cancelado
o por aprobar, sin facturas activas; conserva historial/número y permite un nuevo acuerdo.

La preparación parcial tiene UUID por wizard y hash normalizado del detalle, evento inmutable y unicidad
SQL(order_id,operation_key). Un UPDATE efectivo del PPC serializa preparación y mutaciones comerciales bajo
el aislamiento nativo. Se relee el pendiente, se rechaza otro borrador y se crea una FRC draft con tipo explícito;
no se permite que default_move_type la transforme en NCP. El replay devuelve el documento previo incluso publicado.
La creación usa permisos normales; sólo la evidencia técnica se crea con sudo acotado después de validar negocio.

## Importes y hechos

La preparación usa _prepare_invoice y _prepare_account_move_line, conservando purchase_line_id y valores nativos;
no llama al post ni produce un movimiento físico. La factura requiere ref original del proveedor antes de publicar.
Puede registrarse FRC directa sin PPC. Notas nativas conservan reversed_entry_id y snapshot de origen cuando existe.
Los adaptadores de reportes/vínculos de Ventas y Compras delegan por tipo y componen super, sin depender del orden MRO.

La publicación agrega cantidades del lote efectivamente publicable por purchase_line_id y los otros documentos ya
publicados. Comprueba mismo producto/unidad base, cantidades positivas y neto no negativo. Si hay FRC, impide
superar product_qty o qty_received según purchase_method. Las NCP pueden corregir cantidades ya facturadas aunque
una devolución haya reducido qty_received; no pueden reabrir unidades nunca facturadas. No se cuenta un borrador
como facturación cumplida. Las fechas futuras soft se excluyen del lote inmediato y mantienen la programación nativa.

El guard y el cálculo de precios de proveedor/costo se ejecutan completos por compañía del PPC. Se conserva el
motor de precios/impuestos nativo, con guard de tasas propias efectivas. La fecha de publicación usa el método
nativo _get_invoice_currency_rate_date. No se fabrican tasas ni certificados fiscales.

## Seguridad y composición

Compras ARG implica purchase_user; Administrador ARG implica purchase_manager. Roles combinables con responsable.
ACL nativas de compañía y compra siguen vigentes. Administración recibe lectura de pedidos/evidencia. Público y
portal no tienen acceso a los modelos nuevos. La navegación de origen aplica ACL normales y compañías habilitadas.

Correcciones comunes de esta entrega: protección de defaults RPC de identidad documental y de estados/evidencia
comercial de Ventas; controles de líneas/orígenes; composición de account.move por tipo. Las versiones actuales de Documentos, Ventas y Compras se actualizan juntas cuando cambia el contrato compartido; ver composición. Esta entrega requiere Documentos20.0.1.0.5 para el helper de alcance monetario.

## Alcance pendiente

ENT/DCP y referencias stock.move/picking pertenecen a arg_pyme_compras_stock durante feature008, sin cargar modelos
stock ausentes desde este addon. Pago efectivo/OPA pertenecen a feature009. El residual informa deuda extinguida,
no dinero pagado; T011 sigue parcial hasta disponer de todos esos ejes. Instalación nativa purchase_stock previa
no equivale a implementación del puente ARG. Escenarios quickstart se reservan para QA funcional posterior.

Actualización009: adaptador opcional de dinero aplicado instalado; ver [Administración](009-administracion.md). No crea dependencia obligatoria inversa. Sin Administración se conserva fallback informativo; con ella se distinguen pago efectivo, deuda y alcance facturado. Código/instalación no acreditan QA funcional.
