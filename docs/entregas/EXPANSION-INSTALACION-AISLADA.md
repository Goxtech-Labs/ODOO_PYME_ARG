# Expansión ARG · Instalación técnica aislada

2026-11-06. Los incrementos se instalaron primero en el entorno aislado. Posteriormente se completó
la [promoción técnica a la demo0.1.6-dev](EXPANSION-PROMOCION.md); el [lock](../../composition/versions.lock.json) registra esa entrega.

| Componente | Versión aislada | Evidencia técnica |
| --- | --- | --- |
| Administración | 20.0.1.1.4 | Registro y actualización junto con Valores |
| Valores | 20.0.1.2.0 | 14 estados, CHQ/PAG, defaults, vistas y guías registrados |
| Reparaciones | 20.0.1.2.0 | 9 estados, 14 hechos, REP/PTM, asistentes, ACL y restricciones registrados |
| Compras | 20.0.1.0.6 | Vista combinada y procesada: fecha de proveedor antes de tercero/referencia |

La [composición aislada](../../composition/environments/isolated-development.json) tiene103 módulos:
14 ARG y89 nativos/dependencias. El paquete de285 archivos coincide íntegramente con los hashes de
la lectura posterior, SHA256 `0adad0325df983bee917325f334f452a066555b272dfc71428cb30fd3a5f2f76`.

Se aplicaron OPA1.2, recepción1.0, trabajo1.1, correcciones1.2 y carga de Compras1.0.6 en orden,
con snapshot y lectura técnica por etapa. Odoo quedó activo; túnel público inactivo, sin interfaces
externas, cron/correo activos0 y arranque automático deshabilitado. En esta etapa aislada no se copió información al entorno compartido. La promoción posterior actualizó código, sin copiar transacciones.

Los controles verificaron registro, defaults, versiones, restricciones, guías, fuentes y servicio.
La ficha contable combinada tiene233 nodos de campo en esta composición. La fuente nativa de esa
vista coincide con la revisión inspeccionada; esto no acredita igualdad de todo el core ni revisión visual.
No se ejecutaron recorridos de negocio, pruebas financieras, envíos, emisión fiscal ni renderizado PDF.

## Ejemplos cargados

Con compañía marcada como demo, selección explícita y snapshot, los cargadores optativos crearon
un cliente ficticio, `REP-000001` en borrador, un repuesto y un servicio horario identificados como
EJEMPLO. No registraron recepción, diagnóstico, PTM, pedido, movimiento, factura ni pago. Los
conteos operativos protegidos por los cargadores se conservaron. No se probó un segundo replay.
Se mantienen los ejemplos anteriores del entorno; no se presenta existencia física inventada.

## Pendientes

La promoción a la demo compartida se completó con respaldo fresco y recuperación comprobada,
conservando sus usuarios y configuración. QA funcional/visual, PDF, tutoriales
reales y aceptación son fases posteriores. La instalación de estos incrementos no completa la cartera
argentina ampliada, las22 capacidades, E1 ni las especializaciones019–024 e Integraciones.
