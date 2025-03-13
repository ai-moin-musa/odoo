# -*- coding: utf-8 -*-
{
    'name': 'Library Management',
    'author': 'Moin Musa',
    'version': '18.0.2.8.0',
    'summary': 'Manages books,books category and members at library',
    'website': 'https://www.aktivsoftware.com',
    'description': """
    manage books & members
    Manges books with its categories.
    Manges member at library.
    """,
    'depends': ['stock', 'contacts', 'sale_management', 'base_automation'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_book_category_views.xml',
        'views/library_member_views.xml',
        'views/library_library_views.xml',
        'views/library_book_tags_views.xml',
        'views/library_multiple_books_views.xml',
        'views/product_template_views.xml',
        'data/ir_sequence.xml',
        'data/ir_cron_data.xml',
        'wizard/sale_order_validation_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
        'views/borrow_transaction_history_views.xml',
        'wizard/borrow_books_checklist_wizard_views.xml',
        'views/res_users_views.xml',
        'views/library_menuitem.xml',
        'data/mail_template_data.xml',
        'report/library_library_report_template.xml',
        'report/library_member_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
