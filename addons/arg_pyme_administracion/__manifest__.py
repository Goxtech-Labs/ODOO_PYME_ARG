{
    'name': 'Administración ARG',
    'summary': 'Cuentas corrientes, recibos, pagos, anticipos y aplicaciones nativas',
    'version': '20.0.1.1.3',
    'license': 'AGPL-3',
    'author': 'Gonzalo Sarubilo · GoxtechLabs',
    'website': 'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
    'depends': ['arg_pyme_base', 'arg_pyme_ui', 'arg_pyme_terceros', 'arg_pyme_documentos', 'account'],
    'data': ['security/roles.xml', 'security/ir.access.csv', 'views/current_account_views.xml',
             'views/treasury_document_views.xml', 'wizard/treasury_views.xml', 'views/cash_report_views.xml', 'data/help.xml'],
    'installable': True,
}
