from markupsafe import Markup

def post_init_hook(env):
    env['arg.pyme.ui.branding']._apply_identity()
    operator = env.ref('arg_pyme_base.group_operator')
    users = env['res.users'].search([('share','=',False)])
    users.filtered(lambda user: operator in user.all_group_ids).write({'action_id': env.ref('arg_pyme_ui.action_arg_home').id})
    resources = env['arg.pyme.help.resource']
    guides = {
      'arg_pyme_base': ('Base ARG', 'Configurá compañía y roles combinables. Los códigos se asignan automáticamente; no sustituyen números fiscales. Tutoriales y soporte se administran desde Configuración.'),
      'arg_pyme_ui': ('Interfaz ARG', 'Elegí circuito y documento. El orden es tercero, generales, detalle, totales y acciones. Guardar conserva cambios; confirmar, entregar, facturar y cobrar son acciones diferentes.'),
      'arg_pyme_terceros': ('Terceros ARG', 'Registrá nombre y rol. Una identidad puede ser cliente y proveedor. Completá datos fiscales cuando la operación los necesite.'),
      'arg_pyme_catalogo': ('Catálogo ARG', 'Creá producto o servicio con nombre y unidad. Revisá precio e impuestos conocidos. Las listas son nativas y las matrices piden revisar cambios antes de aplicarlos.'),
      'arg_pyme_ventas': ('Ventas ARG', 'Creá PRE, confirmá aceptación total o parcial y generá PED separado. Confirmá PED antes de entregar y facturar. Consultá pendientes de cada eje y sus documentos relacionados.'),
      'arg_pyme_compras': ('Compras ARG', 'Confirmá PPC, recibí lo efectivo mediante ENT y registrá FRC con número original de proveedor. La factura no vuelve a ingresar stock; el pago pertenece a Administración.'),
      'arg_pyme_stock': ('Stock ARG', 'Distinguí físico, reserva, disponible y previsto. Validá movimientos reales. INV registra conteo; AJU aplica diferencias con motivo, sin editar saldos manualmente.'),
      'arg_pyme_administracion': ('Administración ARG', 'Registrá REC u OPA, medio e importe. Aplicá total o parcial a documentos o conservá anticipo libre. Saldos y caja provienen de la contabilidad nativa.'),
      'arg_pyme_informes': ('Informes ARG', 'Elegí compañía, período y moneda. Ventas, entregas, cobros y deuda son hechos distintos. Abrí el origen de cada total; no sumes monedas o unidades incompatibles.'),
    }
    for module, (name, text) in guides.items():
        if not resources.search_count([('module_key','=',module),('task','=','inicio')]):
            resources.create({'name':name + ' · Primeros pasos', 'module_key':module, 'task':'inicio',
                              'manual_text':Markup('<p>%s</p>') % text, 'state':'planned', 'version_min':'20.0', 'version_max':'20.0'})
