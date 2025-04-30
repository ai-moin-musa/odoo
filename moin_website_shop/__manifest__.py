# -*- coding: utf-8 -*-
{
    'name': 'Moin Website Shop',
    'author': 'Moin Musa',
    'version': '18.0.1.0.0',
    'summary': 'Moin Website Shop',
    'website': 'https://www.aktivsoftware.com',
    'description': """
    Enhance the Odoo Website Shop Page by adding an "Add to Cart" button and displaying the On-Hand Quantity of each product.
    """,
    'depends': [
        'website_sale',
        'stock',
    ],
    'data': [
        # security files
        'security/ir.model.access.csv',

        #views files
        'views/templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
