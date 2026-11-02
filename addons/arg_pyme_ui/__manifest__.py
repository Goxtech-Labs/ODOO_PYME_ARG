{
 'name': 'Interfaz ARG', 'summary': 'Gestión documental simple, identidad argentina y ayuda central',
 'version': '20.0.1.1.5', 'author': 'Gonzalo Sarubilo · GoxtechLabs', 'license': 'AGPL-3',
 'website': 'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
 'depends': ['arg_pyme_base', 'web', 'mail_bot'],
 'data': ['views/help_support.xml', 'data/branding.xml', 'views/login.xml', 'views/preferences.xml', 'views/brand_layout.xml'],
 'assets': {'web._assets_primary_variables': [
    ('before', 'web/static/src/scss/primary_variables.scss', 'arg_pyme_ui/static/src/scss/brand_variables.scss')],
    'web._assets_secondary_variables': [
    ('after', 'web/static/src/scss/secondary_variables.scss', 'arg_pyme_ui/static/src/scss/palette_extensions.scss')],
    'web.assets_backend': ['arg_pyme_ui/static/src/navigation/areas.js',
    'arg_pyme_ui/static/src/navigation/areas.xml', 'arg_pyme_ui/static/src/components/document_actions.js',
    'arg_pyme_ui/static/src/components/document_matrix.xml', 'arg_pyme_ui/static/src/scss/tokens.scss']},
 'post_init_hook': 'post_init_hook', 'application': False, 'installable': True,
}
