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

from openerp.osv import fields, osv
from openerp.tools.translate import _

PRIORITY = {
            5: '4',
            4: '3',
            3: '2',
            2: '1',
            1: '0',
            }

class WorkType(osv.Model):
    
    _name = 'ccorp.project.oerp.work.type'
    
    _order = 'sequence'
    
    _columns = {
                'name': fields.char('name', size=128, required=True),
                'product_id': fields.many2one('product.product', string='Product', required='True'),
                'sequence': fields.integer('Sequence', required=True),
                'column_number': fields.integer('Column Number', required=True),
                }
    
class Sprint(osv.Model):

    _inherit = 'ccorp.project.scrum.sprint'

    def tasks_from_features_oerp(self, cr, uid, ids, context=None):
        task_obj = self.pool.get('project.task')
        task_hour_obj = self.pool.get('ccorp.project.oerp.task.hour')
        task_ids = []
        for sprint in self.browse(cr, uid, ids, context=context):
            for feature in sprint.feature_ids: 
                department_ids = []
                for feature_hours in feature.hour_ids:
                    department_ids.append(feature_hours.department_id.id)
                department_ids = list (set(department_ids))
                for department_id in department_ids:
                    planned_hours = 0.0
                    for feature_hours in feature.hour_ids:
                        if feature_hours.department_id.id == department_id:
                            planned_hours += feature_hours.expected_hours
                    values = {
                          'project_id': sprint.project_id.id,
                          'product_backlog_id': sprint.product_backlog_id.id,
                          'release_backlog_id': sprint.release_backlog_id.id,
                          'sprint_id': False,
                          'feature_id': feature.id,
                          'user_id': uid,
                          'planned_hours': planned_hours,
                          'remaining_hours': planned_hours,
                          'date_start': sprint.date_start,
                          'date_end': sprint.deadline,
                          'date_deadline': sprint.deadline,
                          'priority': PRIORITY[feature.priority],
                          'description': feature.description,
                          'name': feature.code + ' ' + feature.name,
                          'is_scrum': True,
                          }
                    task_id = task_obj.create(cr, uid, values, context=context)
                    task_ids.append(task_id)
                    for feature_hours in feature.hour_ids:
                        if feature_hours.department_id.id == department_id:
                            values = {
                                'task_id': task_id,
                                'project_id': sprint.project_id.id,
                                'work_type_id': feature_hours.work_type_id.id,
                                'expected_hours': feature_hours.expected_hours,
                            }
                            task_hour_obj.create(cr, uid, values, context=context)
        for id in task_ids:
            self.write(cr, uid, ids[0], {'desirable_task_ids': [[4, id]]}, context=context)
        return True
    
    
    def queue_tasks(self, cr, uid, ids, context=None):
        sprint = self.browse(cr, uid, ids[0], context=context)
        for task in sprint.desirable_task_ids:
                if not task.sprint_id:
                    task.write({'sprint_id': sprint.id}, context=context)
        return True
    

    _columns = {
                'planned_task_ids': fields.many2many('project.task', string='Desirable Tasks'),
                }

class FeatureHours(osv.Model):
    
    _name = 'ccorp.project.oerp.feature.hours'
   
   
    def _effective_hours(self, cr , uid, ids, field_name, arg, context=None):
        res = {}
        for hour in self.browse(cr, uid, ids, context=context):
            task_obj = self.pool.get('project.task')
            task_ids = task_obj.search(cr, uid, [('feature_id', '=', hour.feature_id.id)], context=context)
            tasks = task_obj.browse(cr, uid, task_ids, context=context)
            sum = 0.0
            for task in tasks:
                for work in task.work_ids:
                    if work.work_type_id == hour.work_type_id:
                        sum += work.hours
            res[hour.id] = sum
        return res
    
    def _remaining_hours(self, cr , uid, ids, field_name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = task.expected_hours - task.effective_hours
        return res


    
    _columns = {
                'feature_id': fields.many2one('ccorp.project.scrum.feature', string='Feature', required=True,
                    ondelete='cascade'),
                'work_type_id': fields.many2one('ccorp.project.oerp.work.type', string='Work Type'),
                'expected_hours': fields.float('Planned Hour(s)', required=True),
                'effective_hours': fields.function(_effective_hours, type='float', string='Spent Hour(s)', store=True),
                'remaining_hours': fields.function(_remaining_hours, type='float', string='Remaining Hour(s)', store=True),
                }
    
    _defaults = {
                 'feature_id': lambda slf, cr, uid, ctx: ctx.get('feature_id', False),
                 }
    
class Feature(osv.Model):
    
    _inherit = 'ccorp.project.scrum.feature'
    
    _columns = {
                'hour_ids': fields.one2many('ccorp.project.oerp.feature.hours', 'feature_id', string='Feature Hours'),
                'acceptance_requirements_client': fields.text('Acceptance requirements by client'),
                'acceptance_requirements_supplier': fields.text('Funtional acceptance requirements'),
                'issue_id': fields.one2many('project.issue','feature_id', string='Issue'),
                }
    
    def write(self, cr, uid, ids, values, context=None):
        if 'hour_ids' in values:
            hours = values['hour_ids']
            sum = 0.0
            for hour in hours:
                id = hour[1]
                vals = hour[2]
                if vals: 
                    if 'expected_hours' in vals:
                        sum += vals['expected_hours']
                else:
                    hour_obj = self.pool.get('ccorp.project.oerp.feature.hours')
                    sum += hour_obj.browse(cr, uid, id, context=context).expected_hours
            values['expected_hours'] = sum
        return super(Feature, self).write(cr, uid, ids, values, context=context)
    
    def create(self, cr, uid, values, context=None):
        if 'hour_ids' in values:
            hours = values['hour_ids']
            sum = 0.0
            for hour in hours:
                id = hour[1]
                vals = hour[2]
                if vals: 
                    if 'expected_hours' in vals:
                        sum += vals['expected_hours']
                else:
                    hour_obj = self.pool.get('ccorp.project.oerp.feature.hours')
                    sum += hour_obj.browse(cr, uid, id, context=context).expected_hours
            values['expected_hours'] = sum
        return super(Feature, self).create(cr, uid, values, context=context)
    
class TaskHours(osv.Model):
    
    _name = 'ccorp.project.oerp.task.hour'
    
    def _effective_hours(self, cr , uid, ids, field_name, arg, context=None):
        res = {}
        for hour in self.browse(cr, uid, ids, context=context):
            work_obj = self.pool.get('project.task.work')
            work_ids = work_obj.search(cr, uid, [('task_id', '=', hour.task_id.id),
                ('work_type_id', '=', hour.work_type_id.id)], context=context)
            works = work_obj.browse(cr, uid, work_ids, context=context)
            sum = 0.0
            for work in works:
                sum += work.hours
            res[hour.id] = sum
        return res
    
    def _remaining_hours(self, cr , uid, ids, field_name, arg, context=None):
        res = {}
        for hour in self.browse(cr, uid, ids, context=context):
            res[hour.id] = hour.expected_hours - hour.effective_hours
        return res
    
    _columns = {
                'task_id': fields.many2one('project.task', string='Task', required=True, ondelete='cascade'),
                'project_id': fields.related('task_id', 'project_id', type='many2one',
                    relation='project.project', string='Project'),
                'work_type_id': fields.many2one('ccorp.project.oerp.work.type', string='Work Type', required=True),
                'expected_hours': fields.float('Initially Planned Hour(s)', required=True),
                'effective_hours': fields.function(_effective_hours, type='float', string='Spent Hour(s)'),
                'remaining_hours': fields.function(_remaining_hours, type='float', string='Remaining Hour(s)'),
                }

    _defaults = {
                 'project_id': lambda slf, cr, uid, ctx: ctx.get('project_id', False),
                 'task_id': lambda slf, cr, uid, ctx: ctx.get('task_id', False),
                 }

class Task(osv.Model):
    
    _inherit = 'project.task'

    def onchange_sprint(self, cr, uid, ids, sprint_id, context=None):
       res = {}
       return res

    def _remaining_hours(self, cr , uid, ids, field_name, arg, context=None):
        res = {}
        effective_hours=0
        for task in self.browse(cr, uid, ids, context=context):
            for work in task.work_ids:
                effective_hours = effective_hours + work.hours
            remaining = task.planned_hours - effective_hours + task.reassignment_hour
            res[task.id] = remaining
        return res

    def _check_remaining_hours(self, cr, uid, ids, context=None):
        for task in self.browse(cr, uid, ids, context=context):
            if task.remaining_hours < 0:
                return False
            else:
                return True
        
    _columns = {
                'feature_hour_ids': fields.related('feature_id', 'hour_ids', type='one2many',
                    relation='ccorp.project.oerp.feature.hours', string='Feature Hours', readonly=True),
                'task_hour_ids': fields.one2many('ccorp.project.oerp.task.hour', 'task_id', string='Task Hours'),
                'kind_task_id':fields.many2one('ccorp.project.oerp.work.type','Type of task',required=True),
                'reassignment_hour': fields.float('Reassignment Hour', readonly=True),
                'remaining_hours': fields.function(_remaining_hours, type='float', string='Remaining Hour(s)', store=True),
                }

    def create(self, cr, uid, values, context=None):
        if 'project_id' in values:
            project_obj = self.pool.get('project.project')
            project = project_obj.browse(cr, uid, values['project_id'], context=context)
            if project.is_scrum:
                if 'task_hour_ids' in values: 
                    task_hour_ids = values['task_hour_ids']
                    sum = 0.0
                    for hour in task_hour_ids:
                        sum += hour[2]['expected_hours']
                    values['planned_hours'] = sum
        return super(Task, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        for task in self.browse(cr, uid, ids, context=context)[0]:
            if task.project_id.is_scrum:
                if 'task_hour_ids' in values:
                    sum = 0.0
                    for hour in values['task_hour_ids']:
                        if hour[0] == 0:
                            sum += hour[2]['expected_hours']
                        elif hour[0] == 1:
                            if 'expected_hours' in hour[2]:
                                sum += hour[2]['expected_hours']
                            else:
                                task_hour_obj = self.pool.get('ccorp.project.oerp.task.hour')
                                task_hour = task_hour_obj.browse(cr, uid , hour[1], context=context)
                                sum += task_hour.expected_hours
                        elif hour[0] == 4:
                            task_hour_obj = self.pool.get('ccorp.project.oerp.task.hour')
                            task_hour = task_hour_obj.browse(cr, uid , hour[1], context=context)
                            sum += task_hour.expected_hours
                    values['planned_hours'] = sum
            super(Task, self).write(cr, uid, task.id, values, context)
            if task._check_remaining_hours():
                return True
            else:
                raise osv.except_osv(
                _('Error'),
                _('Your time ivested in this task has exeded the planed time frame'))

    _defaults = {
        'state': 'draft',
        }
