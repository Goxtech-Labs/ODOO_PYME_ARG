# Contrato de operaciones: Contrato futuro ARCA dentro de Integraciones ARG

**Alcance**: Preparar adaptador fiscal futuro con homologación separada y trazabilidad; no habilitar emisión real en ejemplos.

## Recorridos y datos mínimos

### Operación 1: Configurar emisor

Como administrador necesito separar compañía, emisor, punto de venta y ambiente.

**Resultado**: Validar configuración de homologación sin usar CUIT o certificados reales del usuario.
**Excepción**: Bloquear producción sin configuración y autorización específicas.

### Operación 2: Autorizar comprobante

Como operador necesito conocer el estado fiscal exacto.

**Resultado**: Preparar solicitud consistente y registrar autorización, rechazo o resultado incierto.
**Excepción**: Consultar último autorizado ante timeout antes de solicitar otra numeración.

### Operación 3: Mostrar evidencia

Como usuario necesito imprimir el estado correcto y corregir por documento inverso.

**Resultado**: Distinguir borrador, pendiente, autorizado y rechazado en pantalla e impresión.
**Excepción**: No imprimir CAE ficticio ni borrar un comprobante autorizado.

## Invariantes

- La localización l10n_ar Community no incluye por sí sola autorización electrónica.
- Esta spec no acredita compatibilidad fiscal; verificar documentación oficial y homologación al implementar.
- No realizar emisión ni comunicación fiscal real durante desarrollo con datos de ejemplo.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.

Resultado incierto: consultar el número fiscal exacto por ambiente/emisor/PV/tipo y contrastar atributos/hash
con esta solicitud. Consultar último autorizado ayuda al correlativo, pero no prueba autorización de este comprobante.
Si no hay evidencia suficiente, conservar uncertain y exigir resolución; nunca asociar CAE del último de otro documento.
Preservar evidencia fiscal autorizada en almacenamiento nativo durable y exportable, independiente de deshabilitar adaptador.
