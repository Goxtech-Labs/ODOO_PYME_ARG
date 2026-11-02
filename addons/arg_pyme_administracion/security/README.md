# Acceso Administración ARG

Primera entrega: group_administracion implica account.group_account_readonly nativo; amplía lectura de contabilidad,
no escritura. Esto permite consultar apuntes/documentos publicados y abrir orígenes con permisos nativos.
No crea ACL paralelas sobre saldos, no usa sudo ni SQL. Conserva reglas nativas de compañía y personalizadas.
Campos ARG sólo para Administración; vistas ARG sin crear/editar/borrar. La UI de consulta no sustituye ACL de ORM.
Las capacidades CRUD que ya posea un usuario por otros grupos permanecen regidas por esos permisos.
Recibos/OPA y confirmación de dinero todavía no se implementan; no se conceden permisos nuevos para efectuarlos.

Administrador ARG implica el rol Administración, en coherencia con los otros circuitos.
