# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ProjectScrumFeature(models.Model):

    _inherit = 'project.scrum.feature'

    # Adds two quote states to feature state
    state = fields.Selection([('draft', 'New'), ('open', 'In Progress'),
                             ('cancelled', 'Cancelled'), ('done', 'Done'),
                             ('quote_pending', 'Quote Pending'),
                             ('quoted', 'Quoted')],
                             'Status', required=True)
