# Catálogo y dependencias ARG

Estado: doce addons propios desarrollados e instalados técnicamente en demo; QA y aceptación pendientes. Integraciones/rubros posteriores. Ver [índice y orden](INDICE.md).

| Módulo | Dependencias propias | Responsabilidad |
| --- | --- | --- |
| arg_pyme_base | — | Tipos, identidad, secuencias, roles y ayuda central |
| arg_pyme_ui | base ARG | Áreas, cinta, matrices, botones, soporte y GOXTECHBOT |
| arg_pyme_terceros | base ARG, UI | Identidad única y roles de tercero |
| arg_pyme_catalogo | base ARG, UI | Productos, servicios, unidades y listas |
| arg_pyme_documentos | base ARG, UI | Mixin de identidad/vínculos e impresión común |
| arg_pyme_ventas | base, UI, terceros, catálogo, documentos ARG | PRE propio, PED separado y derivados nativos |
| arg_pyme_compras | base, UI, terceros, catálogo, documentos ARG | PPC, entradas, factura recibida y devoluciones |
| arg_pyme_stock | base, UI, catálogo, documentos ARG | Existencias y movimientos nativos, conteo/ajuste |
| arg_pyme_administracion | base, UI, terceros, documentos ARG | REC/OPA, pagos, aplicaciones, caja y deuda |
| arg_pyme_informes | base ARG, UI | Adaptadores internos según fuentes instaladas; sin exigir todos los circuitos |
| arg_pyme_ventas_stock | ventas, stock ARG | Puente sobre sale_stock; sin segundo libro físico |
| arg_pyme_compras_stock | compras, stock ARG | Puente sobre purchase_stock; sin segundo libro físico |
| arg_pyme_valores | administración, documentos ARG | REC de cheque papel, depósito, acreditación completa y rechazo; sólo aislado, cartera ampliada pendiente |
| arg_pyme_integraciones | base ARG, UI | Único addon de todos los proveedores externos; posterior |

La columna enumera dependencias propias; las nativas exactas constan en cada plan e index.json.
ARG UI también requiere web/mail_bot; el resto usa contactos, producto, venta, compra, stock o account según su responsabilidad.
Instalar puentes nativos sale_stock/purchase_stock/stock_account sólo con composición explícita.
No crear ciclos: Documentos no depende de Ventas y Base no depende de UI.

ARCA incrementa Integraciones ARG, sin otro addon ni dependencia del addon sobre sí mismo.
Los rubros agregan addons especializados opcionales según necesidad confirmada.
Comisiones, fabricación, cursos, cartera financiera y otras capacidades avanzadas son incrementos
en desarrollo con spec propia. La ficha inicial de Valores no acredita esos efectos.
Conservar manual, tutorial, ejemplo, límites y estado por módulo; no confundir planeado/programado/instalado/QA/aceptado/publicado.

Adaptadores concretos PRE/PED pertenecen a Ventas, no a Documentos. Documentos sólo define mixin/contrato genérico; no hereda modelos consumidores ni crea ciclos.
