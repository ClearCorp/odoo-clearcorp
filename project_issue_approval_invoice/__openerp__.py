# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": 'Project issue approval invoice',
    "version": '8.0.1.0',
    "author": 'ClearCorp',
    "summary": """Approval invoice""",
    'category': 'Projects',
    'sequence': 10,
    'website': 'http://clearcorp.cr',
    'depends': ['base', 'project_issue_approved', 'project_issue_multi_task'],
    'data': ['views/project_issue_approval_invoice.xml'],
    'auto_install': False,
    'application': False,
    'installable': True,
    'license': 'AGPL-3',
}
