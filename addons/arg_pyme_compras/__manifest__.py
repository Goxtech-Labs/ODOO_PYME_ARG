{
    'name': 'Compras ARG',
    'summary': 'Pedidos al proveedor y facturas recibidas con pendientes separados',
    'version': '20.0.1.0.5',
    'license': 'AGPL-3',
    'author': 'Gonzalo Sarubilo · GoxtechLabs',
    'website': 'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
    'depends': ['arg_pyme_base', 'arg_pyme_ui', 'arg_pyme_terceros',
                'arg_pyme_catalogo', 'arg_pyme_documentos', 'purchase'],
    'data': ['security/roles.xml', 'security/ir.access.csv',
             'views/purchase_order_views.xml', 'views/account_move_views.xml',
             'wizard/purchase_bill_views.xml'],
    'installable': True,
}
