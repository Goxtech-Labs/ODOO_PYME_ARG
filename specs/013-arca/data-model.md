# Data model: Contrato futuro ARCA dentro de Integraciones ARG

| Entidad | Modelo o representación propuesta | Datos y relaciones | Restricción |
| --- | --- | --- | --- |
| Emisor | `configuración interna del adaptador ARCA` | compañía, CUIT, PV, ambiente, certificado_ref | Configuración fiscal real fuera de fixtures |
| Solicitud | `arg.pyme.integration.job` | idempotencia fiscal, hash, resultado y correlación | Producción desactivada |
| Comprobante fiscal | `account.move y campos l10n_latam` | tipo, número, emisor, autorización y fechas | No reemplazar número fiscal por FAC interno |

## Estados, efectos y seguridad

- La localización l10n_ar Community no incluye por sí sola autorización electrónica.
- Esta spec no acredita compatibilidad fiscal; verificar documentación oficial y homologación al implementar.
- No realizar emisión ni comunicación fiscal real durante desarrollo con datos de ejemplo.

Usar compañía, permisos y ambiente efectivos en servidor; ocultar un menú no constituye control de acceso.
Conservar fechas, monedas e importes históricos cuando cambien maestros o configuración.
Vincular originales y derivados mediante relaciones verificables, no solamente textos de referencia.
