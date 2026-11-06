# Reparaciones ARG1.1 · Trabajo autorizado

**Estado actual2026-11-06:** el código de este incremento y sus ampliaciones indicadas en la
[entrega0.1.6-dev](EXPANSION-PROMOCION.md) está instalado en demo. Las referencias siguientes a
instalación/promoción pendiente describen el antecedente histórico, no el estado vigente.
QA funcional/visual, PDF, ejemplos de circuito y aceptación siguen pendientes.

Actualización2026-11-06: trabajo1.1 y correcciones1.2 instalados y registrados en aislado;
la demo compartida conserva su composición anterior. [Controles actuales](EXPANSION-INSTALACION-AISLADA.md).

Antecedente2026-11-05: fuente20.0.1.1.0 preparada, entonces sin instalación por acceso SSH.
Revisión funcional, visual, PDF y aceptación no ejecutadas.

## Alcance desarrollado

REP mantiene equipo ajeno/custodia. Desde diagnóstico prepara PRE y conserva revisiones; PED
se genera por el circuito comercial existente. Cada PED conserva una autorización explícita con
fecha/persona/constancia/cobertura y condiciones. Confirmar pedido e iniciar trabajo son pasos separados.

Repuestos usan los movimientos nativos del PED, sin otra salida interna. La ejecución exige trabajo
en curso; devoluciones conservan origen y actualizan cantidades. PTM registra servicios manuales,
horas sólo si su unidad es hora; confirma/revierte cumplimiento nativo con evidencia, sin factura extra.
Listo/retomar/entregar verifican alcance, pendientes y retiro. Facturas/REC permanecen en sus motores.

Ejes de PRE disponibles aun antes del primer PED; después agrega hechos por pedido/unidad/moneda,
sin sumar dinero entre órdenes. Reversión de trabajo posterior conserva la entrega física histórica.
Partes y solicitudes conservan identidad y claves estables, sin reejecutar diálogos anteriores.

## Controles de fuente

Revisión independiente de otra sesión, misma familia/cuenta: corregidas vías para marcar repuestos
cumplidos mediante valores/defaults, limitar controles con un corte histórico, y omitir ejes PRE sin PED.
La fuente actual usa movimientos terminados actuales, comprueba todos los IDs nativos relacionados
con permisos/compañía, y protege cantidades/método/naturaleza de líneas. No es auditoría externa.

Migración1.0→1.1 conserva eventos, asigna claves legacy y sustituye su unicidad; registra PTM y
marca guía previa para revisar sin sobrescribir enlaces/textos del titular. Migración no ejecutada.
AST/XML/JS/manifests, operaciones ACL, XPaths de padres propios y secretos se controlan por paquete;
estos controles no prueban instalación, permisos efectivos, PDF ni funcionamiento físico/financiero.

Paquete281 archivos SHA256f39a34bd49339ea142745e1186acc9f67ae1e792b9cdd895cef203961dfeb22b.
[Composición candidata](../../composition/candidates/018-reparaciones-trabajo.json), sin reemplazar
el lock instalado. OPA1.2 y el primer paquete de Reparaciones1.0 deben instalarse/controlarse en
aislado antes de actualizar1.1, para comprobar la secuencia de entrega/migración prevista.

Dos cargadores optativos: el anterior crea cliente/REP borrador; seed_repair_work_demo.py prepara
repuesto almacenable y servicio horario, sin stock, PRE/PED/PTM/facturas/pagos ni mensajes. No se
afirma existencia disponible ni se ajusta stock silenciosamente para facilitar una demostración.

Pendientes: instalación/lectura técnica, promoción con respaldo fresco, correcciones explícitas de
recepción/diagnóstico, reportes completos, ejemplos operativos y tutoriales; QA posterior. El objetivo
completo incluye todas las22 capacidades y no se reduce a este módulo.

[Contrato](../../specs/018-reparaciones/contracts/trabajo-autorizado.md) ·
[Manual](../usuario/018-reparaciones.md) · [Tareas](../../specs/018-reparaciones/tasks.md)

Ampliación posterior: [correcciones y visitas1.2](018-correcciones-visitas.md). Esta entrada conserva
el paquete de trabajo1.1; ninguna versión de Reparaciones se instaló aún en la demo.
