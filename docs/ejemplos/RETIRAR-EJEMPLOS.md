# Conservar y retirar ejemplos

Los cargadores inicializan una base de ejemplo nueva, no una migración real. Para comenzar una
empresa con datos definitivos, preferir otra base nueva con la composición elegida y conservar
la demo separada para aprendizaje. No ejecutar el inicializador de ejemplo sobre datos reales.

## Inventario del lote completo

| Identificador externo | Modelo / contenido |
| --- | --- |
| arg_demo.customer_retail | res.partner, Ejemplo — Cliente Mostrador |
| arg_demo.customer_pyme | res.partner, Ejemplo — Cliente Pyme |
| arg_demo.supplier_general | res.partner, Ejemplo — Proveedor General |
| arg_demo.product_a | product.template, Ejemplo — Producto A |
| arg_demo.product_b | product.template, Ejemplo — Producto B |
| arg_demo.service_a | product.template, Ejemplo — Servicio A |
| arg_pyme_catalogo.demo_pricelist | product.pricelist, lista general ARS; con Catálogo ARG |
| arg_demo.demo_pricelist | alternativa del cargador cuando no hay Catálogo ARG |
| arg_demo.finance_cash / finance_bank | diarios Caja/Banco creados por seed_finance_demo |
| arg_demo.outstanding_inbound / outstanding_outbound | cuentas transitorias sólo si no existían plantillas nativas compatibles |

La compañía principal, depósito y administrador son registros nativos reutilizados por el
inicializador; no son un conjunto de registros nuevos que pueda borrarse por su nombre.
Los medios manuales y cuentas creados por Odoo al preparar diarios pueden tener otros IDs nativos.
Las preferencias REC/OPA se configuran en la compañía. Registrar todos los vínculos efectivos antes
de tocar configuración; un nombre que comienza por Ejemplo no prueba que sea parte del lote.

## Archivo controlado si se reutiliza una copia de demo

1. Respaldar y verificar DB, filestore, configuración y código. Inventariar por ID externo y modelo,
   incluyendo referencias desde documentos y preferencias. Separar lo ficticio de lo incorporado después.
2. Preparar maestros definitivos por importación idempotente, con mapa propio y datos autorizados.
   No convertir automáticamente un tercero ficticio en un cliente real por coincidencia de nombre.
3. Actualizar explícitamente los predeterminados futuros de compañía, listas y medios. Los documentos
   numerados y sus snapshots históricos se conservan; no reescribir su tercero, precios o identidad.
4. Archivar contactos/productos/listas de ejemplo sólo tras comprobar que no son predeterminados
   vigentes. Mantener sus IDs externos y referencias para consultar historia. Archivar no es borrar.
5. Para diarios, cuentas, ubicaciones, compañía o administrador, usar las acciones y restricciones
   nativas aplicables, con responsable y mapa de reemplazo. No borrar cuentas con apuntes ni desactivar
   el acceso administrador antes de probar su reemplazo autorizado.
6. Confirmar qué registros siguen activos, cuáles se archivaron y dónde se conservan referencias.
   La retirada de recursos de infraestructura y la migración real son encargos separados.

Esta guía no ejecuta archivo, eliminación, importación ni sustitución de datos. La demo entregada
conserva sus maestros de ejemplo y no contiene operaciones de negocio.
