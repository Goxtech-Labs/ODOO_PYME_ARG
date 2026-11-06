# Odoo Pymes ARG — 0.1.6-dev

Expansión desplegada en la demo el 2026-11-06: Valores1.2, Reparaciones1.2,
Administración1.1.4 y Compras1.0.6. [Alcance y controles](EXPANSION-PROMOCION.md).

103 módulos:14 ARG y89 nativos/dependencias;285 archivos propios del paquete SHA256
`0adad0325df983bee917325f334f452a066555b272dfc71428cb30fd3a5f2f76`.
[Composición instalada](../../composition/versions.lock.json). Se conservaron los módulos nativos,
incluido POS, y los conteos de documentos, metadatos seleccionados de usuarios/compañía y configuración de cron/correo.

REC/OPA con cheques en papel, reservas y operaciones descritas en sus contratos están instalados.
La cartera ampliada —ECHEQ, negociación, parciales y demás pendientes017— continúa en desarrollo.
Reparaciones incluye recepción, diagnóstico, PRE/PED, autorización, repuestos, PTM, correcciones,
nuevas visitas y reporte; Compras incorpora fecha de proveedor antes de tercero y referencia.

Respaldo completo fresco y snapshot; restauración y registro/instalación en copia sin red comprobados
antes de actualizar la demo. Servicio y formulario de acceso HTTP200. No se ejecutaron recorridos de
negocio, QA financiera/visual, renderizado PDF ni operaciones externas. Los ejemplos nuevos de
Reparaciones permanecen en aislado; no se copiaron transacciones de esa base.

QA, tutoriales reales y aceptación pendientes. Este incremento no completa las22 capacidades,
E1, specs017–024 ni Integraciones. [Entrega anterior](RELEASE-0.1.5-dev.md).

Originales AGPL-3.0-only/CC BY-SA4.0; atribuciones de Odoo y terceros conservadas.
