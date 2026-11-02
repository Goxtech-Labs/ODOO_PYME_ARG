# Portada y comunidad ARG — 2026-11-01

Estado: documentación implementada; publicación remota y aceptación pendientes.
Portada navegable con identidad argentina, cuatro botones SVG originales, manuales, instalación,
roadmap, contribución y propuesta. Autoría de Gonzalo Sarubilo visible con GoxtechLabs secundario.

Catálogo editorial por tarea/versión con manual alternativo, guion y miniatura del primer episodio
preparados. No se grabó ni publicó un video; canal real pendiente de configuración.
Licencias adoptadas expresamente por el titular: AGPL-3.0 para addons propios y CC BY-SA 4.0 para
documentación/recursos originales. Textos completos en raíz y en cada addon; excepciones en NOTICE.

Incluye perfil de servicios sin Stock, ejemplo conciliable de hechos/dimensiones, personalización
visual y exportación abierta. El perfil técnico mínimo de servicios se instaló en una base aislada:
74 módulos, sin stock.move, cero documentos de negocio, cron y correo desactivados. No se ejecutó
el cargador completo allí ni recorridos de QA.

Los controles documentales verifican enlaces, estructura, cobertura, IDs y dependencias; no son
aceptación del producto. Cargador de ejemplos revisado en lectura independiente tras cerrar guards
de documentos archivados, compañía única y localización preinstalada. No se ejecutó contra la demo.
El registro consolidado está en [controles técnicos](CONTROLES-TECNICOS.md).

No se activó GitHub Pages, no se publicaron destinos ficticios y no se enviaron mensajes externos.
[Release](RELEASE.md) registra el artefacto exacto y los hitos pendientes.

## Composición instalada

Paquete de 183 archivos, SHA256 `bedafa980e91fa4583965c3966c09d9aa8160918f7e704cb24000ee4d8ea55a8`.
Catálogo 20.0.1.0.5 actualizado en entorno aislado y demo. Ventas/Compras acceden al mismo
maestro mediante la misma acción, sin duplicar productos; los demás addons conservan versión.
Los 183 hashes fuente/paquete/runtime coinciden. Home, login, ayuda y soporte HTTP 200, sin
error JS. Cron/correo desactivados, cero documentos/asientos/pagos/movimientos de negocio.
Gitleaks del árbol público y paquete sin hallazgos;11 hashes de Spec Kit original conservados.
Revisiones independientes de fuente/documentos cerradas, misma familia/cuenta.

## Recuperación de esta composición

Respaldo completo consistente con Odoo detenido, integridad zstd y SHA256
`dc2d93ac0b8ad5a7c04008cf59ac09f08db5361a1e04a0e613d2f40707c9a51b`.
Restaurado en un contenedor nuevo sin interfaz de red, con túnel bloqueado y cron/correo desactivados.
Se recuperaron 91 módulos, los 183 archivos de código del paquete y 78/78 adjuntos con checksum
correcto; login local HTTP 200. Cero operaciones de negocio. El contenedor de restauración quedó
apagado. La prueba acredita recuperación técnica de esta demo; QA de circuitos permanece pendiente.
