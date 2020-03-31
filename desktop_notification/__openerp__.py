# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Desktop Notification',
    'summary': 'Desktop notification',
    'version': '8.0.1.0.1',
    'category': 'Social Network',
    'website': 'http://clearcorp.cr',
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'base', 'mail', 'im_chat'
    ],
    'data': [
        'views/assets.xml'
    ]
}
