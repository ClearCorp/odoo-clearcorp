# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": 'Project Scrum',
    "version": '9.0.1.0',
    "author": 'ClearCorp',
    'complexity': 'normal',
    "description": """
""",
    "category": 'Project Management',
    "sequence": 3,
    "website": "http://clearcorp.co.cr",
    "images": [],
    "depends": [
                 'project',
                 'project_task_state',
                 ],
    "data": [
        'security/ir.model.access.csv',
        'data/project_scrum_data.xml',
        'views/project_scrum_view.xml',
        'views/project_scrum_menu.xml',
    ],
    "css": ['static/src/css/project_scrum.css'],
    "init_xml": [],
    "demo_xml": [],
    "update_xml": [],
    "test": [],
    "auto_install": False,
    "application": False,
    "installable": True,
    'license': 'AGPL-3',
}
