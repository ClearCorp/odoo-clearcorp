# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.tools.translate import _
from datetime import datetime
from openerp.exceptions import ValidationError

# Mapping between task priority and
# feature priority
PRIORITY = {
            5: '4',
            4: '3',
            3: '2',
            2: '1',
            1: '0',
            }

STATES = [('draft', 'Draft'), ('new', 'New'), ('open', 'In Progress'),
          ('pending', 'Pending'), ('done', 'Done'),
          ('cancelled', 'Cancelled')]


class FeatureType(models.Model):
    # Allows the creation of different types of features. It needs
    # unique identifiers for each type.
    _name = 'project.scrum.feature.type'
    
    _fields = {
        'code': fields.Char('Code', size=16, required=True),
        'name': fields.Char('Type Name', size=128, required=True,
                            translate=True)
    }
    
    _sql_constraints = [('unique_code', 'UNIQUE(code)',
                         'Code must be unique for every feature type.')]

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for r in self.read(cr, uid, ids, ['code', 'name'], context=context):
            name = '%s - %s' % (r['code'], r['name'])
            res.append((r['id'], name))
        return res


class Feature(models.Model):
    
    _inherit = 'mail.thread'
    _name = 'project.scrum.feature'
    
    def _date_start(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the start date based on the tasks from sprints
        related to each feature"""
        res = {}
        for id in ids:
            task_ids = [x.id for x in
                        self.browse(
                            cr, uid, id, context=context).task_ids]
            task_obj = self.pool.get('project.task')
            task_ids = task_obj.search(cr, uid,
                                       [('id', 'in', task_ids),
                                        ('feature_id', '=', id),
                                        '!', ('state', 'in',
                                              ['cancelled', 'draft'])],
                                       context=context)
            tasks = task_obj.browse(cr, uid, task_ids, context=context)
            date_start = False
            for task in tasks:
                if task.date_start:
                    date = datetime.strptime(task.date_start,
                                             '%Y-%m-%d %H:%M:%S')
                    if not date_start:
                        date_start = date
                    else:
                        if date_start > date:
                            date_start = date
            if date_start:
                date_start = datetime.strftime(date_start, '%Y-%m-%d %H:%M:%S')
            res[id] = date_start
        return res
    
    def _date_end(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the end date based on the tasks from sprints 
        related to each feature"""
        res = {}
        for id in ids:
            task_ids = [x.id for x in
                        self.browse(cr, uid, id,
                                    context=context).task_ids]
            task_obj = self.pool.get('project.task')
            task_ids = task_obj.search(cr, uid,
                                       [('id', 'in', task_ids),
                                        ('feature_id', '=', id),
                                        '!', ('state', 'in',
                                              ['cancelled', 'draft'])],
                                       context=context)
            tasks = task_obj.browse(cr, uid, task_ids, context=context)
            date_end = False
            for task in tasks:
                if task.date_end:
                    date = datetime.strptime(task.date_end,
                                             '%Y-%m-%d %H:%M:%S')
                    if not date_end:
                        date_end = date
                    else:
                        if date > date_end:
                            date_end = date
            if date_end:
                date_end = datetime.strftime(date_end, '%Y-%m-%d %H:%M:%S')
            res[id] = date_end
        return res
    
    def _effective_hours(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the planned hours based on the tasks  
        related to each feature"""

        res = {}
        for id in ids:
            task_ids = [x.id for x in
                        self.browse(
                            cr, uid, id, context=context).task_ids]
            task_obj = self.pool.get('project.task')
            task_ids = task_obj.search(cr, uid,
                                       [('id', 'in', task_ids),
                                        ('feature_id', '=', id)],
                                       context=context)
            tasks = task_obj.browse(cr, uid, task_ids, context=context)
            sum = reduce(lambda result, task: result+task.effective_hours,
                         tasks, 0.0)
            res[id] = sum
            return res
    
    def _remaining_hours(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the difference between planned and effective hours"""
        res = {}
        features = self.browse(cr, uid, ids, context=context)
        for feature in features:
            res[feature.id] = feature.expected_hours - \
                feature.effective_hours
        return res
    
    def _progress(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the total progress based on the tasks from sprints 
        related to each feature"""
        res = {}
        for id in ids:
            task_ids = [x.id for x in
                        self.browse(cr, uid, id,
                                    context=context).task_ids]
            task_obj = self.pool.get('project.task')
            task_ids = task_obj.search(cr, uid,
                                       [('id', 'in', task_ids),
                                        ('feature_id', '=', id)],
                                       context=context)
            tasks = task_obj.browse(cr, uid, task_ids, context=context)
            if tasks:
                sum = reduce(lambda result, task: result+task.progress,
                             tasks, 0.0)
                res[id] = sum/len(tasks)
            else:
                res[id] = 0.0
        return res
    
    def set_open(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)
    
    def set_done(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)
    
    def set_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids,
                          {'state': 'cancelled'}, context=context)
    
    def set_very_low_priority(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'priority': 5}, context=context)
    
    def set_low_priority(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'priority': 4}, context=context)
    
    def set_medium_priority(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'priority': 3}, context=context)
    
    def set_high_priority(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'priority': 2}, context=context)
    
    def set_very_high_priority(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'priority': 1}, context=context)

    _fields = {
        'name': fields.Char('Feature Name', size=128, required=True),
        'code': fields.Char('Code', size=16, required=True),
        'release_backlog_id': fields.Many2one(
            'project.scrum.release.backlog',
            string='Release Backlog',
            domain="[('project_id', '=', project_id),"
            "'|',('state','=','open'),('state','=','pending')]"),
        'project_id': fields.Many2one(
            'project.project', string='Project', required=True),
        'description': fields.Text('Description'),
        'partner_id': fields.Many2one(
            'res.partner', string='Product Owner',
            domain="[('customer','=',True)]",
            help='Contact or person responsible of keeping the '
                 'business perspective in scrum projects.'),
        'type_id': fields.Many2one(
            'project.scrum.feature.type',
            string='Type'),
        'priority': fields.Selection(
            [(5, '5 - Very Low'), (4, '4 - Low'), (3, '3 - Medium'),
             (2, '2 - High'), (1, '1 - Very High')],
            default=3, string='Priority', required=True),
        'task_ids': fields.One2many(
            'project.task', 'feature_id',
            string='Tasks', readonly=True),
        'date_start': fields.Datetime(
            'Start Date', compute=_date_start, store=True),
        'date_end': fields.Datetime(
            'End Date', compute=_date_end, store=True),
        'deadline': fields.Date(string='Deadline'),
        'expected_hours': fields.Float(
            'Initially Planned Hour(s)',
            help='Total planned hours for the development of '
            'this feature.\nRecommended values '
            'are:\n 1 h, 2 h, 4 h, or 8 h.'),
        'effective_hours': fields.Float(
            'Hour(s) Spent',
            help='Total effective hours spent on tasks '
                 'related to this feature.',
            compute=_effective_hours,
            store=True),
        'remaining_hours': fields.Float(
            'Remaining Hour(s)',
            help='Difference between planned hours and spent hours.',
            compute=_remaining_hours,
            store=True),
        'progress': fields.Float(
            'Progress (%)',
            compute=_progress,
            store=True),
        'state': fields.Selection(
            [('draft', 'New'), ('open', 'In Progress'),
             ('cancelled', 'Cancelled'),
             ('done', 'Done'), ],
            default='draft', string='Status', required=True),
        'color': fields.Integer('Color Index'),
        'acceptance_requirements_client': fields.Text(
            'Acceptance requirements by client'),
        'acceptance_requirements_supplier': fields.Text(
            'Funtional acceptance requirements'),
        'validation_date': fields.Date('Validation Date'),
    }
    
    def name_get(self, cr, uid, ids, context=None):
        res = []
        for r in self.read(cr, uid, ids, ['code', 'name'], context=context):
            name = '%s - %s' % (r['code'], r['name'])
            res.append((r['id'], name))
        return res
    
    def name_search(
            self, cr, uid, name='', args=None,
            operator='ilike', context=None, limit=50):
        ids = []
        if name:
            ids = self.search(cr, uid,
                              ['|', ('code', operator, name),
                               ('name', operator, name)] + args,
                              limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        
        return self.name_get(cr, uid, ids, context=context)
    
    def copy(self, cr, uid, id, defaults, context=None):
        feature = self.browse(cr, uid, id, context=context)
        defaults['code'] = feature.code + ' (copy)'
        return super(Feature, self).copy(
            cr, uid, id, defaults, context=context)
    
    _sql_constraints = [
        ('unique_code_product', 'UNIQUE(code,project_id)',
         'Code must be unique for every feature related to a Product Backlog')]


class Sprint(models.Model):
    
    _name = 'project.scrum.sprint'
    
    def _date_end(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate end date as the latest date from
        tasks related to this sprint"""
        res = {}
        for id in ids:
            tasks = self.browse(cr, uid, id, context=context).task_ids
            date_end = False
            for task in tasks:
                if task.date_end and task.state not in ('draft', 'cancelled'):
                    date = datetime.strptime(
                        task.date_end, '%Y-%m-%d %H:%M:%S')
                    if not date_end:
                        date_end = date
                    else:
                        if date > date_end:
                            date_end = date
            if date_end:
                date_end = date_end.strftime('%Y-%m-%d %H:%M:%S')
            res[id] = date_end
        return res
    
    def _expected_hours(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the expected hours from features related to this
        sprint."""
        res = {}
        for id in ids:
            tasks = self.browse(cr, uid, id, context=context).task_ids
            sum = reduce(lambda result, task: result + task.planned_hours,
                         tasks, 0.0)
            res[id] = sum
        return res
    
    def _effective_hours(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the effective hours using the work done in tasks
        related to this sprint."""
        res = {}
        for id in ids:
            tasks = self.browse(cr, uid, id, context=context).task_ids
            sum = reduce(lambda result, task: result + task.effective_hours,
                         tasks, 0.0)
            res[id] = sum
        return res
    
    def _remaining_hours(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the difference between planned and effective hours."""
        res = {}
        sprints = self.browse(cr, uid, ids, context=context)
        for sprint in sprints:
            res[sprint.id] = sprint.expected_hours - sprint.effective_hours
        return res
    
    def _progress(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the progress using the progress in tasks related
        to this sprint."""
        res = {}
        for id in ids:
            tasks = self.browse(cr, uid, id, context=context).task_ids
            if tasks:
                sum = reduce(lambda result, task: result + task.progress,
                             tasks, 0.0)
                res[id] = sum / len(tasks)
            else:
                # set value to zero if no tasks are available
                res[id] = 0.0
        return res
    
    def onchange_project(
            self, cr, uid, ids, project_id, stage_id, context=None):
        if project_id:
            type_ids = [x.id for x in self.pool.get('project.project').browse(
                cr, uid, project_id, context=context).type_ids]
            if stage_id not in type_ids:
                stage = self.get_default_stage_id(
                    cr, uid, project_id, context=context)
                return {'value': {'stage_id': stage}}
            else: 
                return {}
        return {
                'value': {
                    'stage_id': self.get_default_stage(
                        cr, uid, context=context)
                          }
                }
    
    def get_default_stage(self, cr, uid, context=None):
        type_obj = self.pool.get('project.task.type')
        type = type_obj.search(cr, uid, [('state', '=', 'draft')],
                               context=context, limit=1)[0]
        if not type:
            raise Warning(_('There is no ''draft'' state configured.'))
        return type
        
    def get_default_stage_id(self, cr, uid, project_id, context=None):
        type_obj = self.pool.get('project.task.type')
        type = type_obj.search(
            cr, uid, [('project_ids', '=', project_id)],
            context=context, limit=1)[0]
        return type
    
    def tasks_from_features(self, cr, uid, ids, context=None):
        sprint = self.browse(cr, uid, ids[0], context=context)
        task_obj = self.pool.get('project.task')
        for feature in sprint.feature_ids:
            values = {
                'project_id': sprint.project_id.id,
                'release_backlog_id': sprint.release_backlog_id.id,
                'sprint_id': sprint.id,
                'feature_id': feature.id,
                'user_id': uid,
                'planned_hours': feature.expected_hours,
                'remaining_hours': feature.expected_hours,
                'date_start': sprint.date_start,
                'date_end': sprint.deadline,
                'date_deadline': sprint.deadline,
                'priority': PRIORITY[feature.priority],
                'description': feature.description,
                'name': feature.code + ' ' + feature.name,
            }
            task_obj.create(cr, uid, values, context=context)
        return True
    
    def set_features_done(self, cr, uid, ids, context=None):
        sprint = self.browse(cr, uid, ids[0], context=context)
        for feature in sprint.feature_ids:
            if feature.state not in ('done', 'cancelled'):
                feature.write({'state': 'done'}, context=context)
        return True
    
    def set_done(self, cr, uid, ids, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        sprint = self.browse(cr, uid, ids[0], context=context)
        for task in sprint.task_ids:
            if task.state not in ['done', 'cancelled']:
                raise Warning(_('All tasks must be done or cancelled '
                                'in order to cancel this sprint.'))
        project = sprint.project_id
        id = False
        for stage in project.type_ids:
            if stage.state == 'done':
                id = stage.id
                break
        self.write(cr, uid, ids[0], {'stage_id': id}, context)
        return True
    
    def set_cancel(self, cr, uid, ids, context=None):
        sprint = self.browse(cr, uid, ids[0], context=context)
        for task in sprint.task_ids:
            if task.state not in ['done', 'cancelled']:
                raise Warning(_('All tasks must be done or cancelled in order '
                                'to cancel this sprint.'))
        project = sprint.project_id
        id = False
        for stage in project.type_ids:
            if stage.state == 'cancelled':
                id = stage.id
                break
        self.write(cr, uid, ids[0], {'stage_id': id}, context)
        return True

    @api.constrains('date_start', 'deadline')
    def _check_deadline(self, cr, uid, ids, context=None):
        sprints = self.browse(cr, uid, ids, context=context)
        for sprint in sprints:
            date_start = datetime.strptime(
                sprint.date_start, '%Y-%m-%d %H:%M:%S')
            deadline = datetime.strptime(sprint.deadline, '%Y-%m-%d')
            if deadline < date_start:
                raise ValidationError(
                    'Deadline must be greater than Start Date')
    
    _fields = {
        'name': fields.Char('Name', size=128, required=True),
        'partner_id': fields.Many2one(
            'res.users', string='User', size=128, required=True),
        'task_ids': fields.One2many(
            'project.task', 'sprint_id', string='Tasks'),
        'date_start': fields.Datetime(
            'Start Date',
            required=True),
        'date_end': fields.Datetime(
            'End Date', compute=_date_end, store=True),
        'deadline': fields.Date(
            'Deadline',
            default=lambda *a: fields.Date.today(),
            required=True),
        'expected_hours': fields.Float(
            'Initially Planned Hour(s)',
            compute=_expected_hours, store=True),
        'effective_hours': fields.Float(
            'Hour(s) Spent', compute=_effective_hours, store=True),
        'remaining_hours': fields.Float(
            'Remaining Hour(s)', compute=_remaining_hours, store=True),
        'progress': fields.Float(
            'Progress (%)', compute=_progress, store=True),
        'stage_id': fields.Many2one(
            'project.task.type', string='Stage',
            domain="[('fold', '=', False)]"),
        'state': fields.Selection(
            STATES, 'State', default='new', related='stage_id',
            readonly=True),
        'color': fields.Integer('Color Index'),
    }


class Task(models.Model):

    _inherit = 'project.task'

    def onchange_project(self, cr, uid, ids, project_id, context=None):
        res = super(Task, self).onchange_project(
            cr, uid, ids, project_id, context=context)
        if project_id:
            project = self.pool.get('project.project').browse(
                cr, uid, project_id, context=context)
            if 'value' not in res:
                res['value'] = {}
            res['value']['is_scrum'] = project.is_scrum
            if not project.is_scrum:
                res['value']['release_backlog_id'] = False
                res['value']['sprint_id'] = False
                res['value']['feature_id'] = False
        else:
            if 'value' not in res:
                res['value'] = {}
            res['value']['is_scrum'] = False
            res['value']['release_backlog_id'] = False
            res['value']['sprint_id'] = False
            res['value']['feature_id'] = False
        return res
    
    def onchange_sprint(self, cr, uid, ids, sprint_id, context=None):
        res = None
        if sprint_id:
            res = {
                   'value': {},
                   'domain': {},
                   }
            sprint_obj = self.pool.get('project.scrum.sprint')
            sprint = sprint_obj.browse(cr, uid, sprint_id, context=context)
            res['value']['date_deadline'] = sprint.deadline
        else:
            res = {'value': {}}
            res['value']['date_deadline'] = False
        return res

    def onchange_feature(self, cr, uid, ids, feature_id, context=None):
        if feature_id:
            feature = self.pool.get('project.scrum.feature').browse(
                cr, uid, feature_id, context=context)
            return {
                'value': {
                    'planned_hours': feature.expected_hours,
                    'priority': PRIORITY[feature.priority],
                }
            }
        else:
            return {
                'value': {
                    'planned_hours': False,
                    'priority': '2',
                }
            }

    @api.constrains('previous_task_ids', 'next_task_ids')
    def _check_related_tasks(self, cr, uid, ids, context=None):
        tasks = self.browse(cr, uid, ids, context=context)
        validation_error = "There was an error checking the relationship" \
                           "between tasks. Please check if you selected " \
                           "an invalid task."
        for task in tasks:
            for previous_task in task.previous_task_ids:
                if previous_task.id == task.id or \
                                previous_task in task.next_task_ids:
                    raise ValidationError(validation_error)
            for next_task in task.next_task_ids:
                if next_task.id == task.id:
                    raise ValidationError(validation_error)

    def write(self, cr, uid, ids, values, context=None):
        if 'stage_id' in values:
            stage_obj = self.pool.get('project.task.type')
            stage = stage_obj.browse(
                cr, uid, values['stage_id'], context=context)
            if stage.state == 'done':
                date_end = datetime.strftime(
                    datetime.now(), '%Y-%m-%d %H:%M:%S')
                values.update({
                          'date_end': date_end,
                              })
        return super(Task, self).write(cr, uid, ids, values, context)

    _fields = {
        'date_start': fields.Datetime(
            'Starting Date', select=True, copy=False,
            default=lambda *a: datetime.strftime(
                datetime.now(), '%Y-%m-%d %H:%M:%S')),
        'is_scrum': fields.Boolean('Scrum'),
        'project_id': fields.Many2one(
            'project.project', 'Project', ondelete='set null',
            select=True, track_visibility='onchange', change_default=True,
            default=lambda slf, cr, uid, ctx: ctx.get('project_id', False)),
        'sprint_id': fields.Many2one(
            'project.scrum.sprint', string='Sprint',
            default=lambda slf, cr, uid, ctx: ctx.get('sprint_id', False)),
        'feature_id': fields.Many2one(
            'project.scrum.feature', string='Feature'),
        'feature_type_id': fields.Many2one(
            'type_id', string='Feature Type',
            related='project.scrum.feature.type', readonly=True),
        'previous_task_ids': fields.Many2many(
            'project.task', 'project_scrum_task_previous_tasks',
            'task_id', 'previous_task_id', string='Previous Tasks',
            domain="['!',('id','=',id)]"),
        'next_task_ids': fields.Many2many(
            'project.task', 'project_scrum_task_next_tasks',
            'task_id', 'next_task_id', string='Next Tasks',
            domain="['!',('state','in',['done','cancelled']),"
            "'!',('id','=',id)]"),
    }

    _defaults = {

                 'release_backlog_id':
                 lambda slf, cr, uid, ctx: ctx.get(
                     'release_backlog_id', False)

                 }


class ReleaseBacklog(models.Model):
    
    _name = 'project.scrum.release.backlog'
    
    def _date_end(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the end date from sprints related to 
        each backlog"""
        res = {}
        for id in ids:
            features = self.browse(cr, uid, id, context=context).feature_ids
            date_end = False
            for feature in features:
                if feature.date_end and \
                                feature.state not in ['draft', 'cancelled']:
                    date = datetime.strptime(
                        feature.date_end, '%Y-%m-%d %H:%M:%S')
                    if not date_end:
                        date_end = date
                    else:
                        if date_end < date:
                            date_end = date
            if date_end:
                date_end = date_end.strftime('%Y-%m-%d %H:%M:%S')
            res[id] = date_end
        return res
    
    def _date_start(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the start date from sprints related to 
        each backlog"""
        res = {}
        for id in ids:
            features = self.browse(cr, uid, id, context=context).feature_ids
            date_start = False
            for feature in features:
                if feature.date_start and \
                                feature.state not in ['draft', 'cancelled']:
                    date = datetime.strptime(
                        feature.date_start, '%Y-%m-%d %H:%M:%S')
                    if not date_start:
                        date_start = date
                    else:
                        if date_start > date:
                            date_start = date
            if date_start:
                date_start = date_start.strftime('%Y-%m-%d %H:%M:%S')
            res[id] = date_start
        return res
    
    def _expected_hours(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the expected hours from sprints related to 
        each backlog"""
        res = {}
        for id in ids:
            features = self.browse(cr, uid, id, context=context).feature_ids
            sum = reduce(
                lambda result, feature: result + feature.expected_hours,
                features, 0.0)
            res[id] = sum
        return res
    
    def _effective_hours(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the effective hours from sprints related to 
        each backlog"""
        res = {}
        for id in ids:
            features = self.browse(cr, uid, id, context=context).feature_ids
            sum = reduce(
                lambda result, feature: result + feature.effective_hours,
                features, 0.0)
            res[id] = sum
        return res
    
    def _remaining_hours(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the difference between expected and effective hours
        from sprints related to each backlog"""
        res = {}
        releases = self.browse(cr, uid, ids, context=context)
        for release in releases:
            res[release.id] = release.expected_hours - release.effective_hours
        return res
    
    def _progress(self, cr, uid, ids, field_name, arg, context=None):
        """Calculate the total progress from sprints related to 
        each backlog"""
        res = {}
        for id in ids:
            features = self.browse(cr, uid, id, context=context).feature_ids
            if features:
                sum = reduce(lambda result, feature: result + feature.progress,
                             features, 0.0)
                res[id] = sum / len(features)
            else:
                res[id] = 0.0
        return res
    
    def _set_done(self, cr, uid, ids, context=None):
        project = self.browse(cr, uid, ids[0], context=context).project_id
        for stage in project.type_ids:
            if stage.state == 'done':
                return self.write(
                    cr, uid, ids[0], {'stage_id': stage.id}, context=context)
        raise Warning(_('There is no done state configured for'
                        ' the project %s') % project.name)
    
    def do_done(self, cr, uid, ids, context=None):
        sprints = self.browse(cr, uid, ids[0], context=context).sprint_ids
        for sprint in sprints:
            if sprint.state != 'cancelled' and sprint.state != 'done':
                raise Warning(_('You can not set as done a release backlog '
                                'if all sprints related to it are not '
                                'cancelled or done'))
        return self._set_done(cr, uid, ids, context=context)
    
    def _set_cancel(self, cr, uid, ids, context=None):
        project = self.browse(cr, uid, ids[0], context=context).project_id
        for stage in project.type_ids:
            if stage.state == 'cancelled':
                return self.write(
                    cr, uid, ids[0], {'stage_id': stage.id}, context=context)
        raise Warning(_('There is no cancelled state configured for'
                        ' the project %s') % project.name)
    
    def do_cancel(self, cr, uid, ids, context=None):
        sprints = self.browse(cr, uid, ids[0], context=context).sprint_ids
        for sprint in sprints:
            if sprint.state != 'cancelled' and sprint.state != 'done':
                raise Warning(_('You can not cancel a release backlog if '
                                'all sprints related to it are not cancelled'
                                ' or done'))
        return self._set_cancel(cr, uid, ids, context=context)

    _fields = {
        'name': fields.Char('Release Name', size=128, required=True),
        'project_id': fields.Many2one(
            'project.project', string='Project', required=True),
        'feature_ids': fields.One2many(
            'project.scrum.feature', 'release_backlog_id',
            string='Features'),
        'date_start': fields.Datetime(
            'Start Date', compute=_date_start,
            help='Calculated Start Date, will be empty if any '
                 'sprint has no start date.', store=True),
        'date_end': fields.Datetime(
            'End Date', compute=_date_end,
            help='Calculated End Date, will be empty if any '
                 'sprint has no end date.', store=True),
        'deadline': fields.Datetime(
            string='Deadline',
            help='Calculated Deadline, will be empty if any '
                 'sprint has no deadline.'),
        'expected_hours': fields.Float(
            'Initially Planned Hour(s)', compute=_expected_hours,
            help='Total planned hours calculated '
            'from sprints.', store=True),
        'effective_hours': fields.Float(
            'Spent Hour(s)', compute=_effective_hours,
            help='Total spent hours calculated '
            'from sprints.', store=True),
        'remaining_hours': fields.Float(
            'Remaining Hour(s)', compute=_remaining_hours,
            help='Difference between planned hours and spent hours.',
            store=True),
        'progress': fields.Float(
            'Progress (%)', compute=_progress,
            help='Total progress percentage calculated from sprints',
            store=True),
        'stage_id': fields.Many2one(
            'project.task.type', string='Stage',
            domain="['&', ('fold', '=', False),"
            " ('project_ids', '=', project_id)]"),
        'state': fields.Selection(
            STATES, 'State', related='state',
            readonly=True),
        'color': fields.Integer('Color Index'),
    }
    
    _defaults = {
                 'project_id':
                 lambda self, cr, uid, c: c.get('project_id', False),
                 }


class Project(models.Model):
    
    _inherit = 'project.project'
    
    def _date_end(self, cr, uid, ids, field_name, arg, context=None):
        """Calculates the product backlog date_end getting the 
        estimated end_date from features related to 
        each product backlog."""
        res = {}
        for id in ids: 
            backlog_obj = self.pool.get('project.scrum.release.backlog')
            backlog_ids = backlog_obj.search(
                cr, uid, [('project_id', '=', id)])
            features = backlog_obj.browse(
                cr, uid, backlog_ids, context=context).feature_ids
            date_end = False
            for feature in features:
                if feature.date_end and \
                                feature.state not in ['draft', 'cancelled']:
                    date = datetime.strptime(
                        feature.date_end, '%Y-%m-%d %H:%M:%S')
                    if not date_end:
                        date_end = date
                    else:
                        if date_end < date:
                            date_end = date 
            if date_end:
                res[id] = datetime.strftime(date_end, '%Y-%m-%d %H:%M:%S')
            else:
                res[id] = date_end
        return res
    
    def _deadline(self, cr, uid, ids, field_name, arg, context=None):
        """Calculates the product backlog deadline getting the 
        estimated end_date from features related to 
        each product backlog."""
        res = {}
        for id in ids:
            backlog_obj = self.pool.get('project.scrum.release.backlog')
            backlog_ids = backlog_obj.search(
                cr, uid, [('project_id', '=', id)])
            features = backlog_obj.browse(
                cr, uid, backlog_ids, context=context).feature_ids
            deadline = False
            for feature in features:
                if feature.date_end and \
                                feature.state not in ['draft', 'cancelled']:
                    if feature.deadline:
                        date = datetime.strptime(feature.deadline, '%Y-%m-%d')
                        if not deadline:
                            deadline = date
                        else:
                            if deadline < date:
                                deadline = date
            if deadline:
                res[id] = datetime.strftime(deadline, '%Y-%m-%d')
            else:
                res[id] = deadline
        return res

    _fields = {
        'is_scrum': fields.Boolean('Scrum'),
        'date_end': fields.Datetime(
            'End Date', compute=_date_end,
            help='Calculated End Date, will be '
            'empty if any feature has no end date.'),
        'deadline': fields.Date(
            'Deadline', compute=_deadline,
            help='Calculated Deadline, will be empty if any feature '
                 'has no deadline.'),
        'release_backlog_ids': fields.One2many(
            'project.scrum.release.backlog',
            'id', string='Release Backlogs'),
    }
