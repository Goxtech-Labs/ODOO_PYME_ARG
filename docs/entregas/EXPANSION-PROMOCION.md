# Expansión ARG · Promoción técnica a la demo

2026-11-06. Instalados Valores20.0.1.2.0, Reparaciones20.0.1.2.0,
Administración20.0.1.1.4 y Compras20.0.1.0.6. [Lock instalado](../../composition/versions.lock.json)
y [antecedente aislado](EXPANSION-INSTALACION-AISLADA.md).

## Recuperación y actualización

Se detuvo el acceso público, Odoo y PostgreSQL para conservar un punto consistente. Se tomó
snapshot y respaldo completo de la instancia, incluyendo DB, adjuntos, configuración y fuentes.
Integridad zstd/SHA256 comprobada. El respaldo se restauró en una nueva copia sin red ni arranque
automático; los servicios externos se bloquearon antes del primer inicio. No se sustituyó el entorno
de desarrollo existente.

En la copia recuperada se contrastaron101 módulos,231 fuentes,17 referencias de adjuntos con sus
checksums, conteos operativos y metadatos seleccionados. Se desactivaron cron/correo sólo en esa
copia y se instalaron los dos addons nuevos, actualizando Administración y Compras. Registro,
vistas combinadas/procesadas, versiones y arranque comprobados:103 módulos y285 fuentes.
No fue una instalación vacía de todo Odoo ni una prueba de los circuitos de negocio.

La demo recibió el mismo paquete inmutable, con cron temporalmente suspendido. Tras los controles
se repuso su configuración original y se iniciaron Odoo, PostgreSQL y túnel público. La copia de
recuperación quedó apagada. No se restauró una base antigua sobre nuevas transacciones.

## Lectura posterior

- SHA256 del paquete: `0adad0325df983bee917325f334f452a066555b272dfc71428cb30fd3a5f2f76`;285 fuentes coinciden.
- 103 módulos:14 ARG y89 nativos/dependencias. Los nativos, incluido POS, conservan sus versiones.
- Conteos de ocho modelos operativos y hashes de metadatos seleccionados de usuarios/compañía iguales.
- Mapas de activación de cron/correo iguales a los anteriores; no se activaron conectores.
- Reparaciones:9 estados y14 clases de hechos; Valores:14 estados. Vista Compras combinada y procesada.
- Odoo/PostgreSQL/túnel activos; acceso público a `/web/login` HTTP200 y formulario presente.

Los conteos/hashes tienen el alcance indicado; no prueban la integridad semántica completa de los datos.
Las constancias operativas protegidas quedan fuera del repositorio público. No se publican respaldos,
configuraciones con credenciales ni logs crudos.

## Límites y siguientes entregas

Código desplegado, QA pendiente. No se ejecutaron recorridos funcionales/financieros, revisión visual,
PDF ni aceptación. No se emitieron comprobantes fiscales ni mensajes o transacciones bancarias.
Los ejemplos nuevos de Reparaciones siguen en el entorno aislado, sin copiar operaciones a la demo.
Las revisiones estáticas independientes usan otra sesión de la misma familia/cuenta; no son una auditoría externa.

Compras016T006 y promoción018T014 quedan realizadas como entrega técnica. Reparaciones018T012
conserva ejemplos de circuito/tutoriales pendientes;016T015 sigue abierta. Valores017 conserva la
cartera ampliada pendiente. El objetivo completo de22 capacidades, E1,019–024 e Integraciones continúa.
