# F15 · reposición ARG — desarrollo en curso

**Estado: fuente parcial, sin paquete ni instalación de F15.** La entrega instalada continúa
en [0.1.9](RELEASE.md), composición fijada y Stock 20.0.1.1.1. No confundir archivos WIP con el
contenido del paquete instalado. La versión de Stock se incrementará al ensamblar la entrega.

## Fuente actual

- Diseño US6/US7 y [contrato](../../specs/008-stock/contracts/reposicion.md), compra y fabricación
  conservadas en el alcance. [Matriz de mutadores](../../specs/008-stock/contracts/reposicion-mutadores.md)
  con conflictos y cobertura pendiente; no acredita hooks implementados.
- Fundación de evidencia privada: UUID/payload canónicos, referencias autorizadas del solicitante
  actual e inmutabilidad. Falta integrarla a propuesta, confirmación y replay.
- Configuración básica sobre reglas nativas: mínimos/máximos finitos, producto/depósito/ubicación
  compatibles, nuevas manuales y conservación de modalidad existente. Token para no sobrescribir
  una edición posterior y reutilización de configuración idéntica visible.
- Acción y ficha ARG: límites visibles con unidad, ruta/presentación plegadas, selectores de treinta
  resultados, buffer preservado al elegir, filtros aplicados separados de filtros en edición y
  guardas al descartar/salir. Ficha Odoo abre únicamente el formulario estándar de esa regla.
- Simulación de limpiezas nativas al quitar ruta; validación del múltiplo resultante después de las
  inversas y antes de devolver éxito. Guardar no llama abastecimiento ni scheduler.

Los selectores específicos de proveedor/BOM, horizonte y la propuesta de físico/previsto/pipeline
siguen pendientes. T023/T024 continúan abiertas; no declarar US6/F15 completos por esta ficha.
T025–T035 y parent016T009 permanecen abiertos. La fundación no completa T026.

## Controles y fases separadas

Controles de fuente: sintaxis Python/JS/XML y rutas de manifest; revisión independiente del diff y
escaneo de secretos con evidencia operativa fuera de Git. La revisión utiliza otra sesión de la
misma familia/cuenta; no es una auditoría externa ni prueba del comportamiento instalado.

Pendiente de F15: configuración avanzada completa, propuesta/huella/grafo, frontera global,
adaptadores compra/MRP, ejecución/replay, interfaz de revisión/resultados, manual/tutorial final,
paquete con nueva versión, instalación aislada compra+MRP, respaldo fresco restaurado, promoción
del mismo paquete y publicación en main. MRP sigue opcional por instalación y obligatorio para
acreditar la entrega completa prevista; no reducir a compra.

QA funcional, concurrencia, visual, PDF y aceptación se reservan para la fase posterior acordada.
La composición actual y datos de la demo no se modifican durante este incremento de fuentes.
