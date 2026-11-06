{
    'name': 'Cartera de valores ARG',
    'summary': 'REC y OPA con cheques en papel, reservas, entregas y efectos bancarios separados',
    'version': '20.0.1.2.0',
    'license': 'AGPL-3',
    'author': 'Gonzalo Sarubilo · GoxtechLabs',
    'website': 'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
    'depends': ['arg_pyme_administracion', 'arg_pyme_documentos'],
    'data': ['security/ir.access.csv', 'data/help.xml', 'views/value_views.xml', 'views/treasury_value_views.xml', 'wizard/value_operation_views.xml'],
    'post_init_hook': 'post_init_hook',
    'installable': True,
}
