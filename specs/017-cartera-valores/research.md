# Investigación · Cartera de valores y tesorería argentina

**Fecha**: 2026-11-05. Diseño, no verificación funcional.

## Decisión

Crear `arg_pyme_valores` opcional sobre arg_pyme_administracion y arg_pyme_documentos, con account Community transitivo. Incorporar el adaptador de Informes cuando existan hechos financieros, sin crear una dependencia desde el núcleo hacia Valores.

## Razonamiento

Separar nominal disponible, aplicación de deuda, dinero acreditado/debitado y exposición por recurso. REC/OPA multim medio usa cuentas transitorias de valores y conciliación nativa, nunca residuales escritos a mano. La independencia del núcleo evita imponer un rubro a todas las pymes.

## Alternativas

Copiar pantallas españolas o duplicar libros fue descartado: cambia identidad y pierde trazabilidad.
Una dependencia nativa se prefiere si su licencia/API y su interacción con hooks ARG son compatibles;
no se declara probada antes de inspección. Las funciones propias se desarrollan desde cero.

## Fuentes

Ver [investigación coordinada](../016-expansion-argentina/research.md), contratos actuales y composición.
Referencias pertinentes: BCRA ECHEQ, Ley24452, DL5965. Políticas de cuentas, bancos y garantías se fijan con
configuración versionada; nunca usar una fuente española como normativa argentina.

## Límite de certeza

La selección siguiente corresponde a la composición instalada inspeccionada. Las APIs de efectos
financieros deben volver a contrastarse antes de implementar el adaptador; no habilitarlas por instalar
la ficha del instrumento.

## Preflight nativo observado al iniciar implementación

En el runtime20 actual no están disponibles los manifests de l10n_ar_check ni account_batch_payment.
Se implementará Valores ARG sobre account Community (manifest1.6, LGPL-3), sin depender de esos
addons ausentes ni sustituirlos con código Enterprise. La disponibilidad de repair/mrp/project/
hr_timesheet/website_sale y POS se comprobó en manifests LGPL-3; su instalación por rubro sigue separada.

API account.payment observada: action_post, action_cancel, action_draft, _get_valid_liquidity_accounts,
_prepare_move_liquidity_lines(default_values), _prepare_move_lines_per_type(write_off_line_vals=None,
force_balance=None) y _prepare_move_line_default_vals con la misma firma. Estados nativos: draft,
paid, reconciled, canceled, rejected. Paid/reconciled no prueban por sí solos acreditación de un cheque.

Pendiente cerrar implementación de clasificación por medio/evento, correcciones parciales y cuentas/
perfiles antes de habilitar REC/OPA con valores. Registrar una cuenta transitoria no basta para
distinguir liquidez. La inspección de API no es prueba funcional de cartera.

## Compatibilidad observada al instalar la base de registro

Odoo20 de esta composición no registra `res.bank`. La fuente nativa
`base/models/res_partner_bank.py` define `res.partner.bank`, con `account_number`, `bank_name`,
`bank_bic` y `partner_id`. La ficha utiliza esa cuenta opcional y conserva snapshots textuales de banco,
código bancario y cuenta libradora. No crea otra libreta bancaria ni presume que todo banco tenga BIC.
Se conservan los valores explícitos del usuario/contexto, incluidos vacíos explícitos.

La ACL unificada usa `ir.access`: el selector Operation admite `r` y `c` por separado para eventos;
la combinación `rc` fue rechazada por el cargador. Crear eventos exige además un token interno de
identidad Python, no un booleano que pueda enviarse por RPC. Reglas globales limitan ambas tablas
a compañías habilitadas; las operaciones exigen usuario interno ARG y rol Administración.

La identificación de un cheque en papel usa banco/cuenta/número conocidos. La de un pagaré usa
identificación del firmante/número/emisión y no requiere banco. El identificador electrónico, si existe,
se conserva por tipo. La clave evita duplicados exactos dentro de la compañía; no acredita autenticidad
ni detecta equivalencias entre identificadores externos distintos o datos incompletos.

El incremento instalado sólo admite borrador y borrador cancelado; recepción, endoso y REC/OPA
siguen pendientes. Ver [entrega de registro](../../docs/entregas/017-cartera-valores.md).
