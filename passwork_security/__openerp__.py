# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Password Security',
    'summary': 'Password security configurations',
    'version': '8.0.1.0',
    'category': 'Hidden',
    'website': 'http://clearcorp.cr',
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'depends': [
        'base_setup', 'auth_signup', 'web'
    ],
    'data': [
        'views/base_config_settings.xml'
    ],
    'qweb': [
    ],
}
