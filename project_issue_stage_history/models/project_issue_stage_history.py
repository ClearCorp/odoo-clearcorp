# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class ProjectIssueStageHistory(models.Model):

    _name = 'project.issue.stage.history'

    @api.multi
    @api.depends('date', 'issue_id')
    def _compute_elapsed_time(self):
        last_history = self.search([
            ('issue_id', '=', self.issue_id.id),
            ('date', '<', self.date)], order='date DESC', limit=1)
        if last_history:
            now = datetime.strptime(self.date,
                                    DEFAULT_SERVER_DATETIME_FORMAT)
            last = datetime.strptime(last_history.date,
                                     DEFAULT_SERVER_DATETIME_FORMAT)
            self.elapsed_time = (((now - last).days * 24.0 * 60.0) +
                                 (now - last).seconds / 60.0) / 60.0
        else:
            self.elapsed_time = 0.0

    stage_from_id = fields.Many2one('project.task.type', 'Previous Stage',
                                    select=True, copy=False)
    stage_to_id = fields.Many2one('project.task.type', 'Succeding Stage',
                                  select=True, copy=False)
    date = fields.Datetime(
        'Date', default=lambda self: fields.Datetime.now(), required=True)
    issue_id = fields.Many2one(
        'project.issue', 'Issue', required=True, ondelete='cascade')
    elapsed_time = fields.Float(
        'Elapsed time', store=True, compute='_compute_elapsed_time')


class ProjectIssue(models.Model):

    _inherit = 'project.issue'

    issue_stage_history_ids = fields.One2many(
        'project.issue.stage.history', 'issue_id', string='Stage History',
        readonly=True)

    @api.multi
    def write(self, values):
        if 'stage_id' in values.keys():
            stage_history_obj = self.env['project.issue.stage.history']
            stage_to_id = values['stage_id']
            for issue in self:
                stage_from_id = issue.stage_id.id
                stage_history_dic = {'stage_from_id': stage_from_id,
                                     'stage_to_id': stage_to_id,
                                     'issue_id': issue.id
                                     }
                stage_history_obj.create(stage_history_dic)
            return super(ProjectIssue, self).write(values)
        else:
            return super(ProjectIssue, self).write(values)
