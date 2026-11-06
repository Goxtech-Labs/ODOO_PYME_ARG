{
    'name': 'Reparaciones ARG',
    'summary': 'Recepción de equipos ajenos y diagnóstico con carga mínima',
    'version': '20.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Gonzalo Sarubilo · GoxtechLabs',
    'website': 'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
    'depends': ['arg_pyme_ventas', 'arg_pyme_stock', 'arg_pyme_documentos'],
    'data': ['security/roles.xml', 'security/ir.access.csv', 'data/help.xml',
             'views/repair_views.xml', 'wizard/repair_return_views.xml', 'report/repair_document.xml'],
    'post_init_hook': 'post_init_hook',
    'installable': True,
}
