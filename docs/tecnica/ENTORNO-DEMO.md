# Entorno de ejemplo y compatibilidad

Composición inicial: Odoo20.0.20261101 Community, PostgreSQL16.15, Python3.12 y Ubuntu24.04.
Doce addons ARG instalados técnicamente con sus dependencias nativas; composición exacta en
[versions.lock.json](../../composition/versions.lock.json). QA funcional/visual y aceptación pendientes.

La demo contiene compañía, tres terceros, tres productos/servicios y maestros de caja/banco ficticios.
No contiene operaciones de venta, compra, stock o dinero publicadas. Cron y correo permanecen inactivos;
no hay conexión fiscal ni mensajería habilitada. La creación de maestros no acredita validación de circuitos.

La infraestructura, credenciales, direcciones internas y respaldos del operador se registran fuera del
repositorio público. No se distribuyen cuentas compartidas para la demo. Para tu propia instalación,
elegí servidor/homelab/VPS, dominio y acceso bajo tu control; ningún túnel específico es obligatorio.

[Instalación propia](../site/INSTALACION.md) · [Operación y recuperación](OPERACION-Y-RECUPERACION.md)
· [Estado por módulo](../ESTADO-MODULOS.md) · [Release](../entregas/RELEASE.md).
