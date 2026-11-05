# Investigación · Cartera de valores y tesorería argentina

**Fecha**: 2026-11-05. Diseño, no verificación funcional.

## Decisión

Crear/extender `arg_pyme_valores` opcional sobre arg_pyme_administracion, arg_pyme_documentos, arg_pyme_informes; evaluar account; candidatos l10n_ar_check y account_batch_payment sólo tras verificar APIs/licencia.

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

La selección de APIs/clases y dependencias mínimas se cierra al inspeccionar la versión instalada antes
de programar. Esa tarea técnica tiene salida definida; no autoriza instalar candidatos por anticipado.

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
