{
    'name': 'AK Product Catalog PDF',
    'author': 'Moin Musa',
    'version': '18.0.1.0.0',
    'summary': 'AK Product Catalog PDF',
    'website': 'https://www.aktivsoftware.com',
    'description': """  print product details as a catalog report.    """,
    'depends': [
        'base',
        'sale_management',
    ],
    'data': [
        # security files
        'security/ir.model.access.csv',

        # wizards
        'wizard/product_catalog_wizard_views.xml',

        # views
        'views/sales_menus.xml',

        # reports views
        'report/product_catalog_report_views.xml',
        'report/ir_report_actions.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
