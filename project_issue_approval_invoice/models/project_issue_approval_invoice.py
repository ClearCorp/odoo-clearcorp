# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta
from openerp import models, fields, api
from datetime import date
import datetime


class account_analitic_account(models.Model):

    _inherit = 'account.analytic.account'

    journal_invoice = fields.Many2one('account.journal')

    def get_product(self, work_type):
            product = self.invoice_type_id.search([('name', '=', work_type)])
            return product.product_id.id

    def get_product_price(self, work_type):
            product_price = self.invoice_type_id.search(
                [('name', '=', work_type), ('product_price', '=', True)])
            return product_price.product_price

    def get_price_hour(self, work_type):
            price_hour = self.invoice_type_id.search(
                [('name', '=', work_type)])
            return price_hour.price

    def get_contract_price(self, work_type, hours):
        cost = self.invoice_type_id.search([('name', '=', work_type)])
        cost = cost.price * hours
        return cost

    @api.multi
    def action_invoice_lines_approvals_create(
            self, invoice_id, account_invoice_id, account_analytic_id):
        invoice_line_obj = self.env['account.invoice.line']
        prepaid = self.env['account.analytic.prepaid_hours_approval'].search(
            [('state', '=', 'approved')])
        for approval in prepaid:
            if approval.ticket_id.project_id.analytic_account_id.id ==\
                    account_analytic_id:
                prepaid_line =\
                    self.env[
                        'account.analytic.prepaid_hours_approval_line'].search(
                            [('approval_id', '=', approval.id)])
                for line in prepaid_line:
                    invoice_line_vals = {
                        'invoice_id': invoice_id,
                        'product_id': self.get_product(line.work_type_id.name),
                        'name': "Inc: " + str(line.approval_id.ticket_id.id) +
                                "-" + line.work_type_id.name,
                        'account_id': account_invoice_id,
                        'account_analytic_id': account_analytic_id,
                        'quantity': line.extra_hours,
                        'price_unit': line.extra_amount / line.extra_hours,
                        'price_subtotal': line.extra_amount,
                    }
                    invoice_line_obj.create(invoice_line_vals)
            return True

    @api.multi
    def action_invoice_create_lines(self, invoice_create_id,
                                    account_invoice_id, account_analytic_id):
        invoice_line_obj = self.env['account.invoice.line']
        for line_invoice in account_analytic_id.recurring_invoice_line_ids:
            invoice_line_vals = {
                'invoice_id': invoice_create_id,
                'product_id': line_invoice.product_id.id,
                'name': line_invoice.name,
                'account_id': account_invoice_id,
                'account_analytic_id': account_analytic_id.id,
                'quantity': line_invoice.quantity,
                'uom_id': line_invoice.uom_id.id,
                'price_unit': line_invoice.price_unit,
                'price_subtotal': line_invoice.price_subtotal,
            }
            invoice_line_obj.create(invoice_line_vals)
            return True

    @api.multi
    def action_invoice_create(self):
        today = date.today().strftime('%Y-%m-%d')
        invoice_obj = self.env['account.invoice']
        for account in self.env['account.analytic.account'].search(
                [('state', 'in', ['open', 'pending']),
                 ('recurring_invoices', '=', True),
                 ('recurring_next_date', '<=',  today)]):
            while account.recurring_next_date <= today:
                    account_invoice_id =\
                        account.partner_id.property_account_receivable.id
                    invoice_vals = {
                        'partner_id':  account.partner_id.id,
                        'journal_id': account.journal_invoice.id,
                        'account_id': account_invoice_id,
                        'currency_id': account.currency_invoice.id,
                        'date_invoice': today,
                    }
                    invoice_create_id = invoice_obj.create(invoice_vals)
                    self.action_invoice_create_lines(
                        invoice_create_id.id, account_invoice_id, account)
                    self.action_invoice_lines_approvals_create(
                        invoice_create_id.id, account_invoice_id, account.id)
                    # The new date to invoicing
                    next_date = datetime.datetime.strptime(
                        account.recurring_next_date or today, "%Y-%m-%d")
                    interval = account.recurring_interval
                    if account.recurring_rule_type == 'daily':
                        new_date = next_date+relativedelta(days=+interval)
                    elif account.recurring_rule_type == 'weekly':
                        new_date = next_date+relativedelta(weeks=+interval)
                    elif account.recurring_rule_type == 'monthly':
                        new_date = next_date+relativedelta(months=+interval)
                    else:
                        new_date = next_date+relativedelta(years=+interval)
                        account.write(
                            {'recurring_next_date':
                             new_date.strftime('%Y-%m-%d')
                             })
        return True

    @api.model
    def action_invoice_create_api7(self):
        self.action_invoice_create()
