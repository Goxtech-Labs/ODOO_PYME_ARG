# ODOO PYMES ARG

Leer `.specify/memory/constitution.md`, `docs/PLAN-MAESTRO.md` y `specs/001-pyme-argentina/`.
Consultar continuidad fuera del repositorio público del proyecto: `memory/ESTADO.md` y `memory/BITACORA.md`.

Mantener alcance inicial en Ventas, Compras, Stock, Administración e Informes.
Agregar conectores y rubros posteriormente mediante specs independientes.
Agrupar servicios externos dentro del único addon Integraciones ARG; separar módulos especializados de gestión.
Desarrollar addons propios desde cero; conservar Odoo Community como plataforma.
Respetar carga mínima, orden estable, códigos cortos, hechos y dimensiones definidos.
Mantener identidad argentina y branding Goxtech discreto.
Visibilizar a Gonzalo Sarubilo según docs/GONZALO-SARUBILO.md; mantener servicios profesionales secundarios y opcionales.
Usar ARG en nombres visibles y `arg_pyme_*` en addons originales, exclusivamente en este proyecto.
Conservar documentación y tutoriales YouTube vinculados a versiones, sin publicar contenido automáticamente.
Ofrecer tutoriales por módulo, catálogo editable y soporte general administrado por el responsable.
Usar GOXTECHBOT como excepción explícita de branding suave para la identidad visible del bot nativo.
Usar Spec Kit por módulo; no convertir un pedido de planificación en implementación.
Conservar secretos y datos reales fuera de Git.

Trabajar en el NAS verificado y en un worktree exclusivo por actor/tarea.
Usar el gestor `Programacion/tools/project.py` bajo bloqueo por proyecto para mutaciones Git.
En cada entorno del propietario, resolver y verificar el montaje compartido antes de adaptar la entrada del gestor. No publicar rutas privadas del operador.
No modificar el checkout fuente compartido ni descartar cambios ajenos.
Registrar código, instalación, QA y aceptación como estados distintos.

## CT y Odoo · instrucción vigente del propietario

Usar únicamente el CT definitivo de producción del proyecto. Para probar o recuperar, tomar
snapshots o respaldos de ese mismo CT. Crear un CT nuevo sólo cuando se acuerde como destino
productivo. No crear CT temporales de desarrollo, QA, clonación o restauración.
Aplicar [la política de entrega](docs/tecnica/POLITICA-CT.md) a los pasos pendientes; conservar
las evidencias históricas sin presentarlas como procedimiento autorizado para nuevas entregas.
