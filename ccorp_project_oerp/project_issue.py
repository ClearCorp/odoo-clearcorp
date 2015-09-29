from openerp import models, fields, api, _
from openerp.exceptions import Warning


class issue(models.Model):
    
    _inherit = 'project.issue'
    
    task_ids = fields.Many2many('project.task')
    work_type_id = fields.Many2one('ccorp.project.oerp.work.type','Type of work',required=True)
    issue_type = fields.Selection([('change_request','Change Request'),('service_request','Service Request'),
                                   ('issue','Issue'),('problem','Problem')], 
                                  string='Issue Type', default='issue',required=True)
    feature_id = fields.Many2one('ccorp.project.scrum.feature', string='Feature')
    saleorderline_id = fields.Many2one('sale.order.line', string='Sale order line')
    
class saleorderline(models.Model):

    _inherit = 'sale.order.line'

    issue_id = fields.Many2one('project.issue', string='Issue')