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
                'warranty': fields.selection([('seller','Seller'),('manufacturer','Manufacturer')],string="Warranty"),                                 
                'backorder_ids': fields.one2many('stock.picking.out','issue_id'),
                'origin_id':fields.many2one('project.issue.origin',string="Origin"),
                'partner_type':fields.related('partner_id','partner_type',relation='res.partner',string="Partner Type"),
                'categ_id':fields.many2one('product.category',required=True,string="Category Product"),
                'product_id':fields.many2one('product.product',string="Product"),
                'prodlot_id':fields.many2one('stock.production.lot',string="Serial Number"),
                }
    
    def onchange_product_id(self, cr, uid, ids, product_id,context={}):
        data = {}
        if product_id:
            product = self.pool.get('product.product').browse(cr, uid, product_id, context)
            data.update({'categ_id': product.categ_id.id})

            prodlot_obj=self.pool.get('stock.production.lot')
            prodlot=prodlot_obj.search(cr, uid,[('product_id','=',product_id)])
            
            if not prodlot:
                data.update({'prodlot_id': False})
        return {'value': data}
    
    def onchange_categ_id(self, cr, uid,categ_id,ids,context={}):
            data={}
            
            product_obj=self.pool.get('product.product')
            product=product_obj.search(cr, uid,[('categ_id','=',categ_id)])

            if not product:
                data.update({'product_id': False})
                data.update({'prodlot_id': False})
                
            return {'value': data}

    
class ProjectIssueOrigin(osv.Model):
    _name = 'project.issue.origin'
    
    _columns = {
                'name': fields.char(required=True,string="Name"),
                'description': fields.text(string="Description")
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
     

class StockPicking(orm.Model):
    _inherit = 'stock.picking'

    _columns = {
         'issue_id': fields.many2one('project.issue')
    }

class StockPickingOut(orm.Model):
    _inherit = 'stock.picking.out'

    def __init__(self, pool, cr):
        super(StockPickingOut, self).__init__(pool, cr)
        self._columns['issue_id'] = self.pool['stock.picking']._columns['issue_id']
        
class ResPartner(orm.Model):
    _inherit = 'res.partner'

    _columns = {
        'partner_type': fields.selection([('company','Company'),('branch','Branch'),('customer','Customer')],required=True,string="Partner Type"),
        'provision_amount':fields.float(digits=(16,2),string="Provision Amount")
     }
    _defaults={
        'provision_amount':0.0
        }
    
    def onchange_partner_type(self, cr, uid, ids,partner_type,context={}):
        res={}
        
        if partner_type=='company':
            res['is_company'] = True
        elif partner_type=='branch':
            res['is_company'] = True
        elif partner_type=='customer':
            res['is_company'] = False
        return {'value': res}

class ContractPricelist(orm.Model):
    _name = 'contract.pricelist'

    _columns = {
        'name':fields.char(size=256,string="Name"),
        'account_analytic_id':fields.many2one('account.analytic.account',string="Account Analytic"),
        'partner_id':fields.related('account_analytic_id','partner_id',relation='res.partner',string="Partner"),
        'calendar_id':fields.many2one('resource.calendar',string="Calendar"),
        'line_ids': fields.one2many('contract.pricelist.line,','contract_pricelist_id')
        }
    _sql_constraints = [
        ('account_analytic_unique',
        'UNIQUE(account_analytic_id)',
        'Account Analytic already exist ')
                        ]
    
class ContractPriceLine(orm.Model):
    _name = 'contract.pricelist.line'

    _columns = {
        'contract_pricelist_id':fields.many2one('contract.pricelist',string="Contract Pricelist"),
        'pricelist_line_type': fields.selection([('category','Category'),('product','Product')],string="Pricelist Type"),                                 
        'categ_id':fields.many2one('product.category',string="Product Category"),
        'product_id':fields.many2one('product.product',string="Product"),
        'technical_rate':fields.float(digits=(16,2),required=True,string="Technical Rate"),
        'assistant_rate':fields.float(digits=(16,2),required=True,string="Assistant Rate"),
        'overtime_multiplier':fields.float(digits=(16,2),required=True,string="Overtime Multiplier"),
        'holiday_multiplier':fields.float(digits=(16,2),required=True,string="Holiday Multiplier")
       }
    
    _defaults={
        'technical_rate':0.0,
        'assistant_rate':0.0,
        'overtime_multiplier':1.0
        }
    def _check_rates(self, cr, uid, ids, context={}):
        for rates in self.browse(cr, uid, ids, context=context):
            if (rates.technical_rate<1.0 or rates.assistant_rate<1.0):
                return False
        return True
    
    def _check_multipliers(self, cr, uid, ids, context={}):
        for multipliers in self.browse(cr, uid, ids, context=context):
            if (multipliers.overtime_multiplier<1.0 or multipliers.holiday_multiplier<1.0):
                return False
        return True
    _constraints = [
        (_check_rates,'Rates must be greater or equal to one',['technical_rate','assistant_rate']
         ),
        (_check_multipliers,'Multipliers must be greater or equal to one',['overtime_multiplier','holiday_multiplier']
         ) 
                ]
    _sql_constraints = [
        ('contract_line_unique',
        'UNIQUE(categ_id,product_id,contract_pricelist_id)',
        'Contract only allow a line to a single category or product')     
    ]

class HolidayCalendar(orm.Model):
    _name = 'holiday.calendar'

    _columns = {
        'name':fields.char(size=256,string="Name"),
        'date':fields.date(required=True,string="Date"),
        'notes':fields.text(string="Notes")
        }
                        
                 



                        
