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


class ReportStockMoveOrder(models.TransientModel):
    _name = 'report.stock.move.order.wiz'

    stock_location = fields.Many2one('stock.location',
                                     string='Stock Location')
    product_ids = fields.Many2many('product.product',
                                   string='Product')

    @api.multi
    def print_report(self):
        """if not self.product_ids and not self.stock_location:
            doc_ids = self.env['product.product'].search([], order="default_code ASC")
        else:
            location_list_ids=[]
            product_list_ids=[]
            for location in self.stock_location:
                location_list_ids.append(location.id)
            for product in self.product_ids:
                product_list_ids.append(product.id)
            doc_ids = self.env['product.product'].search(['|',('id','in',product_list_ids),('product_tmpl_id.categ_id','in',location_list_ids)] , order="default_code ASC")
        data = {}
        data['form'] = self.read(['stock_location', 'product_ids'])[0]
        res = self.env['report'].get_action(doc_ids,
            'stock_move_report.report_stock_move_order', data=data)
        return res"""
        data = {}
        doc_ids = self
        data['form'] = self.read(['stock_location', 'product_ids'])[0]
        res = self.env['report'].get_action(doc_ids,
            'stock_move_report.report_stock_move_order', data=data)
        return res
        """
        return {'type': 'ir.actions.report.xml',
                'report_name': 'stock_move_report.report_stock_move_order',
                'data': data}
        """