{
 'name':'Documentos ARG', 'summary':'Identidad, vínculos, parciales e impresión comunes',
 'version':'20.0.1.0.5', 'license':'AGPL-3', 'author':'Gonzalo Sarubilo · GoxtechLabs',
 'website':'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
 'depends':['arg_pyme_base','arg_pyme_ui','web'],
 'data':['data/help.xml','views/document_header.xml','views/document_links.xml','report/document_templates.xml'],
 'assets':{'web.assets_backend':['arg_pyme_documentos/static/src/document_widgets.js',
                                'arg_pyme_documentos/static/src/document_widgets.xml']},
 'post_init_hook':'post_init_hook','installable':True,
}
