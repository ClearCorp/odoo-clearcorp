# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProjectIssue(models.Model):

    _inherit = 'project.issue'

    priority = fields.Selection(
        selection_add=[('0', 'None'), ('1', 'Very low'), ('2', 'Low'),
                       ('3', 'Normal'), ('4', 'High'), ('6', 'Very high')])
