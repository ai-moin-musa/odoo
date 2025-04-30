# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Enhance Product Page',
    'author': 'Moin Musa',
    'version': '18.0.1.0.0',
    'summary': 'Enhance Product Page',
    'website': 'https://www.aktivsoftware.com',
    'description': """ enhance the product page on the Odoo website to
                    allow logged-in users to rate products and submit reviews. 
                    This data should be stored in the backend under the respective 
                    product template and displayed on the same product page. """,
    'depends': [
        'website_sale',
    ],
    'data': [
        # security files
        'security/ir.model.access.csv',

        # views
        'views/templates.xml',
        'views/product_review_views.xml',
        'views/menu_items.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
