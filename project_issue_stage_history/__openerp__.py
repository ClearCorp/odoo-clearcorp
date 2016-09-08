# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Project Issue Stage Histoy',
    'version': '9.0.1.0',
    'category': 'Project Management',
    'sequence': 10,
    'summary': 'Allows saving issue stage changes',
    'author': 'ClearCorp',
    'website': 'http://clearcorp.cr',
    'depends': ['project_issue'],
    'data': [
             'views/project_issue_stage_history.xml',
             'security/ir.model.access.csv',
             ],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
