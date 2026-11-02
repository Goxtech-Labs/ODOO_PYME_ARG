# Instalación técnica del entorno de ejemplo

Odoo20 Community nativo y PostgreSQL16 con base de ejemplo UTF-8. Los secretos y la infraestructura
concreta del operador se conservan fuera del repositorio público. La instalación funciona con recursos
propios; HTTPS/proxy del propietario y la gestión local no requieren contratar servicios Goxtech.

La demo contiene maestros ficticios, sin CUIT real, ni documentos publicados o movimientos de negocio.
Base, interfaz, maestros, cinco circuitos y puentes físicos están instalados técnicamente. Los controles
por módulo constan en [CONTROLES-TECNICOS.md](CONTROLES-TECNICOS.md).

Se restauró el respaldo inicial en un entorno aislado sin red;69adjuntos y maestros verificados, HTTP200.
Los respaldos incrementales posteriores tuvieron integridad verificada; eso no equivale a restauración
completa de cada uno. El registro operativo conserva nombres/hashes y condiciones de cada recuperación.
No restaurar automáticamente datos anteriores si hubo operaciones nuevas.

QA funcional/visual y aceptación siguen pendientes. [Instalación bajo tu control](../site/INSTALACION.md)
y [operación/recuperación](../tecnica/OPERACION-Y-RECUPERACION.md).
