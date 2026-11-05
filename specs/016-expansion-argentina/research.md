# Investigación y decisiones · 2026-11-05

## Evidencia de partida

Código local y contratos del núcleo; consulta SQL de sólo lectura del runtime:101 módulos instalados,
POS sí; repair/mrp/project/hr_timesheet/sale_commission/l10n_ar_check/account_batch_payment/website_sale
no entre candidatos. Lock histórico91 módulos no equivale al runtime nuevo. Revalidar al empaquetar.
Lecturas de otras sesiones Codex, misma familia/cuenta: mapa de dependencias y tesorería, sin mutaciones.

## Decisiones

| Decisión | Razón | Alternativa descartada |
| --- | --- | --- |
| Recuperar procesos, argentinizarlos | Uso real de pyme y soberanía | Copiar impuestos/normas/SEPA o pantallas propietarias |
| REC multimedio aplica factura, cartera separada | Definición del titular; aplicación no equivale a liquidez | Registrar cheque como método manual bancario genérico |
| OPA/lote/transferencia separados de pagaré | Usos prácticos y títulos no son sinónimos | Renombrar remesa/pagaré español como pago ejecutado |
| Valores con identidad/eventos | Cadena, rechazo y recurso necesitan historia | Recrear cheque por cada tenedor o editar estados sin efecto |
| Opcionales sobre motores nativos | Compatible con núcleo genérico | Otros saldos/stock o forks por cliente |
| Canales en Integraciones ARG | Una configuración y control de efectos | Addon por conector y envío automático por instalar |

## Fuentes primarias consultadas

- [FactuSOL, funciones](https://www.sdelsol.com/programa-facturacion-factusol/): catálogo de procesos, no normativa argentina.
- [FactuSOL, partes](https://ayuda.teamsystem.es/hc/es/articles/32074315046929-F354-Partes-de-reparaci%C3%B3n): equipo, trabajo y documentos derivados.
- [FactuSOL, capítulos de obras](https://ayuda.teamsystem.es/hc/es/articles/32074062915985-F312-Cap%C3%ADtulos-de-obras): organización de costos por obra.
- [FactuSOL, comisiones](https://ayuda.teamsystem.es/hc/es/articles/32074074639761-F831-C%C3%B3mo-puedo-saber-lo-que-ha-vendido-un-agente-y-sus-comisiones): base de facturación/cobros.
- [BCRA, ECHEQ](https://www.bcra.gob.ar/echeq-o-cheque-electronico/): operaciones electrónicas diferenciadas. Consulta directa de esta sesión falló; resultados indexados y revisión delegada sustentan sólo descripción general.
- [BCRA, uso](https://www.bcra.gob.ar/emitir-un-cheque-y-usar-echeq/): emisión/operaciones y rechazos; capacidades deben revalidarse al implementar.
- [Ley24.452, texto actualizado](https://www.argentina.gob.ar/normativa/nacional/ley-24452-14733/actualizacion): clases de cheque y transmisión; no fraccionar endoso ni presumir liberación de responsabilidad.
- [Decreto-Ley5965/1963](https://www.argentina.gob.ar/normativa/nacional/norma-69687/actualizacion): referencia para distinguir pagaré de orden interna de pago.

## Alcance y certeza

Fuentes argentinas orientan identidades y separación de hechos, no una certificación jurídica/fiscal.
No codificar universalmente plazos, límites de endosos, monedas habilitadas, códigos de rechazo ni tasas.
Versionar perfiles, condiciones contractuales y evidencia; para negociación no inferir baja por etiqueta
sin recurso. Selección de clases/API/licencia de dependencias se resuelve en las tareas técnicas de cada
módulo. No hay duda técnica que justifique reconstruir core o activar proveedores durante planificación.
