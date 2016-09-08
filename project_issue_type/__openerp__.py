# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Project Issue type',
    'version': '9.0.1.0',
    'category': 'Project Management',
    'sequence': 9,
    'summary': 'Project Issue',
    'author': 'ClearCorp',
    'website': 'http://clearcorp.cr',
    'depends': ['project_issue',],
    'data': ['views/project_issue_type_view.xml','security/ir.model.access.csv'],
    'test' : [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}