{
    'name': 'Stock ARG', 'summary': 'Existencias, movimientos e inventarios documentales',
    'version': '20.0.1.0.4', 'license': 'AGPL-3',
    'author': 'Gonzalo Sarubilo · GoxtechLabs',
    'website': 'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
    'depends': ['arg_pyme_base', 'arg_pyme_ui', 'arg_pyme_catalogo', 'arg_pyme_documentos', 'stock'],
    'data': ['security/roles.xml', 'security/ir.access.csv', 'views/stock_matrix_views.xml',
             'views/stock_picking_views.xml', 'views/inventory_count_views.xml'],
    'assets': {'web.assets_backend': ['arg_pyme_stock/static/src/stock_matrix.js', 'arg_pyme_stock/static/src/stock_matrix.xml']},
    'installable': True,
}
