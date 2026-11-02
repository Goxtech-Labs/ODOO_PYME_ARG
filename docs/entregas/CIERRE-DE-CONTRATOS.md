# Correcciones de cierre — 0.1.1-dev

Estado: fuente corregida, revisión independiente cerrada e instalación técnica en aislado/demo completada. QA funcional/visual y aceptación pendientes.
No es QA funcional/visual, no se ejecutaron recorridos de negocio ni se crearon operaciones.

| Hallazgo concreto | Corrección de implementación |
| --- | --- |
| AJU registrado para stock.move, ajuste real en otro modelo | Registro canónico arg.pyme.inventory.adjustment; migración sólo si no hay identidades antiguas, con rechazo explicativo si existen |
| REM/ENT preparado sin eje antes del snapshot | Demanda provisional por lectura; líneas incompletas no se convierten en cantidades conocidas; snapshot permanece reservado al efecto/cancelación |
| Entrega/Recepción al final de ejes | Puentes anteponen el eje físico a facturación y dinero |
| Facturación por movimiento sin evidencia directa | Eje No determinado con razón y consulta de facturas relacionadas, sin atribuirlas a esa entrega |
| Dinero/deuda de factura compartida atribuido a cada pedido | Comprobar origen exclusivo por línea y permisos; caso ambiguo No determinado, sin prorrateo |
| Informes limita representación a doce cifras significativas | Precisión monetaria/decimal, suma antes de formatear, valores comunes HTML/PDF/CSV |
| Iconos y Acerca de pendientes en contrato visual | SVG originales con texto en controles/estados/áreas y página interna de autoría/licencias |

Versiones instaladas: Base1.0.3, UI1.0.1, Documentos1.0.5, Ventas1.0.4, Compras1.0.3,
Stock1.0.3, ambos puentes1.0.1 e Informes1.0.1, todas bajo la rama20.0. Los restantes addons
conservan versión. La composición efectiva se actualiza sólo después de instalar.

Dos revisiones de lectura, misma familia/cuenta, cerraron los hallazgos y los remanentes del diff.
No certifican cálculos con datos, concurrencia, legibilidad ni aceptación del usuario.
Evidencia operativa y recibos privados se conservan fuera del repositorio público.

## Evidencia técnica de la composición

Paquete SHA256 `b4501c7bb1befdc6fac6c77596271bae6ceb9f7320fad60fcee013902affbb2c`,
185 archivos. Las nueve versiones afectadas se actualizaron explícitamente, sin actualización
global ni cambios a core/otros clientes. 91 módulos instalados; los hashes de fuente/paquete/runtime coinciden.
AJU configurado con el modelo correcto y cero identidades previas; migración completada sin renumerar.

Ocho comprobaciones técnicas del helper numérico puro usaron el framework instalado, sin DB ni
documentos: importes grandes/negativos, precisión monetaria, cantidades 0.6/1.2 y salida CSV
numérica negativa/texto protegido. No prueban cálculos de circuitos con documentos reales.
Home, ayuda, soporte y Acerca de arrancan HTTP 200 sin error JS. Informes conserva once fuentes;
formulario y salida vacía HTML/CSV/PDF 200, sin operaciones. Sólo filtros transitorios de consulta.
Instalación mínima limpia:31 módulos, sin Contabilidad/Stock, AJU correcto y cron/correo desactivados.

Respaldo final consistente de la composición corregida, SHA256 `4cb85cbcc4ecd7d2220dbd110411bb10354002aa873aa8a16f96ac1c70ffbcc4`,
restaurado en un contenedor nuevo sin red:185 hashes de código coinciden,91 módulos y
78/78 adjuntos correctos. URL local/cron/correo normalizados antes de arrancar Odoo, túnel bloqueado.
Login local200; copia apagada. No se usó la restauración previa de 0.1.0-dev para certificar este paquete.
