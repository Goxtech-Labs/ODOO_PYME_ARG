# Ventas ARG — contrato de implementación

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Addon `arg_pyme_ventas`, 20.0.1.0.4; Odoo Community 20.0.20261101.
Depende de Base, UI, Terceros, Catálogo, Documentos ARG y `sale_management`.
No modifica el core. Stock y contabilidad conservan los libros nativos.

## Entidades y operaciones

`arg.pyme.quotation` y sus líneas son PRE propios. `sale.order` y `sale.order.line` conservan PED nativos.
La aceptación usa eventos inmutables y snapshots de tercero, condiciones, moneda/tasa, impuestos y
cantidades/precios. La generación conserva vínculo por cabecera y línea, raíz comercial y clave estable;
no reconstruye origen desde un texto. Las revisiones conservan objetivos acumulados y compromisos previos.

Aceptación, generación y liberación usan clave de operación, hash de contenido y unicidad SQL. Un UPDATE
efectivo sobre la raíz comercial serializa operaciones y mutaciones de condiciones/líneas bajo el aislamiento
nativo. La capa HTTP conserva sus reintentos ante conflictos de serialización. No existe endpoint de escritura
libre para cambiar los estados ni la evidencia protegida. Los marcadores internos son objetos Python privados,
no cadenas aceptables desde un contexto RPC; las acciones devueltas limpian esos marcadores.

Los pedidos cancelados siguen comprometidos hasta una liberación explícita autorizada, sin entregas/facturas
activas. Una revisión posterior no puede ignorar esos compromisos. Las cantidades son precisas por unidad,
sin sumar unidades incompatibles. El importe de una nueva revisión corresponde al saldo; las condiciones
históricas arrastradas se presentan por separado.

## Seguridad

Operador prepara y consulta; responsable confirma/revierte; roles combinables. Rigen ACL y compañías nativas.
Las búsquedas de compromisos necesitan visibilidad compartida de pedidos ARG derivados dentro de la compañía;
no se usa sudo para leer negocio oculto. Sudo queda acotado a crear evidencia técnica inmutable tras validar
permisos y operación. Finanzas tiene lectura de origen/evidencia. Portal y público no acceden a los modelos propios.
Los cambios de tipo/estado contable no permiten eludir el circuito de publicación/reversión.

## Precios, impuestos y moneda

El cálculo reutiliza los helpers de precios/impuestos nativos de Odoo20 y fija la compañía del PRE.
Valida recursivamente las monedas de listas base, además de las cotizaciones requeridas por contabilidad.
`res.currency._arg_require_conversion` exige tasa explícita de la compañía raíz coincidente con la que eligió
el motor nativo. Rechaza fallback implícito, tasas globales de anclaje, no finitas o futuras. No altera las tasas
ni sustituye el motor nativo. Esta revisión de Odoo usa búsqueda anterior a la fecha en `_get_rates`; una tasa
cargada sólo el mismo día puede no ser la efectiva. El usuario debe configurar la tasa efectiva; no inventar
un valor para sortear ese límite de la versión.

Las reglas/impuestos congelados se verifican antes de generar o publicar; si sus definiciones cambiaron,
se pide una revisión. El tratamiento fiscal mixto de descuento por pronto pago queda bloqueado hasta contar
con adaptador. Por ahora una preparación de factura no agrupa varios PED. Las unidades son las base del producto.

## Indicadores y límites de composición

Se implementan aceptación PRE, generación de PED, facturación publicada y cancelación de deuda facturada.
`qty_invoiced_posted` evita contar borradores como facturación cumplida. El residual nativo informa deuda
extinguida; no se etiqueta como caja/cobro. Administración aporta su eje de dinero efectivamente aplicado,
separando notas, ajustes, diferencias de cambio y descuentos. No completar T011 por esta primera entrega.

T012 requiere `arg_pyme_ventas_stock` durante Stock ARG. No hay dependencias físicas en el addon comercial.
La instalación previa de `sale_stock` nativo en la composición demo no acredita el puente ARG ni sus indicadores.
Los servicios sin entrega mostrarán No corresponde en ese puente. Se mantienen los estados técnicos nativos.

## Revisión y validación

Revisión estática independiente por otras sesiones Codex; mismo modelo/cuenta, por lo que no representa
independencia de proveedor. Corrige bypass de estados/tipo contable, contexto multiempresa y cadenas monetarias.
Controles de entrega: sintaxis Python/XML/JS, manifests/archivos, secretos, instalación/upgrade y arranque técnico.
No se ejecutan aceptación, generación, facturación, cobros ni movimientos como QA antes del despliegue.
Los escenarios de `specs/006-ventas/quickstart.md` quedan para QA posterior y aceptación del usuario.

Actualización en entrega007: ver [registro](../entregas/007-compras.md). Defaults RPC protegidos y composición de adaptadores.

Actualización009: adaptador opcional de dinero aplicado instalado; ver [Administración](009-administracion.md). No crea dependencia obligatoria inversa. Sin Administración se conserva fallback informativo; con ella se distinguen pago efectivo, deuda y alcance facturado. Código/instalación no acreditan QA funcional.
