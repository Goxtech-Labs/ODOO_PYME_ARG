{
    'name': 'Base ARG', 'summary': 'Identidad documental, roles, ayuda y soporte comunitario',
    'version': '20.0.1.0.5', 'category': 'Administration',
    'author': 'Gonzalo Sarubilo · GoxtechLabs', 'license': 'AGPL-3',
    'website': 'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
    'depends': ['base', 'web'],
    'data': ['security/roles.xml', 'security/ir.access.csv',
             'views/document_type_views.xml', 'views/help_support_views.xml',
             'views/res_users_views.xml', 'views/menu_views.xml'],
    'post_init_hook': 'post_init_hook', 'application': True, 'installable': True,
}
