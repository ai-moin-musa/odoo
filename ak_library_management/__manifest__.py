# -*- coding: utf-8 -*-
{
    'name': 'Ak Library Management',
    'version': '18.0.1.0.0',
    'summary': 'Manages books,books category and members at library',
    'website': 'https://www.aktivsoftware.com',
    'sequence': 10,
    'description': """
manage books & members
====================
Manges books with its categories.
Manges member at library.
    """,
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/ak_library_management_book_view.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
