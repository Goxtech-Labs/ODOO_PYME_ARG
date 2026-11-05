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

ACL por modelo, reglas company_id compatible con allowed_company_ids y validaciones check_company en relaciones.
Nunca usar sudo para construir saldos o exportaciones del operador. Proteger secretos por grupo administrador.
Guardar auditoría de confirmaciones/reversiones; no registrar contraseñas, payloads completos ni datos fiscales en logs públicos.
