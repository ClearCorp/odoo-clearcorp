# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner Defaulter',
    'summary': 'Identify defaulters',
    'version': '8.0.1.0',
    'category': 'Extra Tools',
    'website': 'http://clearcorp.cr',
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'base',
        'account',
        'sale',
    ],
    'data': [
        'views/partner_defaulter_view.xml',
        'security/partner_defaulter_security.xml'
    ],
}
