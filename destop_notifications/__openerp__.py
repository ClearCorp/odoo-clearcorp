# -*- coding: utf-8 -*-
# © <YEAR(S)> ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Desktop Notifications',
    'summary': 'Desktop notifications',
    'version': '8.0.1.0',
    'category': 'Mail',
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
        'base', 'mail'
    ],
    'data': [
        "views/assets.xml",
        "views/report_name.xml",
        "views/model_name_view.xml",
        "wizards/wizard_model_view.xml",
    ],
    'demo': [],
    'qweb': [
        "static/src/xml/module_name.xml",
    ],
}
