# Perfil de ejemplo: gestión de servicios sin Stock

Este perfil usa Base/UI, Terceros, Catálogo, Documentos, Ventas, Compras, Administración e Informes.
No instala arg_pyme_stock ni sus puentes. La instalación técnica limpia del perfil se comprobó sin
stock.move ni stock.move.line, con cero documentos comerciales/contables. No acredita QA funcional.

Para una base nueva y aislada, inicializar las raíces:

```text
arg_pyme_ventas,arg_pyme_compras,arg_pyme_administracion,arg_pyme_informes
```

Usar el mismo comando de instalación de la guía cambiando DB e init explícitamente; UTF-8 y sin demo nativa.
El cargador seed_demo.py es de la demo completa con Stock y no se ejecuta en este perfil.
No se pide ni se crea un depósito. Un producto de tipo Servicio no exige remito ni lote.

## Maestros y recorrido previsto para revisión posterior

- Compañía: Ejemplo — Servicios ARG; moneda ARS, sin identidad fiscal real.
- Cliente: Ejemplo — Cliente Servicios; rol Cliente, sin CUIT inventado.
- Servicio: EJ-SERV-01, Ejemplo — Asistencia técnica; unidad Unidad; precio ficticio$15.000 sin impuestos en este ejemplo.
- PRE: dos prestaciones; aceptación y generación de PED son acciones separadas.
- Entrega física: No corresponde. Facturación y cobro conservan sus ejes independientes.
- REC: puede cobrar parte de la deuda o quedar como anticipo; sólo confirma/aplica el responsable.

Catálogo es un maestro compartido, accesible desde los circuitos comerciales. Tener productos/servicios
no implica un libro de stock. Una factura o un recibo no crean movimientos físicos en este perfil.
Los ejemplos describen el comportamiento a revisar; no se ejecutaron como transacciones de la instalación técnica.
