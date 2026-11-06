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
- Opciones de proveedor/condición en Compras–Stock ARG y BOM normal en el puente opcional
  Stock–Fabricación ARG. Dominios de plantilla/variante/compañía y etiquetas con dimensiones
  autorizadas, sin precios; cambiar producto permite quitar o sustituir una opción incompatible.
- Horizonte nativo de compañía, visible plegado y editable por separado con permiso nativo de
  compañía/campo, token y aviso de alcance global. Reconsultar muestra el valor actual y conserva
  el borrador. No se crea un horizonte por producto ni se escribe al guardar su regla.

T022/T024 completas como fuente, todavía sin instalar. T023 y la propuesta de físico/previsto/
pipeline siguen pendientes; no declarar US6/F15 completos por esta ficha. T025–T035 y parent016T009
permanecen abiertos. La fundación no completa T026. Los selectores de los puentes no completan la
captura y ejecución previstas en T028/T029.

## Controles y fases separadas

Controles de fuente: sintaxis Python/JS/XML y rutas de manifest; revisión independiente del diff y
escaneo de secretos con evidencia operativa fuera de Git. La revisión utiliza otra sesión de la
misma familia/cuenta; no es una auditoría externa ni prueba del comportamiento instalado.

Pendiente de F15: propuesta/huella/grafo, frontera global,
adaptadores compra/MRP, ejecución/replay, interfaz de revisión/resultados, manual/tutorial final,
paquete con nueva versión y composición compra+MRP, respaldo consistente/snapshot del CT definitivo,
instalación y verificación del paquete en ese mismo CT y publicación en main. No crear CT temporales
ni usar otros como staging; aplicar la [política vigente](../tecnica/POLITICA-CT.md). MRP sigue opcional por instalación y obligatorio para
acreditar la entrega completa prevista; no reducir a compra.

QA funcional, concurrencia, visual, PDF y aceptación se reservan para la fase posterior acordada.
La composición actual y datos de la demo no se modifican durante este incremento de fuentes.
