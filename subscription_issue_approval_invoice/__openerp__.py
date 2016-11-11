# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": 'Subscription Issue Approval Invoice',
    "version": '9.0.1.0',
    "author": 'ClearCorp',
    "summary": """Approval invoice""",
    'category': 'Projects',
    'sequence': 10,
    'website': 'http://clearcorp.cr',
    'depends': ['base', 'subscription_issue_approval',
                'project_issue_multi_task'
                'account'],
    'data': ['views/subscription_issue_approval_invoice_view.xml'],
    'auto_install': False,
    'application': False,
    'installable': True,
    'license': 'AGPL-3',
}
