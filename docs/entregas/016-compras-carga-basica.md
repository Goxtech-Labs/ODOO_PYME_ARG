# Compras ARG · Carga básica de facturas recibidas

2026-11-06. Fuente20.0.1.0.6 preparada; instalación/registro, QA funcional/visual y aceptación pendientes.
No cambia la composición instalada, usuarios, datos de ejemplo ni configuración del servidor.

El formulario compartido muestra la fecha del comprobante de proveedor antes de proveedor y número
externo. Condiciones y contabilidad se distinguen en la columna derecha, conservando sus campos.
La fecha contable y vencimiento mantienen su significado. No se fuerza hoy en fechas existentes ni
se cambia ningún default, estado o operación. FRC/NCP internos no reemplazan la referencia externa.

Se mueven los nodos nativos con sus modificadores, sin copiar una ficha ni sustituir su controlador.
Menú, preparación parcial, enlaces y acceso avanzado usan esa misma herencia. in_receipt nativo
comparte el orden de proveedor; no se crea numeración ARG para ese tipo. Ventas/asientos conservan
sus campos de fecha originales. No se ocultan condiciones ni errores en secciones plegadas.

La revisión técnica de fuente compara locators y conservación de campos contra Community fijado;
no prueba la vista combinada del servidor ni la presentación en navegador. El acceso asignado sigue
pendiente de autenticación SSH; ningún upgrade se ejecutó. Parent016T006 conserva el pendiente técnico.

[Contrato](../../specs/007-compras/contracts/operaciones.md) · [Manual](../usuario/007-compras.md) ·
[Escenarios posteriores](../../specs/007-compras/quickstart.md)

[Composición candidata](../../composition/candidates/016-compras-carga-basica.json):285 archivos,
SHA256 `0adad0325df983bee917325f334f452a066555b272dfc71428cb30fd3a5f2f76`.
Control de fuente:6 locators nuevos únicos y202 nodos de campo conservados contra la ficha nativa
fijada, con modificadores de fecha de proveedor y ubicación/atributos de venta y contabilidad intactos.
No equivale a ejecutar el motor de vistas ni renderizar el formulario.
