# -*- coding: utf-8 -*-
{
    'name': 'CRM Customization',
    'author': 'Moin Musa',
    'version': '18.0.1.0.0',
    'summary': 'CRM Customization',
    'website': 'https://www.aktivsoftware.com',
    'description': """
    CRM Customization
    """,
    'depends': [
        'mrp',
        'crm',
        'project',
        'sale_project',
        'account',
    ],
    'data': [
        # security files
        'security/ir.model.access.csv',

        # views files
        'views/sale_order_views.xml',
        'views/mrp_production_views.xml',
        'views/stock_picking_views.xml',
        'views/project_project_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
