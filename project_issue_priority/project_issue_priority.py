# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by CLEARCORP S.A.
#    Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api


class ProjectIssue(models.Model):

    _inherit = 'project.issue'

    priority = fields.Selection(
        selection_add=[('0', 'None'), ('1', 'Very low'), ('2', 'Low'),
                       ('3', 'Normal'), ('4', 'High'), ('6', 'Very high')])

    @api.multi
    def write(self, vals):
        self.env['bus.bus'].create(
            {
                'message': '{"create_date":"2016-03-02 18:10:15","to_id":[6,"808c863d-a0a1-436c-b371-28fbb11dc6e5"],"message":"project.issue","type":"message","id":246,"from_id":[1,"Administrator"]}',
                'channel': '["cc_notificaciones","im_chat.session",5]'
            })
        self.env['bus.bus'].create(
            {
                'message': '{"create_date":"2016-03-02 18:10:15","to_id":[6,"108c863d-a0a1-436c-b371-28fbb11dc6e5"],"message":"project.issue","type":"message","id":246,"from_id":[1,"Administrator"]}',
                'channel': '["cc_notificaciones","im_chat.session",4]'
            })
        return models.Model.write(self, vals)
