# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields


class Task(models.Model):

    _inherit = 'project.task'

    # Creates 4 more priorities, not only 'Normal' and 'High'
    # Changed priority 'Very high' to 5, instead of 6
    priority = fields.Selection(
        selection_add=[('0', 'None'), ('1', 'Very low'), ('2', 'Low'),
                       ('3', 'Normal'), ('4', 'High'), ('5', 'Very high')])
