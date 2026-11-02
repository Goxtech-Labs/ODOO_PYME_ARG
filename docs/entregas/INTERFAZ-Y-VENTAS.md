# Interfaz ARG y revisión de Ventas · 2026-11-02

## Resultado

Interfaz20.0.1.1.2: pestañas por circuito, cinta con documentos/operaciones y datos/catálogos,
Configuración según permisos, ayuda accesible, cinta contraíble y desplazable. Lucide1.66.0 local,
34 SVG con licencia/procedencia; ilustración IA ficticia de industria argentina en Inicio/acceso.
Campos de escritura y selección delimitados; fecha usa el botón nativo Odoo20. Tema y densidad en
Mis preferencias. Sin campos obligatorios nuevos ni cambio de autenticación.

[Vista real en tema claro](../assets/inicio-arg-v1.jpg). [Recursos](../RECURSOS-VISUALES.md).
Paquete227 archivos SHA256 `a4e0dcadaaa7a64985cda7fdf56429f9c1a904b700986d5c8c9a2b1d199d24bf`; instalación/upgrade en aislado antes de demo.
Archivos instalados y versiones contrastados con recibo;91 módulos. Login/Inicio/Ayuda/Soporte/Acerca
y recursos locales HTTP200. Fuente pública en main se registra mediante historial Git.

## Fallos reproducidos y corregidos

1. Confirmar cantidades de PRE fallaba por `uom.uom.rounding`, retirado en Odoo20. Los consumidores
   usan el quantum de `decimal.precision` / Product Unit, de acuerdo con el motor nativo. Se conserva
   el redondeo monetario independiente. PRE congela precisión y definición de unidad en su evidencia.
   Un snapshot aceptado antiguo sin esta precisión exige revisión; no se inventa historia.
2. QWeb servidor ignoraba `t-esc`, generando valores vacíos en impresión. Se cambió a `t-out` en las
   tres plantillas de servidor; se conserva escape y OWL nativo. Se verificó HTML con código, título,
   tercero, líneas/cantidades, importes y marca de ejemplo en PRE/PED/REM/FAC.
3. QA visual corrigió menú duplicado, acceso a configuración, contraste oscuro de tablas/botones,
   superficie del campo de fecha y espacio de toolbar. Login usa azul ARG conservando el flujo nativo.

## Recorrido aislado verificado

Fixture versionado: [qa_sales_flow.py](../../ops/qa_sales_flow.py), guardado para una base de ejemplo
explícita y contenedor con sólo loopback, sin cron ni servidores de correo activos. Usuario de negocio,
sin sudo para realizar las operaciones. No ejecutar contra la demo del propietario.

| Paso | Resultado observado |
| --- | --- |
| PRE-000002 por2 unidades de10000ARS | Confirmado; no crea stock/asientos/pagos |
| Generar PED-000001 | Documento distinto, líneas enlazadas; reintento devuelve el mismo pedido |
| Confirmar PED | Crea REM-000001, no factura |
| Apertura INV ficticia de10 | Ajuste nativo trazable, sólo en base aislada |
| Entregar1 de2 | REM terminado; REM-000002 pendiente por1; pedido con entrega parcial |
| Facturar1 de2 | FAC-000001 publicada en diario QARG interno, total/residual10000ARS |
| Revisar efectos | Factura no mueve stock; saldo físico9; entrega/facturación/deuda separados |
| Protecciones | Cambio directo de estado, términos aceptados, cantidad derivada y evidencia rechazados |
| Informes | PED2, FAC1, existencia9; precisión0,01; HTML preparado para las cuatro clases documentales |

La primera secuencia consumida por el intento fallido no se reutilizó. Los códigos no dependen
entre sí ni se renumeran para ocultar huecos técnicos. No se emitió CAE ni se llamó a ARCA.

## Interfaz y límites de evidencia

Navegador real: arranque de Home/cinta, selección de Cliente, referencia temporal y cambio de
pestaña sin perderla; Descartar vuelve al listado sin crear el PRE visual. Menús de configuración
accesibles, tema claro/oscuro y ancho390px comprobados; cinta contraída y viewport restablecido.

Dos sesiones de revisión estática de la misma familia/cuenta, con lectura del diff exacto y fuente
nativa; no constituyen auditoría externa ni independencia de modelo. Hallazgos resueltos y releídos.
Controles AST/XML/JS/manifests y Gitleaks sin hallazgos. Respaldo completo previo íntegro, sin nuevo
ensayo de restauración. Recuperaciones históricas no se atribuyen a esta composición.

No se certifican PDF visual/exportación final, concurrencia, multiempresa, permisos de todos los
roles ni los circuitos completos de Compras, Stock, Administración e Informes. La prueba de Inventario
y consulta descrita sólo cubre el soporte del caso de Ventas. Aceptación del titular pendiente.
