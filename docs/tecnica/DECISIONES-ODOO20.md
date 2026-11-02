# Decisiones técnicas y evidencia Odoo 20

Fecha de investigación: 2026-11-01. Base: Community estable 20.0.
Fuente inspeccionada: revisión `bb238af6f0ddd70d7ff91521c6104472583661d1` del repositorio público Odoo.
El paquete instalado `20.0.20261101` tiene procedencia apt propia; no afirmar que su árbol corresponde exactamente a ese SHA.
Revalidar APIs contra el paquete al implementar cada módulo.

| Área | Comportamiento comprobado | Decisión ARG |
| --- | --- | --- |
| Ventas | `sale.order` nativo pasa de draft/sent a sale sobre el mismo registro | Crear presupuesto propio `arg.pyme.quotation`; PED es otro documento basado en `sale.order` |
| Compras | `purchase.order.line` usa `uom_id`; ventas usa `product_uom_id` | No trasladar campos de otra versión sin inspección |
| Entregas | Estado full puede incluir transferencias canceladas | Mostrar cumplido, pendiente abierto y faltante cerrado por cantidades |
| Stock | `stock.quant` y movimientos son fuente nativa; inventario aplica diferencias mediante movimientos | Documento INV agrupa conteos, no mantiene otra existencia |
| Puentes | `sale_stock` y `purchase_stock` son auto_install y sus hooks pueden afectar pedidos abiertos | Activación posterior como migración previsualizada y respaldada |
| Pagos | Estados draft, paid, reconciled, canceled, rejected | No usar estado posted para `account.payment` |
| Deuda | `invoice_ids` no implica conciliación; un pago puede no tener asiento | Aplicar mediante `account.payment.register` y conciliación; exigir cuentas transitorias antes de confirmar REC/OPA |
| Aplicaciones | `account.partial.reconcile` relaciona apuntes débito/crédito con importes y monedas | No escribir residuales ni mantener otro libro de saldos |
| Localización | `l10n_ar` Community depende de account y l10n_latam_invoice_document | No atribuirle emisión CAE por sí sola |
| Informes | `account.invoice.report` tiene grano de línea y no representa caja | Separar hechos y no depender de `account_reports` Enterprise |
| Bot | `mail.bot` usa `base.partner_root`, datos noupdate | Cambiar nombre/avatar por hook idempotente, preservando ID; inventariar textos y traducciones |
| Parámetros | En runtime 20 se verificaron `set_str`, `set_bool`, `get_str`, `get_bool` | No usar `set_param/get_param` heredados sin verificar |
| CLI | `odoo server` expone flags; `--without-demo` recibe booleano | Usar ayuda del binario instalado; no copiar comandos de Odoo 17/18 |

## Arquitectura de módulos

Base ARG declara identidad, secuencias, roles y ayuda. UI ARG depende de Base, web y mail_bot.
Terceros y Catálogo extienden maestros. Documentos depende de Base y UI, sin depender de Ventas.
Ventas/Compras/Stock/Administración consumen esos contratos sin dependencias circulares.
Informes depende sólo de Base/UI: registra adaptadores locales para modelos instalados y oculta consultas sin fuente.
No cargar XML, campos relacionales ni vistas SQL a tablas ausentes; los adaptadores deben validar disponibilidad antes de registrarse.
Los puentes operativos nativos se instalan según composición y se inventarían explícitamente.

Integraciones ARG es el único addon de proveedores externos. ARCA es un incremento interno, no un addon que dependa de sí mismo.
Los rubros sí pueden agregar addons especializados opcionales. No modificar core Odoo ni copiar Enterprise.

## Fuentes primarias

- [Código Odoo fijado](https://github.com/odoo/odoo/tree/bb238af6f0ddd70d7ff91521c6104472583661d1).
- [Paquetes oficiales](https://nightly.odoo.com/).
- Cada spec incluye los archivos de investigación concretos; los métodos mencionados son evidencia de esa revisión y requieren control al instalar.

## Licencias y composición

Conservar atribuciones Odoo y revisar licencia de cada dependencia antes de incorporarla.
Decisión expresa del titular, 2026-11-01: código original AGPL-3.0 (SPDX AGPL-3.0-only) y documentación/recursos CC-BY-SA-4.0. Textos y excepciones en NOTICE.md y LICENSES/. Reemplaza la propuesta previa de AGPL-3.0-or-later; no se extiende la autorización a versiones futuras no elegidas.
Elegir textos definitivos antes de publicación/distribución del código. Programación local y especificaciones pueden continuar.
No afirmar que el alojamiento, Internet o servicios externos sean gratuitos: la libertad del proyecto no elimina esos costos elegidos.

## Puentes operativos propios

Crear arg_pyme_ventas_stock (deps arg_pyme_ventas, arg_pyme_stock, sale_stock) y
arg_pyme_compras_stock (deps arg_pyme_compras, arg_pyme_stock, purchase_stock), auto_install sólo cuando están todas las dependencias.
No son conectores de servicios externos: no contradicen Integraciones ARG único.
Cada puente posee campos/vistas de picking, sale_line_id/purchase_line_id, acciones REM/ENT y cantidades físicas.
Los addons Ventas/Compras solos no referencian modelos/campos de stock ni cargan esas vistas.
Sin puente, ofrecen documentos comerciales/contables y no muestran indicadores de entrega que no tengan fuente.
Con puente, usar métodos nativos y tratar su instalación sobre pedidos abiertos como migración controlada.

## ACL del runtime 20 verificado durante implementación
El paquete instalado unifica permisos y restricciones en ir.access; CSV con columnas id,name,model_id,group_id/id,operation,domain. Grupos con dominio conceden permisos; filas sin grupo restringen. No usar ir.model.access/ir.rule de versiones anteriores. Privilegios de grupos usan res.groups.privilege.

Binary/Image en runtime20 requieren BinaryValue (p. ej. odoo.tools.binary.BinaryBytes con bytes crudos), no base64 bytes ORM. Se verificó al instalar identidad visual. Las funciones XML sin record IDs necesitan @api.model.

## Hallazgos durante Ventas006 y extracción reproducible

- OWL4: inputs proxy usan eventos explícitos; t-model requiere SignalWithSet.
- Bundles Odoo incluyen mtime: el tar reproducible usa0; instalación aplica mtime actual al extraer código, sin alterar contenido ni borrar adjuntos de usuario.
- SaleLine usa tax_ids plural; qty_invoiced_posted distingue facturas publicadas de borradores.
- _get_product_price_rule y helpers de impuestos se llaman con compañía del documento. Las reglas fijas pueden convertir extras de variantes; listas derivadas convierten recursivamente.
- Monedas: _get_rates devuelve rate/rate_date y puede elegir fallback1/fecha futura o anclajes globales. Guard ARG exige tasa explícita efectiva de compañía raíz; no altera motor nativo.
- AccountMove usa _get_invoice_currency_rate_date para validar la misma fecha que aplicará al publicar.
- Residual saldado admite NC/ajustes: no es dinero cobrado. Administración debe separar liquidez efectiva de deuda extinguida, incluyendo write-offs y descuentos, sin duplicar pago por factura.
- Listas de ejemplo inspeccionadas en demo: Predeterminado y Ejemplo—Lista general ARG en ARS; no fue necesario inventar FX ni cambiar preferencias de clientes.

## Hallazgos durante Compras007

- purchase.order._prepare_invoice toma default_move_type del contexto: preparación ARG fuerza in_invoice/draft.
- qty_invoiced de compras incluye borradores: el eje ARG agrega sólo AML de movimientos publicados y resta notas.
- _post por lote comprueba cantidades agregadas y neto por purchase_line_id; el lock PPC no sustituye validar el propio lote.
- Precio proveedor/costo: el cálculo nativo entero debe usar with_company del pedido, no sólo la selección de seller.
- Los defaults RPC también son entradas: proteger estados, identidades, snapshots y vínculos tanto en cabeceras como líneas.
- Adaptadores account.move se componen con super y despacho por tipo; no depender del orden MRO entre Sales/Compras.

## Hallazgos Stock008

- tracking=False es por cantidad; no comparar con selección 'none'. StockMove usa uom_id/quantity.
- Devolución está en picking.action_return; stock_account define to_refund y conserva valor del origen.
- No-backorder puede cerrar saldo sin crear split cancelado: ARG registra arg_closed_quantity_base explícito.
- Capturar demanda sólo al finalizar/cancelar evita congelar un wizard abandonado antes de editar.
- Quant.quantity/reserved/dimensiones y aliases quant_id en detalle terminal requieren guard de motor; proteger también padres destino y líneas comerciales.
- Inventario nonce por producto y huella de quants detecta concurrencia, incluidos productos sin quant previo; unidades/templates se bloquean antes de comparar.
- Matriz actual limpia contexto histórico/lot/owner/package y usa el mismo dominio de ubicación para reservas.

## Orden efectivo de vistas en acciones nativas

Un view_mode=list,form y view_id=list no garantizan entrada por lista si ir.actions.act_window.view
sólo registra explícitamente form. La definición efectiva puso form antes de list en ocho acciones ARG,
comprobado por lectura del runtime. Se corrigió agregando registros list explícitos de secuencia anterior
al formulario: productos, PRE, PED, PPC, movimientos, inventarios y ambas cuentas corrientes.
Verificar views resuelta y tabla del listado al comprobar arranque; una presencia transitoria de selector
no demuestra el modo inicial definitivo. Conservar historial de esta corrección sin reinterpretar
los checks anteriores como validación funcional.
