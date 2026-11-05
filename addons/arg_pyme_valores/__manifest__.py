{
    'name': 'Cartera de valores ARG',
    'summary': 'Identidad y registro de cheques y pagarés; extensión de tesorería argentina',
    'version': '20.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Gonzalo Sarubilo · GoxtechLabs',
    'website': 'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
    'depends': ['arg_pyme_administracion', 'arg_pyme_documentos'],
    'data': ['security/ir.access.csv', 'views/value_views.xml'],
    'post_init_hook': 'post_init_hook',
    'installable': True,
}
