# Instalar bajo tu control

ARG funciona sobre Odoo 20 Community, PostgreSQL 16 y Python 3.12 en Linux compatible.
La composición probada usa Ubuntu 24.04 y el paquete oficial Odoo 20.0.20261101.
No requiere Enterprise, una cuenta Goxtech, Cloudflare ni un proveedor de IA.
Consultá [versiones fijadas](../../composition/versions.lock.json) y [estado de entrega](../entregas/RELEASE.md).
Usá una revisión o artefacto identificado; no instales una rama móvil sin registrar su contenido.

## Preparar una instalación nueva

1. Instalá el paquete oficial Odoo de la composición y PostgreSQL compatibles siguiendo la documentación del proveedor. Conservá firma, versión y procedencia del paquete.
2. Instalá el motor PDF compatible con Odoo. Esta composición usa wkhtmltox 0.12.6.1 con patched Qt y dependencias de fuentes, según la guía de operación. Comprobá que el usuario del servicio encuentra el binario.
3. Ubicá los addons de esta entrega en una ruta local, por ejemplo /opt/odoo-pymes-arg/addons. No se descarga código de otro cliente ni Enterprise.
4. El usuario de servicio y rol PostgreSQL local se llaman odoo en los comandos siguientes. Si ya existen, verificá sus permisos en lugar de recrearlos. Conservá contraseña maestra y configuración fuera del repositorio.
5. Mantené el servicio en loopback y el entorno aislado mientras inicializás credenciales y ejemplos.

Para una base de ejemplo nueva, con rol odoo ya preparado:

```sh
sudo -u postgres createdb --owner=odoo --template=template0 --encoding=UTF8 --locale=C arg_demo
```

UTF-8 explícito evita heredar una plantilla SQL_ASCII. No ejecutar sobre una base existente.
El archivo privado /etc/odoo/odoo.conf debe definir usuario de DB, base/filtro exactos, data_dir local,
contraseña maestra propia, list_db=False, http_interface=127.0.0.1 y addons_path con addons ARG y nativos.
Usá workers=2 si el despliegue lo admite para impresión; max_cron_threads=0 durante preparación.
Protegé el archivo root:odoo 0640. No copies una contraseña de esta guía: no contiene credenciales.

## Elegir capacidades

Detené el servicio antes de inicializar y ejecutá con su usuario y configuración privados.
La combinación completa del núcleo se resuelve desde estas raíces y sus dependencias:

```sh
sudo -u odoo odoo server -c /etc/odoo/odoo.conf -d arg_demo \
  --init=arg_pyme_ventas_stock,arg_pyme_compras_stock,arg_pyme_administracion,arg_pyme_informes,l10n_ar \
  --load-language=es_AR --without-demo=True --stop-after-init --workers=0 --max-cron-threads=0 --no-http
```

No usa -uall. Para una gestión de servicios, elegí el [perfil sin Stock](../ejemplos/servicios.md)
y una base nueva independiente. Agregar Stock después requiere composición/backup y puentes explícitos;
no se simula stock desde una factura.

## Cargar sólo maestros de ejemplo

El cargador completo [seed_demo.py](../../ops/seed_demo.py) admite únicamente arg_demo sin operaciones.
Requiere ARG_DEMO_ACK_EXAMPLES=1 y las variables privadas ARG_DEMO_LOGIN, ARG_DEMO_PASSWORD
(de 16 caracteres o más) y ARG_DEMO_BASE_URL con el origen elegido por el propietario.
Pasalas al proceso desde un archivo protegido o almacén privado; no las pongas en argumentos, historial,
Git ni logs. Ejecutá el script dentro de odoo shell, con configuración y usuario del servicio.

Crea contactos/productos ficticios, lista ARS, compañía de ejemplo, roles y marca de datos de ejemplo.
No fija un dominio o usuario Goxtech, no envía mensajes ni registra documentos publicados.
Conserva contactos, productos y lista encontrados por sus XML IDs. El inicializador fija otra vez
la configuración de compañía, depósito y acceso administrador del entorno de ejemplo; no es
un sincronizador para instalaciones personalizadas. Rechaza inicializar si hay operaciones.
[seed_finance_demo.py](../../ops/seed_finance_demo.py) agrega Caja/Banco y medios de ejemplo sólo después,
sin credenciales bancarias ni pagos/asientos. Ambos mantienen cron/correo desactivados.

## Acceso y mantenimiento

Iniciá Odoo con su servicio y verificá login, módulos, ayuda y arranque. Configurá HTTPS propio antes de
publicar acceso, con proxy_mode sólo detrás del proxy controlado. No habilites listado de bases ni
servicios externos por copiar la demo. Para LAN/homelab podés mantener acceso privado sin túnel externo.

Separá la base de ejemplo de una instalación con datos definitivos. Usá [respaldo y recuperación](../tecnica/OPERACION-Y-RECUPERACION.md)
y [exportación abierta](../tecnica/exportacion.md). Conservá revisión de código, DB, filestore y configuración
como conjunto. HTTP 200 prueba disponibilidad; los recorridos funcionales se revisan después de instalar.

[Primeros pasos](MANUALES.md) · [Volver](README.md).

## Actualizar desde 0.1.0-dev completa

Con respaldo consistente/restaurable, servicio detenido y configuración privada, actualizar los
nueve módulos de esta corrección como conjunto. No copiar sólo el consumidor sobre Documentos anterior.

```sh
sudo -u odoo odoo server -c /etc/odoo/odoo.conf -d arg_demo \
  --update=arg_pyme_base,arg_pyme_ui,arg_pyme_documentos,arg_pyme_ventas,arg_pyme_compras,arg_pyme_stock,arg_pyme_ventas_stock,arg_pyme_compras_stock,arg_pyme_informes \
  --without-demo=True --stop-after-init --workers=0 --max-cron-threads=0 --no-http
```

Para servicios sin Stock, actualizar sólo las capacidades ya instaladas: Base, UI, Documentos,
Ventas, Compras e Informes. No agregar Stock/puentes por usar el comando del perfil completo.
AJU migra únicamente una definición antigua sin identidades; si el registro ya tiene identidades
antiguas, se detiene con explicación para una migración explícita. No se renumeran documentos.
Verificar versiones y arranque antes de retomar escrituras; la QA de circuitos es una fase posterior.

[Conservar o retirar los ejemplos](../ejemplos/RETIRAR-EJEMPLOS.md) antes de planificar una migración real.
