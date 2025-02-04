# -*- coding: utf-8 -*-
{
    'name': 'Library Management',
    'author': 'Moin Musa',
    'version': '18.0.1.0.0',
    'summary': 'Manages books,books category and members at library',
    'website': 'https://www.aktivsoftware.com',
    'description': """
    manage books & members
    ====================
    Manges books with its categories.
    Manges member at library.
    """,
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_book_category_views.xml',
        'views/library_member_views.xml',
        'views/library_library_views.xml',
        'views/library_book_tags_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
