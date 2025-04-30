# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sale Order Approval',
    'author': 'Moin Musa',
    'version': '18.0.1.0.0',
    'summary': 'Sale Order Approval',
    'website': 'https://www.aktivsoftware.com',
    'description': """ Sale Order Approval """,
    'depends': [
        'sale_management',
    ],
    'data': [
        # security files
        'security/ir.model.access.csv',

        # views files
        'views/res_config_settings_views.xml',
        'views/sales_manager_approval_views.xml',
        'views/sale_order_views.xml',
        'views/menu_items.xml',

        # data files
        'data/mail_template_data.xml',
        'data/ir_cron_data.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
