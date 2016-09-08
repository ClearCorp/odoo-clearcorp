# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class Task(models.Model):
    _inherit = 'project.task'

    @api.one
    @api.depends('date_deadline', 'date_start')
    def add_urgent_tag(self):
        # xmlid is not the external id, but the complete id
        res_id = self.env['ir.model.data'].xmlid_to_res_id(
            'project_deadline_color.project_deadline_tag_data')
        self.write({'tag_ids': [(4, res_id)]})
