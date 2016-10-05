# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import date


class SubscriptionPrepaidHours(models.Model):
    # Represents the different types of hours that can be bought.
    _name = 'sale.subscription.prepaid_hours'

    name = fields.Char('Name', required=True)
    quantity = fields.Float('Quantity', required=True)
    subscription_id = fields.Many2one(
        'sale.subscription', string='Subscription')
    date = fields.Datetime('Date', required=True)
    active = fields.Boolean('Active', default=True)


class SubscriptionPrepaidHoursAssignment(models.Model):
    # Represents assigned hours to a specific Feature
    _name = 'sale.subscription.prepaid_hours.assignment'

    date = fields.Datetime('Date:', required=True)
    quantity = fields.Float('Quantity', required=True)
    group_id = fields.Many2one('sale.subscription.prepaid_hours', required=True)


class SubscriptionPrepaidHoursApprovedValues(models.Model):
    _name = 'sale.subscription.prepaid_hours_approved_values'

    prepaid_hours_id = fields.Many2one('sale.subscription.prepaid_hours')
    prepaid_hours = fields.Float('Prepaid Hours')
    spent_hours = fields.Float('Spent Hours')
    remaining_hours = fields.Float('Remaining Hours')
    hours_to_be_approved = fields.Float('Hours Awaiting Approval')
    requested_hours = fields.Float('Requested Hours')
    extra_hours = fields.Float('Additional Hours Requested')
    extra_amount = fields.Float('Additional Amount Requested')
    approval_id = fields.Many2one('sale.subscription.prepaid_hours_approval')


class SubscriptionPrepaidHoursApprovalLines(models.Model):
    _name = 'sale.subscription.prepaid_hours_approval_line'

    prepaid_hours_id = fields.Many2one('sale.subscription.prepaid_hours')
    approval_id = fields.Many2one('sale.subscription.prepaid_hours_approval')
    work_type_id = fields.Many2one('project.work.type')
    requested_hours = fields.Float('Feature hours')
    extra_hours = fields.Float('Extra hours')
    extra_amount = fields.Float('Extra amount')


class SaleSubscription(models.Model):

    _inherit = 'sale.subscription'

    prepaid_hours_id = fields.One2many(
        'sale.subscription.prepaid_hours', 'subscription_id')

    def create_subscription_prepaid_hours_assignment(self):
        today = date.today().strftime('%Y-%m-%d')
        contracts = self.env['account.analytic.account'].search([])
        prepaid_hours_id =\
            self.env['sale.subscription.prepaid_hours'].search([])
        prepaid_hours_assignment =\
            self.env['sale.subscription.prepaid_hours.assignment']
        for contract in contracts:
            for qty_qroup in prepaid_hours_id:
                if qty_qroup.analitic_account_id.id == contract.id:
                    vals = {
                        'date': today,
                        'quantity': qty_qroup.quantity,
                        'group_id': qty_qroup.id,
                    }
                    prepaid_hours_assignment.create(vals)
        return True

    @api.model
    def create_account_analytic_prepaid_hours_assignment_api7(self):
        self.create_subscription_prepaid_hours_assignment()


class InvoiceType(models.Model):
    _inherit = 'invoice.type'

    prepaid_hours_id = fields.Many2one(
        'sale.subscription.prepaid_hours', string="Prepaid hours")
