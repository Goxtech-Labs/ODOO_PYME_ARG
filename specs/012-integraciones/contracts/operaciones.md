# Contrato de operaciones: Integraciones ARG

**Alcance**: Único módulo para configuración, salud y adaptadores de todos los proveedores externos; posterior al núcleo.

## Recorridos y datos mínimos

### Operación 1: Configurar proveedor

Como administrador necesito habilitar sólo el servicio elegido.

**Resultado**: Crear configuración por compañía y entorno con secreto referenciado fuera de Git.
**Excepción**: Deshabilitar por defecto y detectar configuración incompleta sin revelar claves.

### Operación 2: Ejecutar con control

Como operador necesito enviar una operación autorizada sin duplicados.

**Resultado**: Encolar una operación con clave idempotente y registrar resultado sanitizado.
**Excepción**: Resolver timeout como estado incierto y consultar proveedor antes de repetir.

### Operación 3: Diagnosticar y detener

Como responsable necesito ver fallos y detener envíos.

**Resultado**: Pausar proveedor y consultar intentos sin contenido sensible.
**Excepción**: Conservar evidencia al rotar credenciales o revocar servicio.

## Invariantes

- No conservar payload sensible completo en logs.
- Estados draft, queued, processing, succeeded, failed, uncertain y canceled con transiciones explícitas.
- Timeout requiere lookup y conciliación antes de reintentar efectos irreversibles.
- Deshabilitar proveedor conserva jobs e historia. La desinstalación del addon requiere política explícita de conservación/exportación y no equivale a deshabilitar.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.

Idempotencia: compañía + proveedor + ambiente + clave de operación comercial estable; no incluir ID mutable de conector/credencial.
Para ARCA agregar emisor, punto de venta, tipo y número fiscal correlacionado.
Deshabilitar conserva datos. Bloquear desinstalación del addon con operaciones inciertas o evidencia pendiente de preservación;
requerir exportación verificada, resguardo protegido y aceptación de retirada. La evidencia fiscal autorizada debe persistir
como documento/adjunto nativo durable con formato público, además de la configuración del adaptador.
No confiar en conservar tablas que Odoo elimina al desinstalar su addon.
