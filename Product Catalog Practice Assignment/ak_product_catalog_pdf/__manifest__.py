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

        # views
        'views/sales_menus.xml',

        # reports views
        'report/product_catalog_report_views.xml',

        # wizards
        'wizard/product_catalog_wizard_views.xml',

    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
# -*- coding: utf-8 -*-











































