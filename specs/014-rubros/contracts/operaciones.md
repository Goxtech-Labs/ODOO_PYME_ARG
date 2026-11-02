# Contrato de operaciones: Extensiones por rubro y personalizaciones ARG

**Alcance**: Proceso y contrato para agregar rubros sin imponer reglas sectoriales al núcleo genérico.

## Recorridos y datos mínimos

### Operación 1: Definir alcance

Como comunidad necesito describir un rubro mediante casos reales anonimizados.

**Resultado**: Completar plantilla con problema, documentos, campos mínimos y exclusiones.
**Excepción**: Rechazar supuestos de otro cliente que contradigan la gestión genérica.

### Operación 2: Extender sin duplicar

Como desarrollador necesito agregar campos y operaciones coherentes.

**Resultado**: Proponer addon arg_pyme_rubro_nombre con extensiones y relaciones al núcleo.
**Excepción**: Resolver conflicto entre reglas de rubros mediante composición explícita.

### Operación 3: Documentar entrega

Como usuario necesito saber qué agrega y cómo aprenderlo.

**Resultado**: Encontrar manual, datos de ejemplo, tutorial y notas de compatibilidad por rubro.
**Excepción**: Conservar datos al deshabilitar menús y documentar límites de desinstalación.

## Invariantes

- Indumentaria, comercio, servicios y otros rubros son candidatos, no funciones prometidas en el núcleo.
- Una regla exclusiva de cliente permanece en su personalización.
- Toda integración externa nueva se registra en Integraciones ARG.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.
