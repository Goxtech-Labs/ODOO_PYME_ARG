# Compras ARG · Carga básica de facturas recibidas

2026-11-06.20.0.1.0.6 instalado técnicamente en aislado; QA funcional/visual y aceptación pendientes.
La composición de la demo compartida conserva su versión anterior.

El formulario compartido muestra la fecha del comprobante de proveedor antes de proveedor y número
externo. Condiciones y contabilidad se distinguen en la columna derecha, conservando sus campos.
La fecha contable y vencimiento mantienen su significado. No se fuerza hoy en fechas existentes ni
se cambia ningún default, estado o operación. FRC/NCP internos no reemplazan la referencia externa.

Se mueven los nodos nativos con sus modificadores, sin copiar una ficha ni sustituir su controlador.
Menú, preparación parcial, enlaces y acceso avanzado usan esa misma herencia. in_receipt nativo
comparte el orden de proveedor; no se crea numeración ARG para ese tipo. Ventas/asientos conservan
sus campos de fecha originales. No se ocultan condiciones ni errores en secciones plegadas.

La revisión técnica de fuente compara locators y conservación de campos contra Community fijado;
no prueba la presentación en navegador. La lectura posterior del servidor verificó la vista combinada
y procesada, con233 nodos de campo y el orden esperado. Parent016T006 conserva la promoción pendiente.

[Contrato](../../specs/007-compras/contracts/operaciones.md) · [Manual](../usuario/007-compras.md) ·
[Escenarios posteriores](../../specs/007-compras/quickstart.md)

[Composición candidata](../../composition/candidates/016-compras-carga-basica.json):285 archivos,
SHA256 `0adad0325df983bee917325f334f452a066555b272dfc71428cb30fd3a5f2f76`.
Control de fuente:6 locators nuevos únicos y202 nodos de campo conservados contra la ficha nativa
fijada, con modificadores de fecha de proveedor y ubicación/atributos de venta y contabilidad intactos.
Este control de fuente es distinto del registro/procesamiento de vistas comprobado después en aislado;
ninguno acredita revisión visual. [Instalación y composición](EXPANSION-INSTALACION-AISLADA.md).
