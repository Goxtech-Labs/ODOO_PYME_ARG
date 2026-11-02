{
 'name':'Ventas ARG','summary':'Presupuestos propios y pedidos independientes con parciales',
 'version':'20.0.1.0.5','license':'AGPL-3','author':'Gonzalo Sarubilo · GoxtechLabs',
 'website':'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
 'depends':['arg_pyme_base','arg_pyme_ui','arg_pyme_terceros','arg_pyme_catalogo','arg_pyme_documentos','sale_management'],
 'data':['security/roles.xml','security/ir.access.csv','views/quotation_views.xml',
         'views/sale_order_views.xml','views/sale_document_links.xml','wizard/quotation_operation_views.xml'],
 'installable':True,
}
