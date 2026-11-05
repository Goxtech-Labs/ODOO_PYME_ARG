# Investigación · Agentes y comisiones ARG

**Fecha**: 2026-11-05. Diseño, no verificación funcional.

## Decisión

Crear/extender `arg_pyme_comisiones` opcional sobre arg_pyme_ventas, arg_pyme_administracion, arg_pyme_documentos; evaluar sales_team/account; sale_commission sólo candidato, sin asumir disponibilidad o licencia.

## Razonamiento

Base explícita por facturación neta o cobro efectivo aplicado; separar comisión devengada de pagada y conservar devoluciones/rechazos. Regla inicial propuesta por facturación neta, seleccionable por compañía antes de activar. La independencia del núcleo evita imponer un rubro a todas las pymes.

## Alternativas

Copiar pantallas españolas o duplicar libros fue descartado: cambia identidad y pierde trazabilidad.
Una dependencia nativa se prefiere si su licencia/API y su interacción con hooks ARG son compatibles;
no se declara probada antes de inspección. Las funciones propias se desarrollan desde cero.

## Fuentes

Ver [investigación coordinada](../016-expansion-argentina/research.md), contratos actuales y composición.
Referencias pertinentes: FactuSOL comisiones. Políticas de cuentas, bancos y garantías se fijan con
configuración versionada; nunca usar una fuente española como normativa argentina.

## Límite de certeza

La selección de APIs/clases y dependencias mínimas se cierra al inspeccionar la versión instalada antes
de programar. Esa tarea técnica tiene salida definida; no autoriza instalar candidatos por anticipado.
