# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": 'Project Deadline Color',
    "version": '9.0.1.0',
    "author": 'ClearCorp',
    'complexity': 'easy',
    "description": """Adds a red tag if the task is about to reach its
    deadline.""",
    'category': 'Project Management',
    'sequence': 4,
    'website': 'http://clearcorp.co.cr',
    'depends': [
        'base', 'project', 'project_task_state', 'base_action_rule'
    ],
    'data': [
        'data/project_deadline_tag.xml',
        'data/project_deadline_auto_action.xml'
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
    'license': 'AGPL-3',
}
