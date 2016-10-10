# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    "name": 'Subscription Prepaid Hours',
    "version": '9.0.1.0',
    "author": 'ClearCorp',
    "summary": """Prepaid hours""",
    'category': 'Projects',
    'sequence': 10,
    'website': 'http://clearcorp.cr',
    'depends': [
        'base', 'project_work_type', 'account_analytic_analysis',
        'sale_contract'],
    'data': [
        'views/subscription_prepaid_hours_view.xml',
        'data/subscription_prepaid_hours_data.xml'
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
    'license': 'AGPL-3',
}
