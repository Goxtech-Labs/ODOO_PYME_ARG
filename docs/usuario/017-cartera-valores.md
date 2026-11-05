# Registro de valores ARG · desarrollo inicial

La ficha de cheques y pagarés conserva el orden **fecha → tercero → documento → importe**.
Propone hoy según la zona horaria del usuario y respeta la fecha que se indique. La moneda se
propone desde la compañía. Los datos del título y observaciones se completan en las pestañas.

Al guardar asigna un código propio `CHQ-000001` o `PAG-000001` y conserva el tipo y la compañía.
Los datos del borrador pueden corregirse; la cancelación mantiene el número y su historial.
La cuenta bancaria registrada puede proponer banco, cuenta y librador. No es necesario registrar
otra cuenta bancaria para completar manualmente los datos conocidos del título.

Este incremento está instalado en el entorno aislado de desarrollo. La demo compartida conserva
su versión publicada; no presenta todavía una cartera de cheques operativa.

Las recepciones, endosos, depósitos, descuentos, acreditaciones y rechazos continúan en desarrollo,
al igual que seleccionar valores dentro de REC/OPA. Un borrador no altera facturas, caja, bancos
ni existencias. El recibo multimedio previsto conservará cada medio y su aplicación a facturas.

Tutorial específico: pendiente. Módulo20.0.1.0.0; [canal general Goxtech Argentina](https://www.youtube.com/@Goxtech_Arg).
El canal general no sustituye una demostración compatible de este circuito.

[Plan y contrato](../../specs/017-cartera-valores/spec.md) · [Estado de la entrega](../entregas/017-cartera-valores.md)
