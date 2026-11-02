# Documentos ARG

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Cada comprobante tiene código corto y número propios, asignados al primer guardado válido: PRE-000001, PED-000001, etc. La identidad interna no reemplaza el número fiscal ni la referencia del proveedor. No se reinicia por año ni se reutiliza al cancelar.

El encabezado común muestra la identidad y cada pendiente por separado. Pendiente, parcial y completo se calculan con cantidades/importes de origen; cerrado con faltante no significa completo. Cuando un eje no aplica, muestra No corresponde.
Origen y derivados permite recorrer documentos y vínculos por línea que tu rol pueda consultar. Los adaptadores de cada circuito aportan los vínculos reales; no se deducen de un texto.

Imprimir usa una plantilla común con tercero, generales, detalle, totales, estado y pendientes. Los documentos de la demo se marcan como ejemplo y los borradores como borrador. El PDF de gestión no acredita autorización fiscal.
Presupuesto y pedido se mantienen separados; confirmar PRE y generar PED son acciones distintas. Los adaptadores de los cinco circuitos están incluidos en la composición actual; QA funcional y aceptación pendientes. Guía escrita; videos pendientes de publicación.

Ver la [matriz de estados documentales](ESTADOS-DOCUMENTALES.md) para etiquetas, ejemplos de parciales y lectura de cada pendiente.
