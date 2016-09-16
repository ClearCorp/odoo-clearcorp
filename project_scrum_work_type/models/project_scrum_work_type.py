# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api
from openerp.exceptions import ValidationError
from openerp.tools.translate import _


class FeatureHours(models.Model):
    
    _name = 'project.scrum.feature.hours'

    def _effective_hours(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for hour in self.browse(cr, uid, ids, context=context):
            task_obj = self.pool.get('project.task')
            task_ids = task_obj.search(
                cr, uid, [('feature_id', '=', hour.feature_id.id)],
                context=context)
            tasks = task_obj.browse(cr, uid, task_ids, context=context)
            sum = 0.0
            for task in tasks:
                if task.work_type_id == hour.work_type_id:
                    sum += task.effective_hours
            res[hour.id] = sum
        return res
    
    def _remaining_hours(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = task.expected_hours - task.effective_hours
        return res

    _fields = {
        'feature_id': fields.Many2one(
            'project.scrum.feature', string='Feature', required=True,
            ondelete='cascade',
            default=lambda slf, cr, uid, ctx: ctx.get('feature_id', False)),
        'work_type_id': fields.Many2one(
            'project.work.type', string='Work Type'),
        'expected_hours': fields.Float(
            'Planned Hour(s)', required=True),
        'effective_hours': fields.Float(
            'Spent Hour(s)', compute=_effective_hours, store=True),
        'remaining_hours': fields.Float(
            'Remaining Hour(s)', compute=_remaining_hours, store=True),
    }


class Feature(models.Model):
    
    _inherit = 'project.scrum.feature'
    
    _fields = {
        'hour_ids': fields.One2many(
            'project.scrum.feature.hours', 'feature_id',
            string='Feature Hours'),
    }
    
    def create_tasks(self, cr, uid, context):
        active_ids = context.get('active_ids', [])
        feature_obj = self.pool.get('project.scrum.feature')
        for feature in feature_obj.browse(
                cr, uid, active_ids, context=context):
            for feature_hour in feature.hour_ids:
                try:
                    values = {
                        'name': feature.code + ' ' + feature.name,
                        'project_id': feature.project_id.id,
                        'work_type_id': feature_hour.work_type_id.id,
                        'sprint_id': False,
                        'feature_id': feature.id,
                        'description': feature.description,
                        'planned_hours': feature_hour.expected_hours,
                        'date_deadline': feature.deadline,
                        'date_start': feature.date_start,
                        'is_scrum': True,
                    }
                    task_obj = self.pool.get('project.task')
                    task_id = task_obj.create(cr, uid, values, context=context)
                except:
                    raise Warning(_('An error occurred while creating the '
                                    'tasks. Please contact your system '
                                    'administrator.'))

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
                    hour_obj = self.pool.get('project.scrum.feature.hours')
                    sum += hour_obj.browse(
                        cr, uid, id, context=context).expected_hours
            values['expected_hours'] = sum
        return super(Feature, self).write(
            cr, uid, ids, values, context=context)

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
                    hour_obj = self.pool.get('project.scrum.feature.hours')
                    sum += hour_obj.browse(
                        cr, uid, id, context=context).expected_hours
            values['expected_hours'] = sum
        return super(Feature, self).create(cr, uid, values, context=context)


class Task(models.Model):
    
    _inherit = 'project.task'

    def onchange_sprint(self, cr, uid, ids, sprint_id, context=None):
        res = {}
        return res

    def _remaining_hours(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        effective_hours = 0
        for task in self.browse(cr, uid, ids, context=context):
            for work in task.work_ids:
                effective_hours = effective_hours + work.hours
            remaining = \
                task.planned_hours - effective_hours + task.reassignment_hour
            res[task.id] = remaining
        return res

    @api.constrains('planned_hours')
    def _validate_planned_hours(self, cr, uid, ids, context=None):
        for task in self.browse(cr, uid, ids, context):
            if task.planned_hours == 0.0:
                raise ValidationError('Planned hours can\'t be zero')

    def create(self, cr, uid, values, context=None):
        if 'project_id' in values:
            project_obj = self.pool.get('project.project')
            project = project_obj.browse(
                cr, uid, values['project_id'], context=context)
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
                                task_hour_obj = self.pool.get(
                                    'project.task.hour')
                                task_hour = task_hour_obj.browse(
                                    cr, uid, hour[1], context=context)
                                sum += task_hour.expected_hours
                        elif hour[0] == 4:
                            task_hour_obj = self.pool.get('project.task.hour')
                            task_hour = task_hour_obj.browse(
                                cr, uid, hour[1], context=context)
                            sum += task_hour.expected_hours
                    values['planned_hours'] = sum
            super(Task, self).write(cr, uid, task.id, values, context)
        return True

    _fields = {
        'feature_hour_ids': fields.One2many(
            'feature_id', string='Feature Hours',
            related='project.scrum.feature.hours', readonly=True),
        'remaining_hours': fields.Float(
            'Remaining Hour(s)', compute=_remaining_hours, store=True),
        'state': fields.Selection(
            [('draft', 'New'), ('open', 'In Progress'),
             ('cancelled', 'Cancelled'),
             ('done', 'Done'), ],
            default='draft', string='Status', required=True)
    }
