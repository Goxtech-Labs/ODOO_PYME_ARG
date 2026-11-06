# Estado de módulos ARG

2026-11-05. 101 módulos instalados: 89 nativos/dependencias y 12 addons ARG (incluidos dos puentes físicos). Código, instalación, QA y aceptación son hitos distintos.

| Feature | Spec/plan/tareas | Código ARG | QA funcional |
| --- | --- | --- | --- |
| 002-base-arg | Preparados | Desarrollado e instalado demo | Pendiente |
| 003-experiencia-documental | Preparados | Desarrollado e instalado demo | Pendiente |
| 004-terceros | Preparados | Desarrollado e instalado demo | Pendiente |
| 005-catalogo | Preparados | Desarrollado e instalado demo | Pendiente |
| 006-ventas | Preparados | Comercial, puente Stock y dinero aplicado desplegados demo | Pendiente |
| 007-compras | Preparados | Comercial, puente Stock y dinero aplicado desplegados demo | Pendiente |
| 008-stock | Preparados | Desarrollado e instalado demo, con ambos puentes | Pendiente |
| 009-administracion | Preparados | Cuentas, REC/OPA, aplicaciones y caja instalados demo | Pendiente |
| 010-informes | Preparados | Desarrollado e instalado demo | Pendiente |
| 011-web-comunidad | Preparados | Documentación y portada publicadas; integración a main registrada en [PR #1](https://github.com/Goxtech-Labs/ODOO_PYME_ARG/pull/1) | Pendiente |
| 012-integraciones | Preparados | Pendiente | Pendiente |
| 013-arca | Preparados | Pendiente | Pendiente |
| 014-rubros | Preparados | Pendiente | Pendiente |
| 015-documentos | Preparados | Desarrollado e instalado demo | Pendiente |
| 017-cartera-valores | Preparados | REC con cheque papel y operaciones básicas sólo en aislado; cartera ampliada pendiente | Pendiente |
| 018-reparaciones | Preparados | Circuito, correcciones, nuevas visitas y reporte en fuente1.2; no instalado | Pendiente |

Integraciones y rubros son etapas posteriores. Las tareas generales resumen el producto y no se suman como entregas duplicadas a las tareas de módulo.

Referencia histórica de0.1.2: Base20.0.1.0.4 e Interfaz20.0.1.0.2 incorporan los [canales oficiales Goxtech](comunidad/CONTACTO.md),
configurados en demo. [Controles y límites de0.1.2-dev](entregas/CANALES-GOXTECH.md).

## Expansión activa

El [plan completo](PLAN-EXPANSION-ARG.md) incorpora22 capacidades y specs016–024. Entrega0.1.5-dev
instala sólo el primer incremento de carga básica. Valores ARG incorpora REC de cheque papel, depósito, acreditación completa y rechazo en aislado;
las operaciones ampliadas de cartera y las especializaciones continúan por entregas. Reparaciones
ya tiene código de recepción; los otros seis addons nuevos siguen pendientes de código.
[Controles técnicos](entregas/CARGA-BASICA-ARG.md); revisión funcional/visual y aceptación separadas.
El POS nativo está instalado, pero su adaptación ARG es una tarea distinta; no contarlo como addon ARG nuevo.

[Alcance de REC/cheques](entregas/017-rec-cheques.md): disponible sólo en aislado, sin habilitar aún
la cartera ampliada ni OPA con valores en la demo. La composición candidata no reemplaza el lock del entorno compartido.

Desarrollo adicional: [OPA/entregas1.2](entregas/017-opa-cheques.md) preparado en código,
pendiente de renovación SSH para instalación aislada. No reemplaza las composiciones verificadas
anteriores ni acredita QA o promoción.

[Reparaciones1.0](entregas/018-reparaciones.md): fuente de recepción/custodia y diagnóstico,
sin instalación acreditada. No habilita todavía intervenciones, repuestos ni facturación.

[Trabajo autorizado1.1](entregas/018-trabajo-autorizado.md) amplía esa fuente; ningún incremento
de Reparaciones está instalado todavía. No sumar su código como disponibilidad en la demo.

[Correcciones/visitas1.2](entregas/018-correcciones-visitas.md) completa la fuente preparada de018;
instalación, ejemplos operativos, tutoriales, QA y aceptación siguen como entregas pendientes.
