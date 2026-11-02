# Contrato de operaciones: Base ARG

**Alcance**: Configurar compañía, roles combinables, tipos/secuencias internas, ayuda por módulo y soporte general para micropymes.

## Recorridos y datos mínimos

### Operación 1: Identificar documentos

Como operador necesito reconocer cada documento con código corto sin cargar números manualmente.

**Resultado**: Asignar PRE-000001 y PED-000001 desde secuencias independientes y conservar ambos códigos.
**Excepción**: Rechazar una colisión, conservar números anulados y permitir crecimiento por encima de seis dígitos.

### Operación 2: Configurar roles y preferencias

Como responsable necesito combinar funciones en pocas personas sin crear departamentos artificiales.

**Resultado**: Asignar a una persona Ventas, Compras y Administración según permisos expresos.
**Excepción**: Rechazar acceso a otra compañía o acción fuera de permisos efectivos.

### Operación 3: Ayuda y soporte central

Como usuario necesito tutoriales de mi módulo y un único soporte general administrado por el responsable.

**Resultado**: Actualizar un enlace YouTube central sin reinstalar el módulo y encontrarlo desde su ayuda.
**Excepción**: Mostrar guía escrita y estado pendiente cuando falte un video o canal de contacto.

## Invariantes

- No reutilizar códigos anulados ni reiniciar por ejercicio implícitamente.
- Conservar código interno separado del número fiscal y del proveedor.
- Mantener compañía, zona horaria e idioma explícitos.
- Compartir configuración única de soporte; capturar contexto opcional sin exigirlo al usuario.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.
