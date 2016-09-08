# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv, fields


class Project(osv.Model):
    _inherit = 'project.project'
    
    _columns = {
        'task_sequence_id': fields.many2one(
            'ir.sequence',
            'Task Sequence',
            domain=[('code', '=', 'project.project')]),
    }
    
    def create(self, cr, uid, vals, context=None):

        project_id = super(Project, self).create(cr, uid, vals, context)
        if 'task_sequence_id' not in vals.keys() \
                or not vals['task_sequence_id']:
            ir_sequence_obj = self.pool.get('ir.sequence')
            sequence_name = "Project " + str(project_id) + " " + vals['name']
            task_sequence_id = ir_sequence_obj.create(
                cr, uid, {'name': sequence_name,
                          'code': 'project.project'}, context)
            self.write(cr, uid, project_id, {
                'task_sequence_id': task_sequence_id}, context=context)
        return project_id
    
    def write(self, cr, uid, id, vals, context=None):
        project_id = super(Project, self).write(
            cr, uid, id, vals, context=context)
        if 'task_sequence_id' in vals.keys() and not vals['task_sequence_id']:
            ir_sequence_obj = self.pool.get('ir.sequence')
            sequence_name = "Project " + str(project_id) + " " + vals['name']
            task_sequence_id = ir_sequence_obj.create(
                cr, uid, {'name': sequence_name,
                          'code': 'project.project'}, context)
            self.write(cr, uid, project_id,
                       {'task_sequence_id': task_sequence_id}, context=context)
        return project_id
    
    def unlink(self, cr, uid, ids, context=None):
        task_sequence_ids = []
        ir_sequence_obj = self.pool.get('ir.sequence')       
        for proj in self.browse(cr, uid, ids, context=context):
            if proj.task_sequence_id \
                    and not self.search(
                        cr, uid, [('task_sequence_id', '=',
                                   proj.task_sequence_id.id),
                                  ('id', '<>', proj.id)], context=context):
                task_sequence_ids.append(proj.task_sequence_id.id)
        res = super(Project, self).unlink(cr, uid, ids, context=context)
        ir_sequence_obj.unlink(cr, uid, task_sequence_ids, context=context)
        return res


class Task(osv.Model):
    _inherit = 'project.task'
    
    _columns = {
        'number': fields.char('Number', size=32),
    }

    def get_number_sequence(self, cr, uid, project_id, context=None):
        ir_sequence_obj = self.pool.get('ir.sequence')
        project_obj = self.pool.get('project.project')
        project = project_obj.browse(cr, uid, project_id, context)
        return ir_sequence_obj.next_by_id(cr, uid,
                                          project.task_sequence_id.id, context)
    
    def create(self, cr, uid, vals, context={}):
        if 'number' not in vals or vals['number'] is None \
                or vals['number'] == '':
            vals.update({'number': self.get_number_sequence(
                cr, uid, vals['project_id'], context)})
        return super(Task, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'project_id' in vals:
            vals.update({'number': self.get_number_sequence(
                cr, uid, vals['project_id'], context)})
        return super(Task, self).write(cr, uid, ids, vals, context)
