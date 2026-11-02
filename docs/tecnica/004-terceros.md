# Terceros ARG — implementación

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

Addon arg_pyme_terceros20.0.1.0.0; deps Base ARG, UI ARG y contacts.
res.partner nativo; arg.pyme.partner.role sólo clasifica roles combinables. Rank comercial se sincroniza únicamente cuando existe.
Campos internos restringidos a base.group_user; métodos privados de condiciones respetan ACL y compañía sin sudo de negocio.
Índice normalizado de identificación para advertir coincidencias accesibles; sin unicidad fiscal global ni fusión automática.
Monedas y condiciones company_dependent; moneda efectiva de lista nativa en ventas y preferencia nativa de compras cuando existe.
Hook idempotente clasifica exclusivamente fixtures con XML ID arg_demo. No modifica otros contactos.
Sin conectores, datos fiscales inventados ni cuentas corrientes paralelas.
