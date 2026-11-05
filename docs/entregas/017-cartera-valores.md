# Valores ARG · base de registro · 2026-11-05

Addon opcional `arg_pyme_valores`20.0.1.0.0, original AGPL-3.0-only. Identidad CHQ/PAG por compañía,
ficha con fecha de hoy propuesta, tercero, documento e importe; secundarios en pestañas.
Incluye borradores, cancelación conservando número, validación de nominal positivo, clave de
identificadores conocidos e historial interno append-only. No modifica core ni efectos de tesorería.

Instalación técnica en entorno aislado Odoo20 Community:102 módulos,13ARG+89nativos/dependencias.
Paquete242 archivos SHA2563f7d5c91be18bb4a7c802756452240e13d89e8477299aaa65bcaa0826a42d2a8.
El [registro de composición candidato](../../composition/candidates/017-valores-registro.json) está
separado de la [composición publicada](../../composition/versions.lock.json).

Controles: AST/XML/JS/manifests, Gitleaks sin hallazgos, revisión estática independiente por otra
sesión de la misma familia/cuenta; instalación y arranque. Lectura técnica de versión, fuentes,
ACL, tipos documentales, vistas list/form y defaults de fecha con contexto histórico/vacío.
Sin crear documentos, operaciones bancarias, correo ni nuevas pruebas de negocio o visuales.
Respaldo por snapshot del entorno aislado antes de instalar. Sin cambios al entorno compartido.

La instalación inicial detectó dos incompatibilidades resueltas en el código: `res.bank` no existe
en esta composición y el selector de ACL no admite `rc`. Se usa `res.partner.bank` y permisos
de lectura/creación separados, manteniendo la factoría de eventos protegida en servidor.

Pendientes: motor financiero por instrumento/medio, reservas exclusivas, cartera y transmisiones,
depósitos, liquidaciones, negociación y recurso, rechazo parcial, enlace REC/OPA, lotes,
transferencias, informes, ejemplos y tutorial específico. No se habilita cheque como medio manual
genérico: haría aparecer dinero disponible sin demostrar acreditación. La base de registro no cierra017.

QA funcional/visual y aceptación posteriores, según [quickstart](../../specs/017-cartera-valores/quickstart.md).
[Manual inicial](../usuario/017-cartera-valores.md) · [Tareas](../../specs/017-cartera-valores/tasks.md)
