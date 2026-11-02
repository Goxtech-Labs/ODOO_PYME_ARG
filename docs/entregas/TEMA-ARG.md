# Paleta ARG y superficies nativas · 2026-11-02

## Resultado

Interfaz20.0.1.1.5 reemplaza los valores de marca violeta antes de compilar los assets de Odoo20.
El azul operativo es #145B91; enlaces oscuros usan #8BC4F1. Las listas de colores conservan sus
índices y longitudes; sólo se sustituyen familias violeta/rosa de presentación por azules.
No se alteran colores de productos, fotografías ni estados de negocio.

Variables primarias antes de `web/static/src/scss/primary_variables.scss`, extensión de paletas
secundarias después de `secondary_variables.scss`; sin copiar ni modificar core. Los alias CSS
usan el prefijo vacío real de Bootstrap en Odoo20 y respetan la preferencia ARG claro/oscuro.
Buscador, calendario y botones neutros reciben superficies y texto coherentes en oscuro.

El favicon original ARG se ofrece como fallback; `x_icon` de empresa conserva prioridad y no se
fuerza MIME SVG sobre un icono ajeno. El color de navegador es azul en acceso/backend/ayuda.
Enlaces de llave de acceso/atribución y salto al contenido usan también azul ARG.
La marca dinámica inyectada por Portal se sobreescribe sólo en el acceso ARG, sin modificar
la preferencia de portal de la compañía. Login conserva autenticación y CSRF nativos, con URL CSS versionada para renovar caché.

## Verificación realizada

- Compilación real de assets y arranque OWL en CT aislado antes de actualizar la demo.
- Inicio, listado con selección, formulario vacío, desplegable Cliente, calendario y preferencias
  nativas revisados. Formularios visuales descartados sin crear documentos.
- Capturas y análisis de estilos computados en claro/oscuro: cero coincidencias violeta en las
  superficies observadas. El buscador oscuro combina texto #F0F5FA con fondo #1B2B38; las cabeceras
  del calendario dejaron de usar fondo blanco con texto claro.
- Revisión estática independiente del diff exacto por otra sesión de la misma familia/cuenta,
  sin hallazgos bloqueantes; no constituye auditoría externa ni independencia de modelo.
- AST/XML/JS/manifests y Gitleaks sin hallazgos.91 módulos;231 archivos del paquete verificados
  en ambos entornos. Sólo se actualizó `arg_pyme_ui`.
- Snapshot y backup completos previos íntegros, sin ensayo de restauración nuevo. Conteos de negocio
  antes/después preservados; no se ejecutó el fixture funcional de Ventas ni se emitieron mensajes,
  pagos o comprobantes fiscales. Cron/correo continúan desactivados.

Paquete SHA256 `37f8c64c3030591348b193e6560c2da585d5ff78d02f87c3e678d2325518788e`. Evidencia operativa privada en
`artifacts/release-005-theme-20261102`, fuera del repositorio público y sin credenciales.

## Límites

El análisis CSS no revisa cada píxel de imágenes, pseudoelementos, estados ocultos ni addons ajenos.
No acredita accesibilidad completa, todos los roles/circuitos ni aceptación del titular.
Las imágenes de terceros no se recolorean automáticamente. La aplicación instalada, el código
publicado, la revisión parcial y la aceptación se registran por separado.
