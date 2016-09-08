# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProjectIssue(models.Model):
    _inherit = 'project.issue'
    task_ids = fields.Many2many('project.task', string='Tasks')


class ProjectTask(models.Model):
    _inherit = 'project.task'
    tickets_ids = fields.Many2many('project.issue', string='Tickets')
