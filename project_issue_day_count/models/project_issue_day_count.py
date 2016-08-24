# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime


class ProjectIssue(models.Model):

    _inherit = 'project.issue'

    @api.one
    @api.depends('date_deadline')
    def _compute_day_count(self):
        if self.date_deadline:
            today = fields.date.today()
            deadline = datetime.strptime(self.date_deadline,
                                         DEFAULT_SERVER_DATE_FORMAT).date()
            self.day_count = (deadline - today).days

    day_count = fields.Integer('Amount of days',
                               compute='_compute_day_count')
