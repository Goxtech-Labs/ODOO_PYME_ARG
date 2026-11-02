{
 'name': 'Interfaz ARG', 'summary': 'Gestión documental simple, identidad argentina y ayuda central',
 'version': '20.0.1.0.1', 'author': 'Gonzalo Sarubilo · GoxtechLabs', 'license': 'AGPL-3',
 'website': 'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
 'depends': ['arg_pyme_base', 'web', 'mail_bot'],
 'data': ['views/help_support.xml', 'data/branding.xml'],
 'assets': {'web.assets_backend': ['arg_pyme_ui/static/src/navigation/areas.js',
    'arg_pyme_ui/static/src/navigation/areas.xml', 'arg_pyme_ui/static/src/components/document_actions.js',
    'arg_pyme_ui/static/src/components/document_matrix.xml', 'arg_pyme_ui/static/src/scss/tokens.scss']},
 'post_init_hook': 'post_init_hook', 'application': False, 'installable': True,
}
