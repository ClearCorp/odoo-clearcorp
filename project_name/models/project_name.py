# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv, fields

class project_name_shortcut(osv.osv):
    _inherit = 'project.project'
    
    def name_get(self, cr, uid, ids=[], context=None):
        res = []
        if isinstance(ids, int):
            ids = [ids]
        done_ids=[]
        for project in self.browse(cr, uid, ids, context=context):
            if project.id not in done_ids:
                data = []
                proj = project.parent_id
                while proj and proj.parent_id:
                    if proj.code != '' and proj.code != False:
                        data.insert(0, (proj.code))
                        proj = proj.parent_id
                        continue
                    else:
                        data.insert(0, (proj.name))
                        proj = proj.parent_id
                data.append(project.name)
                data = ' / '.join(data)
                res.append((project.id, data))
                done_ids.append(project.id)
        return res

    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=50):
        ids = []
        
        if name:
            ids = self.search(cr, uid,
                              ['|', ('complete_name', operator, name),
                               '|', ('name', operator, name),
                               ('code', operator, name)] + args,
                              limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        analytic_account_ids= [project.analytic_account_id.id for project in self.browse(cr,uid,ids,context=context)] 
        analytic_account_ids= self.pool.get('account.analytic.account').get_children(cr,uid,analytic_account_ids,context=context)
        ids+=self.search(cr,uid,[('analytic_account_id','in',analytic_account_ids)],context=context)
        
        return self.name_get(cr, uid, ids, context=context)
    
class account_name_shortcut(osv.osv):
    _inherit = 'account.analytic.account'
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=50):
        ids = []
        
        if name:
            ids = self.search(cr, uid,
                              ['|', ('complete_name', operator, name),
                               '|', ('name', operator, name),
                               ('code', operator, name)] + args,
                              limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        ids+= self.get_children(cr,uid,ids,context=context)
        
        return self.name_get(cr, uid, ids, context=context)