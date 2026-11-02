# Informes ARG — implementación 20.0.1.0.1

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Addon original con depends Base/UI ARG. No hereda modelos opcionales ni declara comodels de módulos
que podrían faltar. La selección dinámica de fuentes consulta registro y has_access(read), sin sudo.
Instalación mínima sin account/stock y composición completa se controlan por separado.

## Arquitectura

arg.pyme.report.engine es abstracto: adapters ORM, dominios por compañía, fechas/moneda y dimensiones.
arg.pyme.report.query es TransientModel de filtros/página. ACL Informes/Administrador ARG y regla global
company_ids + create_uid=user.id. No guarda hechos, filas ni saldos paralelos. Los datos son estructuras
en memoria del servidor; cada request consulta de nuevo las fuentes actuales.

facts.py impone permisos de campos/registros con read antes de mostrar datos y documentos relacionados.
No recibe modelos, dominios ni medidas arbitrarios del cliente. Usa una fuente declarada internamente;
search respeta reglas nativas. Cada consulta fija compañía y, si es monetaria, moneda. Aplicaciones
requiere moneda de compañía y usa amount nativo una vez por partial; no joins que dupliquen dinero.
Vincula ambos apuntes publicados; las aplicaciones eliminadas no se presentan como vigentes.
Deuda usa amount_residual_currency actual y fechas de vencimiento, claramente distinta de saldo histórico.

Stock histórico usa quantity_product_uom nativo en product.uom_id y signos por extremo interno;
transferencias internas producen ambos extremos y sólo netean dentro del ámbito elegido. Restringe
almacenables actuales y ubicaciones internas propias. No promete reservas/valoración histórica ni
reconstrucción perfecta si se modificaron dimensiones históricas. Corte UTC y fechas visibles comparten
context tz → user.tz → UTC, validado mediante ZoneInfo. Los períodos de datetime son [inicio, día siguiente).

## Agrupación, paginación y salida

dimensions.py agrupa por IDs (no nombres que podrían repetirse), UOM y circuito físico. Sumas math.fsum
sobre filas fuente; no agrega redondeos intermedios. Total monetario separado de totales de cantidades,
sin sumar monedas/UOM incompatibles. Cada origen usa /odoo/modelo.con.punto/id, ruta nativa20.
Se limita la lectura a5001para detectar exceso; más de5000exige filtros, sin truncar. Navegador50filas;
agrupación y totales se realizan en servidor sobre el corte admitido completo.

Export CSV usa ruta GET auth=user, revalida consulta propia/permisos y genera bytes UTF-8 con BOM,
quoting y defensa de fórmulas/controles. Nombre de archivo fijo, no-store y nosniff. No exporta datos
proporcionados por el cliente ni columnas no leídas con permisos. QWeb recibe sólo un ID válido,
ignora payload de resultados, revalida y limita2000filas. A4 apaisado, t-out, sin HTML crudo de fuentes.
La consulta HTML usa Markup con interpolación escapada y sanitización del campo.

No depende de account_reports Enterprise ni de almacén externo. Tutorial escrito por versión20;
canal/contactos pendientes no se inventan. QA funcional/visual, límites con datos y aceptación quedan
posteriores; los controles de instalación/arranque no los acreditan. Ver entrega010 y quickstart.

Precisión de salida: se agregan valores fuente con fsum antes de formatear. Dinero usa redondeo
de moneda; cantidades usan precisión decimal Product Unit y decimales de unidad, sin cuantizarlas
al múltiplo UOM. HTML/PDF usan los mismos valores localizados; CSV usa equivalentes canónicos
con punto decimal y conserva negativos numéricos. No se recortan a doce cifras significativas.
