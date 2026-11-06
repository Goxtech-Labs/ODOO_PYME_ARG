# Contrato de soberanía y recuperación

Permitir elegir servidor, administrador y proveedor; conservar acceso completo a los datos autorizados.
Mantener instalación autónoma sin cuenta obligatoria Goxtech.

## Respaldo completo

Incluir base PostgreSQL consistente, filestore, configuración recuperable y revisiones exactas de código/dependencias.
Separar secretos del repositorio público; describir cómo recuperarlos mediante almacenamiento protegido.
Documentar ejecución, frecuencia, retención, cifrado, destino y restauración.
Documentar recuperación reproducible con datos de ejemplo y conservar las verificaciones ya
realizadas. Para nuevas operaciones de este proyecto, usar únicamente el CT definitivo con sus
snapshots o respaldos; no crear un CT temporal para restaurar. Otra instalación requiere un destino
productivo acordado, según la [política vigente](../../../docs/tecnica/POLITICA-CT.md). Esto no limita
la elección de infraestructura por quienes instalen el proyecto comunitario.
No equiparar copia de Git con respaldo de documentos y adjuntos.

## Exportación y salida

Ofrecer exportación de maestros y documentos autorizados con identificadores estables y relaciones documentadas.
Incluir monedas, estados y fechas necesarias para interpretar los datos.
Proporcionar formato abierto para tablas y conservar adjuntos originales.
Distinguir exportación de consulta de respaldo íntegro restaurable.
Documentar retirada de una instalación y revocación de accesos externos.

## Conexiones externas posteriores

Agruparlas en un único módulo Integraciones ARG, organizado internamente por servicio/proveedor.
Permitir activación y revocación independientes sin instalar un addon separado por proveedor.

Explicar proveedor, datos enviados, finalidad, compañía, ambiente y modo de revocación.
No activar conectores al visitar sus ajustes ni instalar una extensión visual.
Mantener estados Pendiente, Desactivado, Configurado, Prueba, Habilitado y Conexión comprobada según evidencia.
Evitar telemetría propia obligatoria; revisar llamadas externas de la composición efectiva.
Conservar operaciones internas ante indisponibilidad externa sin simular autorización fiscal o pagos.
