# OPA y entregas de cheques · desarrollo1.2 · 2026-11-05

**Código preparado; instalación pendiente de autenticación del operador.** Valores20.0.1.2.0 y
Administración20.0.1.1.4. No atribuirles instalación, QA o disponibilidad en la demo compartida.
Últimas composiciones verificadas: aislado [REC1.1](017-rec-cheques.md) y demo0.1.5.
No se revalidó su estado actual después del pedido de renovación SSH.

## Cambios desarrollados

OPA admite cheque propio o recibido en papel, por su nominal completo. Reserva explícita o automática
al confirmar; otra OPA no puede comprometerlo. Cambiar/eliminar un medio reservado requiere liberar;
cancelar borrador libera. Reserva no paga deuda. Fecha, tercero, instrumento y nominal conservan orden.

La entrega con constancia genera pago nativo y aplicación al proveedor. Terceros usa la cuenta de
cartera del REC; propio crea una obligación pendiente en pasivo corriente. El débito propio completo posterior reclasifica obligación a banco y no paga de nuevo.
El medio y nominal se proponen al elegir título; campos necesarios de transmisión aparecen en OPA.

Devolución/rechazo de salida corrige sólo su línea/pago de OPA. REC mantiene sus aplicaciones.
Rechazo devuelve un título discutido, no reutilizable. Recuperación del cliente requiere otro evento
explícito. Reversión general exige resolver títulos; un documento cuyos medios ya tienen inversos
puede cerrarse sin repetirlos. El rol/pago/línea gobierna cada corrección, no el estado global del valor.

El diálogo conserva la entrega objetivo: una nueva entrega del mismo título no cambia qué OPA corrige
un diálogo anterior. Reintentos se reconocen por solicitud y objetivo antes de exigir actividad actual.
El seguimiento de responsabilidad vive por transmisión; el nominal por instrumento no se suma varias
veces. Alcance desconocido queda marcado. Cerrar seguimiento no registra dinero del cliente.

Los perfiles de medios conservan su uso; reutilizar su cuenta en un medio sin etiqueta no permite
crear pagos de cheque anónimos. Pagos1.1 se reconocen por su línea y cuenta histórica, aunque cambió
el perfil predeterminado. Una marca de migración preserva callbacks/correcciones de pagos ordinarios
anteriores; crear/publicar de nuevo o modificar términos sigue validando el instrumento. Perfiles
nuevos no pueden mezclar cuentas con pagos anónimos, y un perfil anterior mezclado puede cambiarse
a una cuenta nueva sin forzar su etiqueta histórica. Se limpian default_* antes de motores/eventos/reversión/conciliación.
Bloqueos: instrumentos primero, cabeceras después; callbacks internos no expanden el grafo de reservas.

## Evidencia y pendientes

Paquete252 archivos SHA2565352cb7f09e433ce1e745a60c133e9176b626dac6fe9593e4ae8313952bf6720.
[Composición de código candidata](../../composition/candidates/017-valores-opa.json), sin inventario instalado atribuido.

AST/XML/JS/manifests, Gitleaks y revisión estática independiente por otra sesión de la misma familia/
cuenta. Hallazgos corregidos: objetivo mutable de devolución/reintento y pago legacy con perfil cambiado.
La fuente nativa20 cacheada admite cuentas transitorias activo/pasivo corriente y account.journal.bank_account_id;
esa lectura no sustituye instalación ni prueba financiera de esta composición.

Tailscale pidió renovación SSH antes de leer/instalar en el servidor; ninguna mutación de este incremento
se ejecutó allí. El cargador nuevo de ejemplos está preparado, no ejecutado: perfiles propios, banco
ficticio y un cheque propio en borrador, sin pagos/asientos/stock ni cambios a cron o correo.
La guía1.1 queda para revisión y enlaza la nueva, conservando texto, URL y video del administrador.

Pendientes017: instalación/lectura posterior, promoción, QA posterior, ECHEQ, custodia, negociación/
descuento/recurso avanzado, parciales, operaciones posteriores al débito/acreditación, lotes,
transferencias, pagaré formal, informes y tutoriales completos. Se conserva todo el plan de expansión.

[Contrato de salidas](../../specs/017-cartera-valores/contracts/salidas-opa.md) ·
[Manual](../usuario/017-cartera-valores.md) · [Tareas](../../specs/017-cartera-valores/tasks.md)
