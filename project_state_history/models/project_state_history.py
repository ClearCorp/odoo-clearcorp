# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class ProjectStateHistory(models.Model):

    _name = 'project.state.history'

    @api.one
    @api.depends('date', 'project_id')
    def _compute_value(self):
        last_history = self.search([
            ('project_id', '=', self.project_id.id),
            ('date', '<', self.date)], order='date DESC', limit=1)
        if last_history:
            now = datetime.strptime(self.date,
                                    DEFAULT_SERVER_DATETIME_FORMAT)
            last = datetime.strptime(last_history.date,
                                     DEFAULT_SERVER_DATETIME_FORMAT)
            self.value = (((now - last).days * 24.0 * 60.0) +
                          (now - last).seconds / 60.0) / 60.0
        else:
            self.value = 0.0

    state_from = fields.Selection([
        ('template', 'Template'), ('draft', 'New'), ('open', 'In Progress'),
        ('cancelled', 'Cancelled'), ('pending', 'Pending'),
        ('close', 'Closed')], 'Status from', required=True, copy=False)
    state_to = fields.Selection([
        ('template', 'Template'), ('draft', 'New'), ('open', 'In Progress'),
        ('cancelled', 'Cancelled'), ('pending', 'Pending'),
        ('close', 'Closed')], 'Status to', required=True, copy=False)

    date = fields.Datetime(
        'Date', default=lambda self: fields.Datetime.now(), required=True)
    project_id = fields.Many2one('project.project', 'Project', required=True)
    value = fields.Float('Value', store=True, compute='_compute_value')


class Project(models.Model):

    _inherit = 'project.project'

    state_history_ids = fields.One2many(
        'project.state.history', 'project_id', string='State history',
        readonly=True)

    @api.multi
    def write(self, values):
        if ('state' in values.keys()):
            state_history_obj = self.env['project.state.history']
            state_to = values['state']
            for project in self:
                state_from = project.state
                state_history_dic = {'state_from': state_from,
                                     'state_to': state_to,
                                     'project_id': project.id
                                     }
                state_history_obj.create(state_history_dic)
            return super(Project, self).write(values)
        else:
            return super(Project, self).write(values)
