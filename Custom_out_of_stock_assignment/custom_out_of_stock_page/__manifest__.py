# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Custom Out Of Stock Page',
    'author': 'Moin Musa',
    'version': '18.0.1.0.0',
    'summary': 'Custom out of stock page',
    'website': 'https://www.aktivsoftware.com',
    'description': """Enhance the Odoo Website Shop functionality by adding a custom out-of-stock page for products that are unavailable.""",
    'depends': [
        'sale_management',
        'website_sale',
    ],
    'data': [
        # security files
        'security/ir.model.access.csv',

        # views files
        'views/product_template_views.xml',
        'views/website_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
