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
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
import time

class StockMoveWizard(models.TransientModel):
    _name = 'stock.move.report.wiz'
    
    @api.multi
    def print_report(self):
        #Get all customers if no one is selected
        if not self.product_ids:
            self.product_ids = self.env['product.product']
        data = {
            'form': {
                     'date_from': self.date_from,
                     'date_to': self.date_to,
                     'include_costs': self.include_costs,
                     'category_ids': self.filter,
                     
                     'fiscalyear_id': self.fiscalyear_id.id,
                     'period_to': self.period_to.id,
                     'period_from':self.period_from.id,
            }
        }
        if self.out_format=='qweb-PDF':
            res = self.env['report'].get_action(self.product_ids,
            'stock_move_report.report_stock_move_pdf', data=data)
            return res        
        #elif self.out_format=='qweb-XLS':
            #res = self.env['report'].get_action(self.product_ids,
            #'stock_move_report.report_stock_move_pdf_xls', data=data)
            #return res

    date_from=fields.Date('Start Date',required=True)
    date_to=fields.Date('End Date',required=True)
    include_costs=fields.Boolean('Include costs')
    category_ids=fields.Many2many('product.category','Category Product')
    product_ids=fields.Many2many('product.product','Product')
    partner_ids = fields.Many2many('res.partner','Company')
    location_src_ids=fields.Many2many('stock.location','Source Location')
    location_dest_ids=fields.Many2many('stock.location','Destination Location')
    picking_type_ids = fields.Many2many('stock.picking.type','Picking Type')
    out_format=fields.Selection([('qweb-PDF', 'Portable Document Format (.pdf)')],'Print Format',required=True)
    #out_format=fields.Selection([('qweb-PDF', 'Portable Document Format (.pdf)'), ('qweb-XLS','Microsoft Excel 97/2000/XP/2003 (.xls)')], string="Print Format",required=True)
    
    _defaults={
              out_format:'qweb-PDF',
              date_from: lambda *a: time.strftime('%Y-%m-%d'),
              date_to: lambda *a: time.strftime('%Y-%m-%d'),
              include_costs: False,
              }