# Roles y carga progresiva

Los roles son capacidades combinables: una persona puede vender, comprar, entregar y administrar.
No exigir departamentos, vendedores adicionales ni aprobadores distintos en micropymes.
Administrador configura; operador de circuito prepara/consulta; responsable confirma/revierte según permiso.
Consulta y exportación son permisos separados de edición y confirmación. Cambiar un menú no evita acceso RPC.

| Operación | Datos pedidos normalmente | Validación al confirmar |
| --- | --- | --- |
| Alta tercero | Nombre y rol cliente/proveedor | Datos fiscales sólo si exige operación posterior |
| Alta producto | Nombre, tipo y precio si conocido | Unidad, políticas e impuestos configurados |
| PRE/PED/PPC | Tercero, producto, cantidad | Moneda, precio/condiciones y líneas coherentes |
| REM/ENT | Origen y cantidad efectiva | Ubicaciones, lote/serie si corresponde |
| FAC/FRC | Origen o tercero/líneas directas | Datos contables/fiscales requeridos por operación |
| REC/OPA | Tercero/deuda, importe y medio | Diario, moneda, cuentas transitorias y aplicaciones |
| INV | Ubicación y contado | Diferencia, motivo y control de concurrencia |

Usar fecha, compañía, depósito, moneda, lista e impuestos predeterminados conocidos.
Mostrar origen del valor automático y permitir excepción por permiso. Nunca rellenar CUIT o tipo de cambio inventado.
Datos avanzados en secciones desplegables; errores al lado del campo y resumen con siguiente acción.
Orden de tabulación: fecha → tercero → identificación documental → conceptos/artículos → totales → acciones.
Fecha de registro: hoy por defecto en una carga nueva, con zona horaria del usuario y corrección explícita.
No sobrescribir fechas del usuario, históricas, importadas o heredadas. El vencimiento conserva su regla propia.
Tipo/código documental se deducen de la pantalla; no pedirlos como un paso repetido de carga.
Datos secundarios en pestañas o secciones adicionales; no inventar información requerida ausente.
Enter agrega línea sin confirmar documento. Priorizar pocos pasos para equipos pequeños.

## Regla de carga cotidiana

El recorrido documental es **cuándo → a quién → documento → qué**, sin volver a pedir la
configuración de la empresa en cada operación. Hoy aparece propuesto; el operador sólo modifica
la fecha cuando corresponde. El tipo de documento surge del acceso utilizado y su código/número
se asigna conforme al contrato de cada circuito. Un número de comprobante externo se solicita
cuando identifica el documento recibido; no se inventa ni se confunde con la numeración interna.

| Circuito | Lo que completa normalmente la persona | Lo que se propone o se toma del origen |
| --- | --- | --- |
| Ventas | Cliente y artículos/conceptos con cantidades; revisar precio | Fecha de hoy, tipo documental, moneda, lista, condiciones e impuestos configurados |
| Compras | Proveedor, referencia externa cuando corresponda y artículos/conceptos | Fecha de registro, datos del pedido y condiciones conocidas; fecha del comprobante separada si difiere |
| Stock | Documento de origen y cantidades efectivas, o producto/ubicación en un ajuste | Fecha, productos y ubicaciones del origen; no exigir tercero en movimientos internos |
| Administración | Cliente/proveedor, medios e importes y documentos a cobrar/pagar | Fecha y datos de la deuda seleccionada; perfil de caja/banco previamente configurado |
| Reparaciones | Cliente, equipo identificable y problema informado | Fecha y código del parte; diagnóstico, técnico y costos se completan en su etapa |

Los defaults son propuestas visibles y corregibles según permisos. No reemplazan una fecha ya
elegida ni una información explícita del documento de origen. Vencimiento, fecha de emisión del
comprobante, fecha prometida de entrega y fecha de ejecución bancaria conservan su significado:
no se completan todas con hoy para reducir campos.

Datos fiscales, depósito, moneda, cuenta, serie/lote u otros datos secundarios se solicitan en la
etapa en que resulten indispensables. Cuando falta una configuración necesaria, indicar el dato
faltante y el siguiente paso; no exigirla repetidamente, ocultarla ni inventarla. Guardar un borrador
no exige anticipar el diagnóstico, la entrega, la acreditación o la emisión fiscal de etapas futuras.

## Criterios de revisión por documento

En la revisión posterior de cada módulo comprobar: fecha propuesta una sola vez; fecha corregida
conservada al guardar/reabrir; datos del origen reutilizados; orden visual y de teclado coincidentes;
datos avanzados fuera del recorrido ordinario; requisitos específicos visibles cuando aplican.
Una persona con las capacidades necesarias debe poder completar el circuito sin asignar usuarios
ficticios a departamentos o aprobaciones adicionales. Estos criterios no acreditan revisión ya ejecutada.

ACL por modelo, reglas company_id compatible con allowed_company_ids y validaciones check_company en relaciones.
Nunca usar sudo para construir saldos o exportaciones del operador. Proteger secretos por grupo administrador.
Guardar auditoría de confirmaciones/reversiones; no registrar contraseñas, payloads completos ni datos fiscales en logs públicos.
