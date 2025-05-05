# -*- coding: utf-8 -*-
{
    'name': 'Enhance Contacts Webpage',
    'author': 'Moin Musa',
    'version': '18.0.1.0.0',
    'summary': 'Enhance Contacts Webpage',
    'website': 'https://www.aktivsoftware.com',
    'description': """ enhancing contacts webpage """,
    'depends': [
        'contacts',
        'website',
    ],
    'data': [
        # security files
        'security/ir.model.access.csv',

        # views files
        'views/contacts_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'en_contacts_webpage/static/src/js/contact_form.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
