# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ProjectScrumFeature(models.Model):

    _inherit = 'project.scrum.feature'

    state = fields.Selection([('draft', 'New'), ('open', 'In Progress'),
                             ('cancelled', 'Cancelled'), ('done', 'Done'),
                             ('quote_pending', 'Quote Pending'),
                             ('quoted', 'Quoted')],
                             'Status', required=True)

    @api.multi
    def set_quote_pending(self):
        print "set quote pending"
        for feature in self:
            feature.write({'state': 'quote_pending'})

    @api.multi
    def set_quoted(self):
        print "\nset quoted"
        for feature in self:
            feature.write({'state': 'quoted'})
            for ticket in self.tickets_ids:
                appr = ticket._create_approvals()
                print "\n approva create: ", appr
