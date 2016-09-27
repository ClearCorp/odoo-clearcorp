# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name" : 'Project scrum feature work estimate',
    "version" : '9.0.1.0',
    "author" : 'ClearCorp',
    "category": 'Project Management',
    "sequence": 10,
    "website" : "http://clearcorp.cr",
    "depends" : [
                   'project_scrum_method',
                   'project_work_type',
                   'project_timesheet'
                   'hr',
                 ],
    "data" : [
              'views/project_scrum_feature_work_est_view.xml',
              'security/ir.model.access.csv',
              ],
    "demo_xml" : [],
    "test" : [],
    "auto_install": False,
    "application": False,
    "installable": True,
    'license': 'AGPL-3',
}
