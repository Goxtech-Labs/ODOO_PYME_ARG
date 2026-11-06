# Entorno de ejemplo y compatibilidad

Odoo20.0.20261101 Community, PostgreSQL16.15, Python3.12 y Ubuntu24.04. La entrega0.1.9-dev
conserva103 módulos:14 ARG y89 nativos/dependencias, incluido POS. Stock1.1.1 incorpora series/lotes y Catálogo1.2.0 mantiene precio
y condiciones; la [composición fijada](../../composition/versions.lock.json) identifica versiones
y paquete instalado. La composición inicial de doce addons es una entrega histórica.

La demo usa datos ficticios identificados y puede ser explorada/modificada por usuarios habilitados
por el responsable. El catálogo de ejemplo no acredita ejecución de circuitos ni una base vacía.
La ejecución cron está deshabilitada por configuración (`max_cron_threads = 0`), aunque existan
registros cron activos; su configuración se conservó. Los servidores de correo observados permanecen
inactivos. No se habilitaron conexiones fiscales, bancos ni mensajería reales.
QA funcional/visual y aceptación del incremento siguen pendientes.

Infraestructura, credenciales, direcciones internas y respaldos del operador permanecen fuera del
repositorio público. Las credenciales de exploración se entregan por un canal privado; no se incluyen
en código ni manuales. Para tu instalación elegí servidor/homelab/VPS, dominio y acceso bajo tu
control; ningún túnel específico es obligatorio.

[Instalación propia](../site/INSTALACION.md) · [Operación y recuperación](OPERACION-Y-RECUPERACION.md)
· [Estado por módulo](../ESTADO-MODULOS.md) · [Release](../entregas/RELEASE.md).
