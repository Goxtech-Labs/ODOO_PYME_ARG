{
 'name':'Terceros ARG', 'summary':'Clientes y proveedores sobre una identidad, con alta mínima',
 'version':'20.0.1.0.0', 'license':'AGPL-3', 'author':'Gonzalo Sarubilo · GoxtechLabs',
 'website':'https://github.com/Goxtech-Labs/ODOO_PYME_ARG',
 'depends':['arg_pyme_base','arg_pyme_ui','contacts'],
 'data':['security/ir.access.csv','data/roles.xml','views/res_partner_views.xml'],
 'post_init_hook':'post_init_hook','installable':True,
}
