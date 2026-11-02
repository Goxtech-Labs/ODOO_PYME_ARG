# Research and decisions

Fecha: 2026-11-01. Distinguir requisitos confirmados y decisiones técnicas propuestas.

## R01 Base Community estable

**Decision**: Usar Odoo 20.0 Community, Python 3.12 y PostgreSQL 16; runtime demo instalado y registrado en composition/versions.lock.json.
**Rationale**: Fuentes oficiales identifican versión estable y requisitos mínimos.
**Alternatives considered**: 19/18 como compatibilidad temporal; excluir master del producto estable.
**Evidence**: [Builds](https://nightly.odoo.com/),
[release.py](https://github.com/odoo/odoo/blob/20.0/odoo/release.py),
[instalación](https://www.odoo.com/documentation/20.0/administration/on_premise/source.html).
No acreditar compatibilidad funcional del producto por consultar requisitos upstream.

## R02 Desarrollo propio desde cero

**Decision**: Crear addons `arg_pyme_*`; extender modelos nativos compatibles sin copiar addons de clientes.
**Rationale**: Respetar la instrucción del usuario y conservar la plataforma Odoo.
**Alternatives considered**: Copiar ARG existente; descartar por instrucción. Rehacer stock/contabilidad; evitar duplicación.
**Evidence**: [Manifiestos](https://www.odoo.com/documentation/20.0/fr/developer/reference/backend/module.html).

## R03 Separación documental

**Decision**: Separar tipos por navegación, identidad, estados y efectos, con enlaces trazables.
Crear Presupuesto ARG propio mediante `arg.pyme.quotation`; generar un pedido nativo `sale.order` separado desde el presupuesto confirmado.
Conservar líneas vinculadas, condiciones aprobadas e historia del presupuesto sin convertir su registro en pedido.
**Rationale**: Mantener claridad documental inspirada en FactuSOL.
**Alternatives considered**: Menú único de operaciones; descartar. Modelo nuevo por pantalla; justificar individualmente.
**Evidence**: Doce capturas del usuario; [mapa de procesos DELSOL](https://ayudafactusol.sdelsol.com/docs/f3007-mapa-de-procesos).
Odoo utiliza un mismo `sale.order` para su presupuesto/pedido nativos; esa implementación no cumple por sí sola la separación documental requerida para ARG.
Reservar snapshots para revisiones del presupuesto propio, no como sustituto de su identidad documental.

## R04 Licencia y sostenibilidad

**Decision**: Mantener licencias originales; proponer AGPL-3.0 para addons originales, con elección final pendiente.
**Rationale**: Mantener código comunitario y revisar compatibilidad de cada dependencia.
**Alternatives considered**: LGPL-3.0 para addons propios, con mayor permisividad.
**Evidence**: [LICENSE Odoo 20](https://github.com/odoo/odoo/blob/20.0/LICENSE),
[AGPL](https://www.gnu.org/licenses/agpl-3.0.html), [licencias OCA](https://github.com/OCA/l10n-argentina).
No declarar licencia adoptada del repositorio antes de resolver esta elección.
Separar software gratuito de alojamiento y asistencia opcionales.

## R05 Argentina y conectores después del núcleo

**Decision**: Diferir ARCA y otros conectores, conforme a la última instrucción del usuario.
Evaluar `l10n_ar` como base abierta de maestros fiscales al especificar facturación.
**Rationale**: La gestión interna básica debe preceder a las conexiones externas.
**Alternatives considered**: Presuponer localización fiscal completa gratuita; descartar.
**Evidence**: [Manifest l10n_ar](https://github.com/odoo/odoo/blob/20.0/addons/l10n_ar/__manifest__.py),
[documentación argentina](https://www.odoo.com/documentation/18.0/applications/finance/fiscal_localizations/argentina.html),
[ARCA oficial](https://www.arca.gob.ar/ws/documentacion/ws-factura-electronica.asp).
La documentación general no prueba disponibilidad Community de EDI y reportes legales.
Identificar registros internos hasta incorporar emisión fiscal autorizada.

## R06 Portada y documentación pública

**Decision**: Preparar README visual navegable y planificar una web documental estática posterior.
**Rationale**: Convertir el repositorio en entrada pública del proyecto sin infraestructura adicional obligatoria.
**Alternatives considered**: Hosting y aplicación web independiente inmediatos; innecesarios para planificación.
Separar publicación del README y habilitación de un sitio; no activar Pages automáticamente.

## R07 Identidad y referencias

**Decision**: Proponer celeste/blanco, acento solar y firma Goxtech secundaria.
Adoptar áreas, cinta contextual, filtros, listados y fichas de las capturas como patrones funcionales.
**Rationale**: Mantener reconocimiento operativo con identidad propia argentina.
**Alternatives considered**: Copia literal de assets o temas distintos por rubro; descartar.
Conservar capturas como referencias privadas; revisar derechos antes de redistribuirlas.

## R08 Soberanía

**Decision**: Instalación propia, respaldos completos portables, exportación y conectores optativos.
**Rationale**: Permitir cambiar de infraestructura y proveedor.
**Alternatives considered**: SaaS obligatorio, licenciamiento remoto o cuenta Goxtech obligatoria; descartar.
No equiparar autohospedaje con emisión fiscal sin internet.

## R09 Spec Kit

**Decision**: Importar scripts y templates upstream fijados al commit `7370e592f3cd9c06e5b698983957e227c75b30e2`.
Aplicar constitución, especificación, plan, investigación, modelo, contratos, guía y tareas.
**Rationale**: El workspace no contenía `.specify/` ni CLI `specify` disponible.
**Alternatives considered**: Plan sin Spec Kit; descartar por pedido explícito.
**Evidence**: [Upstream fijado](https://github.com/github/spec-kit/tree/7370e592f3cd9c06e5b698983957e227c75b30e2).
Conservar hashes y atribución en `.specify/upstream.json`; no afirmar instalación del CLI.

## R10 Identidad ARG y YouTube

**Decision**: Usar identidad ARG, nombres visibles terminados en ARG y namespace técnico `arg_pyme_*`.
Conservar GoxtechLabs como impulsor discreto y tomar otras soluciones Odoo como referencia técnica.
**Rationale**: Instrucción expresa del usuario, limitada a este proyecto.
**Alternatives considered**: Mantener marca operativa de los otros proyectos; descartar por identidad propia.
**Decision**: Incorporar YouTube como canal de alcance y enseñanza, con guías y ejemplos versionados.
**Rationale**: Facilitar descubrimiento, adopción y comunidad.
**Alternatives considered**: Depender exclusivamente de videos; conservar también documentación pública independiente.
Definir canal y encargo editorial antes de publicar; no asumir una URL ni audiencia existentes.

## R11 Tutoriales por módulo y soporte general

**Decision**: Vincular YouTube y manuales desde cada módulo mediante un catálogo editable y versionado.
**Rationale**: Instrucción del usuario para mantener aprendizaje actualizado con cada módulo.
**Alternatives considered**: Enlaces dispersos en código o cambios de video que exijan reinstalar; descartar.
**Decision**: Centralizar soporte general administrado por el responsable, con correo, WhatsApp o tickets configurables.
**Rationale**: Mantener todos los accesos de asistencia bajo su administración sin duplicar canales por módulo.
**Decision**: Renombrar identidad visible de OdooBot como GOXTECHBOT, con branding suave.
**Rationale**: Excepción de marca explícita posterior a la convención general ARG.
Conservar identificadores y relaciones nativas; inventariar superficies concretas antes de implementar.
Definir canales reales antes de habilitarlos; reservar conexiones API para Integraciones ARG.

## R12 Marca personal y propósito comunitario

**Decision**: Identificar a Gonzalo Sarubilo como impulsor y autor de sus aportes personales.
Presentar más de 20 años de experiencia en tecnología para pymes, según su declaración.
Incluir gestión financiera, dirección de empresas, redes, software/desarrollo, gestión, marketing y ventas.
**Rationale**: Visibilizar conocimiento y aportes del impulsor mientras aprende de la comunidad.
**Alternatives considered**: Atribución exclusivamente corporativa; reemplazarla por autoría personal visible con marca técnica discreta.
**Decision**: Presentar consultoría y servicios profesionales como actividad secundaria y opcional.
**Rationale**: El objetivo principal de este proyecto es compartir conocimiento y aportar valor comunitario.
Evitar condicionar el acceso al conocimiento o la participación a una contratación.
Conservar ARG como identidad del producto y reconocer contribuciones de otros autores.

## Decisión posterior de licencia — 2026-11-01

El titular adoptó AGPL-3.0 para addons originales y CC BY-SA 4.0 para documentación/recursos. Se aplica AGPL-3.0-only, sin presuponer versiones futuras. NOTICE.md y LICENSES/ conservan textos y excepciones. Esta decisión sustituye la propuesta D04 previa; Odoo, Spec Kit y terceros mantienen sus licencias.
