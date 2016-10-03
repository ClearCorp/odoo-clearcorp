# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class WorkType(models.Model):
    
    _name = 'project.work.type'
    _order = 'sequence'
    
    name = fields.Char('name', size=128, required=True)
    product_id = fields.Many2one(
        'product.product', string='Product', required='True')
    sequence = fields.Integer('Sequence', required=True)
    column_number = fields.Integer('Column Number', required=True)


class InvoiceType (models.Model):
    _name = 'invoice.type'
    
    name = fields.Many2one('project.work.type', required='True')
    product_price = fields.Boolean('Use product price')
    product_id = fields.Many2one('product.product')
    price = fields.Float('Price')
    # This relates the client's Subscription (contract) with the different
    # invoice types.
    contract_type_ids = fields.Many2many('sale.subscription')
    
    @api.one
    @api.onchange('name')
    def onchange_name(self):
        self.product_id = self.name.product_id
        return True


class Task(models.Model):
    
    _inherit = 'project.task'
    work_type_id = fields.Many2one(
        'project.work.type', 'Task Type', required=True)


class SaleSubscription(models.Model):

    _inherit = 'sale.subscription'
    invoice_type_ids = fields.Many2many('invoice.type')
