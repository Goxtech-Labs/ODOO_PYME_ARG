# Registro de entregas de la expansión ARG

Este índice sigue la implementación del [plan completo](../PLAN-EXPANSION-ARG.md). Código,
instalación, ejemplos, publicación, QA y aceptación son hitos distintos; los controles técnicos
seleccionados no acreditan los recorridos de usuario. No cierra las22 capacidades por un incremento.

| Entrega | Alcance | Estado técnico | Pendientes |
| --- | --- | --- | --- |
| [0.1.6-dev](EXPANSION-PROMOCION.md) | Valores, Reparaciones y carga básica de Compras | Instalada en demo, composición fijada y recuperación comprobada | Cartera ampliada, ejemplos de circuito, QA y aceptación |
| [0.1.7-dev](005-variantes.md) | Variantes F13 y cantidades opcionales de Stock | Instalada en aislado y demo; ejemplos de maestros, fuente publicada | QA, impresión, aceptación y ampliaciones F17/F22 |
| [0.1.8-dev / Catálogo1.2.0](005-precio-condiciones.md) | Consulta y explicación de precio/condiciones F19 | Instalado en aislado y demo con paquete294, recuperación comprobada | QA y aceptación |
| [0.1.9-dev / Stock1.1.1](008-trazabilidad.md) | Series/lotes F14 y alta mínima | Instalada en aislado/demo con paquete299 y recuperación comprobada | F15/reposición, QA y aceptación |

La [composición de demo](../../composition/versions.lock.json) identifica la entrega instalada;
las [tareas coordinadoras](../../specs/016-expansion-argentina/tasks.md) conservan el trabajo restante
y las especificaciones de cada módulo. Integraciones ARG mantiene proveedores externos en un único
addon, sin activar canales ni operaciones reales por una instalación.
