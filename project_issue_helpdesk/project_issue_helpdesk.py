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

from openerp.osv import osv,fields, orm
from openerp.tools.translate import _
import math

class ProjectIssue(osv.Model):
    _inherit = 'project.issue'
    _columns = {
                'issue_type': fields.selection([('support','Support'),('preventive check','Preventive Check'),
                                              ('workshop repair','Workshop Repair'),('installation','Installation')],
                                             required=True,string="Issue Type"),
                'warranty': fields.selection([('seller','Seller'),('manufacturer','Manufacturer')],string="Warranty")                                 
                }

class HrAnaliticTimeSheet(osv.Model):
    _inherit = 'hr.analytic.timesheet'
    _columns = {
                'ticket_number': fields.char(required=True,string="Ticket Number"),
                'start_time': fields.float(required=True,string="Start Time"),
                'end_time': fields.float(required=True,string="End Time"),
                'service_type': fields.selection([('expert','Expert'),('assistant','Assistant')],required=True,string="Service Type")
                          
                }
    def _check_start_time(self, cr, uid, ids, context={}):
        for timesheet_obj in self.browse(cr, uid, ids, context=context):
            if timesheet_obj.start_time:
                hour = math.floor(timesheet_obj.start_time)
                min = round((timesheet_obj.start_time % 1) * 60)
            if (hour not in range(0,24) or min not in range(0,60)):
                return False
        return True
    
    def _check_end_time(self, cr, uid, ids, context={}):
        for timesheet_obj in self.browse(cr, uid, ids, context=context):
            if timesheet_obj.end_time:
                hour = math.floor(timesheet_obj.end_time)
                min = round((timesheet_obj.end_time % 1) * 60)
            if (hour not in range(0,24) or min not in range(0,60)):
                return False
        return True
    
    _constraints = [
        (_check_start_time,'Format Start Time incorrect',['start_time']
         ),
         (_check_end_time,'Format End Time incorrect',['end_time']
         )]