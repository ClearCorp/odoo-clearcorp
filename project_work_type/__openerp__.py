# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name" : 'Project Work Type',
    "version" : '9.0.1.0',
    "author" : 'ClearCorp',
    'complexity': 'easy',
    "description": """""",
    'category': 'Project Management',
    'sequence': 4,
    'website' : 'http://clearcorp.co.cr',
    'depends' : ['base','project'],
    'data': [
             'security/project_security.xml', 'views/project_work_type_view.xml',
             'security/ir.model.access.csv'],
    'auto_install': False,
    'application': False,
    'installable': True,
    'license': 'AGPL-3',
}