# Estado de módulos ARG

2026-11-06. Demo compartida:103 módulos,89 nativos/dependencias y14 ARG. Entorno aislado:103 módulos,
89 nativos/dependencias y14 ARG. Código, instalación, QA y aceptación son hitos distintos.

| Feature | Spec/plan/tareas | Código ARG | QA funcional |
| --- | --- | --- | --- |
| 002-base-arg | Preparados | Desarrollado e instalado demo | Pendiente |
| 003-experiencia-documental | Preparados | Desarrollado e instalado demo | Pendiente |
| 004-terceros | Preparados | Desarrollado e instalado demo | Pendiente |
| 005-catalogo | Preparados | Base, variantes y precio/condiciones1.2 instalados en demo | Pendiente |
| 006-ventas | Preparados | Comercial, puente Stock y dinero aplicado desplegados demo | Pendiente |
| 007-compras | Preparados | Comercial/Stock/dinero en demo; carga1.0.6 instalada en demo | Pendiente |
| 008-stock | Preparados | Desarrollado e instalado demo, con ambos puentes | Pendiente |
| 009-administracion | Preparados | Cuentas, REC/OPA, aplicaciones y caja instalados demo | Pendiente |
| 010-informes | Preparados | Desarrollado e instalado demo | Pendiente |
| 011-web-comunidad | Preparados | Documentación y portada publicadas; integración a main registrada en [PR #1](https://github.com/Goxtech-Labs/ODOO_PYME_ARG/pull/1) | Pendiente |
| 012-integraciones | Preparados | Pendiente | Pendiente |
| 013-arca | Preparados | Pendiente | Pendiente |
| 014-rubros | Preparados | Pendiente | Pendiente |
| 015-documentos | Preparados | Desarrollado e instalado demo | Pendiente |
| 017-cartera-valores | Preparados | REC/OPA y operaciones papel1.2 instaladas en demo; cartera ampliada pendiente | Pendiente |
| 018-reparaciones | Preparados | Circuito, correcciones, nuevas visitas y reporte1.2 instalados en demo | Pendiente |

Integraciones y rubros son etapas posteriores. Las tareas generales resumen el producto y no se suman como entregas duplicadas a las tareas de módulo.

Referencia histórica de0.1.2: Base20.0.1.0.4 e Interfaz20.0.1.0.2 incorporan los [canales oficiales Goxtech](comunidad/CONTACTO.md),
configurados en demo. [Controles y límites de0.1.2-dev](entregas/CANALES-GOXTECH.md).

## Expansión activa

El [plan completo](PLAN-EXPANSION-ARG.md) incorpora22 capacidades y specs016–024. [Entrega0.1.6-dev](entregas/EXPANSION-PROMOCION.md)
instala la ampliación de Valores/Reparaciones y carga de Compras. Valores ARG incorpora REC de cheque papel, depósito, acreditación completa y rechazo en demo;
las operaciones ampliadas de cartera y las especializaciones continúan por entregas. Reparaciones
ya tiene código instalado en demo; las otras especializaciones siguen pendientes de código.
[Controles técnicos](entregas/CARGA-BASICA-ARG.md); revisión funcional/visual y aceptación separadas.
El POS nativo está instalado, pero su adaptación ARG es una tarea distinta; no contarlo como addon ARG nuevo.

[Alcance de REC/cheques](entregas/017-rec-cheques.md) y [OPA](entregas/017-opa-cheques.md):
instalados en demo, con cartera ampliada pendiente. El lock registra el paquete realmente instalado.

[Instalación técnica aislada](entregas/EXPANSION-INSTALACION-AISLADA.md): OPA/Valores1.2,
Reparaciones1.2 y Compras1.0.6 registrados, con fuentes y controles por etapa. Incluye REP borrador
y catálogo ficticios, sin efectos operativos. [Promoción técnica completada](entregas/EXPANSION-PROMOCION.md); ejemplos de circuito, tutoriales, QA y aceptación pendientes.

[Variantes de Catálogo1.1 / Stock1.0.6](entregas/005-variantes.md): instalación aislada con paquete290
archivos, promovida a demo; QA pendiente. F19 se entregó posteriormente en Catálogo1.2; F17/F22 ampliados siguen pendientes.

[Precio y condiciones1.2](entregas/005-precio-condiciones.md): instalado técnicamente en aislado y demo,
con propuesta de cliente y explicación recalculada sin modificar historia.
QA funcional/visual y aceptación pendientes.
