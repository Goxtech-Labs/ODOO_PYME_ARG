# Composición observada al iniciar expansión · 2026-11-05

**Estado actual2026-11-06:** el código de este incremento y sus ampliaciones indicadas en la
[entrega0.1.6-dev](EXPANSION-PROMOCION.md) está instalado en demo. Las referencias siguientes a
instalación/promoción pendiente describen el antecedente histórico, no el estado vigente.
QA funcional/visual, PDF, ejemplos de circuito y aceptación siguen pendientes.

Consulta técnica de sólo lectura:101 módulos instalados; doce addons ARG; el paquete propio conserva231 archivos. El lock histórico de la entrega0.1.4
contiene91 módulos. Módulos adicionales observados: google_address_autocomplete, iot_webserial, l10n_ar_pos, point_of_sale, pos_online_payment, pos_partner_autocomplete, pos_sale, pos_sale_margin, pos_sale_stock, pos_stock.

Esta observación no demuestra configuración ni QA del POS. No elimina ni reclasifica módulos del
titular. Tres cron activos y cero servidores de correo activos observados en la demo; se conservan
sus decisiones. En aislado152:91 módulos, cron/correo0, túnel inactivo y sin interfaz de red configurada.
Sólo se inicia ese entorno aislado para controles de carga/instalación; no se ejecutan flujos ficticios.

Antes de promover: versiones/revisión/paquete y hashes se contrastan con el runtime, sin presentar el
lock antiguo como composición actual. Evidencia operativa sanitizada fuera del repositorio público.
