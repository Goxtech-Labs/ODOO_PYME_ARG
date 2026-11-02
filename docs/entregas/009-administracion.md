# Administración ARG — entrega20.0.1.1.1 — 2026-11-01

Estado: **desarrollado e instalado técnicamente en demo y entorno aislado; QA funcional/visual y aceptación pendientes**.
Incluye cuentas corrientes, REC/OPA, anticipos, aplicaciones/desaplicaciones, reversión, caja y atribución
de dinero. No se ejecutaron operaciones de negocio para comprobar esta entrega.

## Composición y alcance

Administración20.0.1.1.1, Documentos20.0.1.0.4, Ventas20.0.1.0.3 y Compras20.0.1.0.2.
Los demás addons conservan la versión de composition/versions.lock.json.90módulos:79nativos/dependencias y11ARG.
145archivos fuente/artefacto/runtime coinciden por SHA256. Composición `e67584850e82eb8835d772d8a7a679447e519197781036a6bd9df2292f106e55`.
Destino demo arg_demo, https://pymes.goxtechlabs.com.ar. Fuente sin commit/push.

REC/OPA agrupa medios y pagos nativos con identidad propia. No hay libro paralelo de saldos.
Roles separan preparación/consulta de confirmación/reversión. Eventos inmutables conservan aplicación
y desaplicación; claves y conjuntos objetivo estables evitan repetir efectos o borrar aplicaciones nuevas.
Cuentas corrientes conservan granularidad apunte/cuota. Caja usa liquidez publicada; pagos transitorios
se consultan aparte. FAC/FRC y PED/PPC distinguen deuda de dinero, con No determinado cuando falta evidencia.
Ver [guía de usuario](../usuario/009-administracion.md) y [contrato técnico](../tecnica/009-administracion.md).

## Controles técnicos realizados

- AST Python, XML, sintaxis JS, manifests/dependencias/rutas/recursos; paquete determinista y Gitleaks sin hallazgos en addons y ops.
- Upgrade exacto de cuatro addons en entorno aislado aislado sin red y demo; sin-uall.
- Instalación limpia de cuatro raíces y sus86dependencias en arg_install_009_utf8, entorno aislado sin red. Los puentes opcionales no forman parte de ese ensayo limpio; sí están en la composición90del upgrade.
- Primer intento limpio falló por plantilla PostgreSQL SQL_ASCII; se conservó arg_install_009 y se creó otra base con template0/UTF8/localeC. No se alteró arg_demo para resolverlo.
- Arranque Chromium autenticado: Home, cuatro listas, formularios REC/OPA sin guardar y tres vistas de wizard compiladas; cero erroresJS/diálogos. Ayuda/soporte200; una guía financiera vigente y anterior reemplazada.
- Lectura efectiva de22acciones: listas antes de formas, cero discrepancias.
- Fuente/runtime145hashes iguales; servicios Odoo/túnel activos. Cero presupuestos/pedidos/inventarios/pickings/movimientos/quants/facturas/asientos/pagos/REC/OPA/parciales/eventos. Cron/correo0activos.

Ejemplos maestros: Caja de ejemplo ARG y Banco de ejemplo ARG, medios manuales y cuentas transitorias;
predeterminados de compañía configurados. No hay datos fiscales reales, credenciales bancarias ni dinero registrado.
La base limpia técnica también mantiene cron/correo inactivos y cero documentos financieros/asientos.

Revisión independiente estática por dos sesiones Codex de la misma familia/cuenta; sin independencia de modelo.
Hallazgos de concurrencia, RPC/defaults, contexto de compañía, reversión, reintentos de desaplicación,
atribución EPD, ACL y ayuda corregidos y releídos. No acredita QA contable ni cobertura funcional.
Escenarios de quickstart siguen reservados para revisión posterior con el usuario.

## Recuperación y continuidad

Snapshot `punto de recuperación previo de la entrega`. Backup consistente con Odoo detenido:
`respaldo privado de la entrega`, 1328371646bytes, SHA256 `8b6e9e3abfa9fd6534bcd5332a24d1f0f5b166b6f1551dd5f8eaee473a2579d5`; integridad zstd correcta.
Este respaldo nuevo no fue restaurado; baseline inicial sí restaurado en entorno aislado sin red, con69adjuntos verificados.
No restaurar una base anterior automáticamente si hay escrituras posteriores.
Evidencia sanitizada: registro técnico privado de la entrega fuera del repositorio público.

Sigue Informes010 y portada/documentación011; integraciones y rubros son posteriores al núcleo.
El objetivo completo sigue activo; no se declara aceptación ni publicación.
