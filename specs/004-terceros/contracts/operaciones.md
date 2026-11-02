# Contrato de operaciones: Terceros ARG

**Alcance**: Gestionar clientes y proveedores con una ficha por identidad, alta rápida y datos fiscales/comerciales progresivos.

## Recorridos y datos mínimos

### Operación 1: Alta mínima

Como operador necesito dar de alta un tercero con datos disponibles y completar lo demás cuando corresponda.

**Resultado**: Guardar un contacto de ejemplo con nombre y rol y continuar el documento.
**Excepción**: Permitir borrador sin datos fiscales desconocidos y señalar requisitos antes de la operación que los necesita.

### Operación 2: Combinar roles

Como responsable necesito que un mismo tercero pueda ser cliente y proveedor sin duplicar sus datos.

**Resultado**: Agregar rol proveedor a un cliente y conservar identidad, contactos e historia.
**Excepción**: Advertir posibles duplicados sin fusionar automáticamente identidades diferentes.

### Operación 3: Aplicar condiciones

Como operador necesito condiciones predeterminadas sin volver a escribirlas en cada documento.

**Resultado**: Aplicar moneda, tarifa, plazo y dirección conocidas al crear un documento.
**Excepción**: Conservar corrección explícita del usuario y no completar con datos inventados.

## Invariantes

- No fusionar registros por coincidencia parcial de nombre.
- Validar formato de CUIT separado de verificación remota de padrón.
- No activar consultas externas al guardar una ficha.
- Permitir importar ejemplos con clave estable y conservar ceros iniciales en códigos.

Aplicar [contrato documental común](../../001-pyme-argentina/contracts/documentos.md),
[interfaz](../../001-pyme-argentina/contracts/interfaz.md) y
[soberanía](../../001-pyme-argentina/contracts/soberania.md).

No activar servicios externos por abrir una pantalla ni enviar datos sin acción de usuario autorizada.
Conservar ayuda/tutoriales por módulo y soporte general administrado centralmente.
