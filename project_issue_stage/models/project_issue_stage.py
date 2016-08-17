# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import Warning
from datetime import date


class project_issue_type(models.Model):
    _inherit = 'project.task.type'
    
    type = fields.Selection([('task', 'Task'), ('issue', 'Issue'),
                             ('both', 'Both')], 'Stage type', required=True)
