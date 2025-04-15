# -*- coding: utf-8 -*-
{
    'name': 'Library Management',
    'author': 'Moin Musa',
    'version': '18.0.1.2.3',
    'summary': 'Manages books,books category and members at library',
    'website': 'https://www.aktivsoftware.com',
    'description': """
    manage books & members
    Manges books with its categories.
    Manges member at library.
    """,
    'depends': [
        'sale_stock',
        'contacts',
        'base_automation',
        'hr',
        'website_sale',
        'point_of_sale',
        'sale_purchase',
    ],
    'data': [
        #security files
        'security/security.xml',
        'security/ir.model.access.csv',

        #custom report files which reference use in data/mail_template_data.xml
        'report/library_member_report_template.xml',

        #data files
        'data/ir_sequence.xml',
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',

        #views files
        'views/library_book_views.xml',
        'views/library_book_category_views.xml',
        'views/library_member_views.xml',
        'views/library_library_views.xml',
        'views/library_book_tags_views.xml',
        'views/library_multiple_books_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
        'views/borrow_transaction_history_views.xml',
        'views/res_users_views.xml',
        'views/library_menuitem.xml',
        'views/stock_warehouse_views.xml',
        'views/res_config_settings_views.xml',
        'views/contacts_template.xml',
        'views/customer_page.xml',
        'views/website_templates.xml',
        'views/product_product_views.xml',

        #wizard files
        'wizard/sale_order_validation_wizard_views.xml',
        'wizard/borrow_books_checklist_wizard_views.xml',
        'wizard/borrow_transaction_history_wizard_views.xml',

        #report files
        'report/library_library_report_template.xml',
        'report/report_custom_invoice.xml',

    ],
    'assets':{
        'web.assets_frontend': [
            'ak_library_management/static/src/js/customer_fetch.js',
        ],
        'point_of_sale._assets_pos': [
            'ak_library_management/static/src/xml/product_card.xml',
            'ak_library_management/static/src/xml/product_screen.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
