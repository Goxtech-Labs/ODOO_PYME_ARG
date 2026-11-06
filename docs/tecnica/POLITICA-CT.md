# CT definitivo del proyecto

Instrucción del propietario del 6 de noviembre de 2026, aplicable desde esta decisión:

> Usar únicamente el CT definitivo de producción del proyecto. Para probar o recuperar, tomar
> snapshots o respaldos del mismo CT. Crear un CT nuevo sólo cuando se acuerde como destino
> productivo. No crear CT temporales de desarrollo, QA, clonación o restauración.

La entrega pendiente utiliza el CT productivo ya inventariado en el
[entorno del proyecto](ENTORNO-DEMO.md). No usar otros CT existentes como staging ni crear copias
para ensayos. Las restauraciones aisladas de entregas anteriores son evidencia histórica; esta
decisión no autoriza repetirlas, convertirlas en nuevos destinos ni borrar las copias existentes.

Antes de actualizar, fijar revisión/paquete y comprobar composición, espacio y cobertura de datos.
Tomar respaldo consistente del mismo CT, incluida base, adjuntos, configuración y revisiones.
Verificar integridad del respaldo y registrar un snapshot del mismo CT cuando esté soportado,
con sus límites de cobertura. Conservar código y datos necesarios para recuperación.

Instalar y comprobar módulos, registry, vistas, versión activa, servicio y HTTP en el CT definitivo.
La revisión de código y controles de fuente se mantienen en el workspace del proyecto. QA
funcional/visual continúa en la fase posterior acordada, con datos de ejemplo y respaldos del
mismo CT. No crear infraestructura temporal para cumplir un gate anterior de staging.

Restaurar es una operación de recuperación del mismo destino; no sobrescribir datos activos para
simular una prueba de restauración ni perder transacciones posteriores. Ante un fallo, determinar
el alcance y aplicar la recuperación autorizada con su evidencia. No confundir verificación de
integridad del archivo con una restauración ejecutada.

Actualizar los pasos futuros que exigían CT aislados. Conservar fechas y resultados históricos sin
reescribirlos: documentan lo realizado bajo la política anterior, no un permiso vigente.
