# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import date


class PrepaidHoursType(models.Model):
    # Classifies prepaid hours as development, support, or training.
    # This classification is a product, so the price of hours can be
    # defined using pricelists.

    # Extra hours are needed for approval and invoicing. They don't have a
    # related prepaid hours object.
    # todo Load extra hours data in data file.
    _name = 'sale.subscription.prepaid_hours_type'
    _inherit = 'product.product'

    hour_type = fields.Selection(
        [('dev', 'Development Hours'),
         ('sup', 'Support Hours'),
         ('tra', 'Training Hours'),
         ],
        string='Hour Type', required=True)


class PrepaidHours(models.Model):
    # Represents the prepaid hours clients can have in their subscription
    # (the client's "hour bag").
    _name = 'sale.subscription.prepaid_hours'

    name = fields.Many2one(
        'sale.subscription.prepaid_hours_type', string='Type of Hour',
        required=True)

    # Amount of hours of a certain type
    quantity = fields.Float('Amount of Hours', required=True)

    # One subscription has many prepaid hours
    subscription_id = fields.Many2one(
        'sale.subscription', string='Subscription')

    # Creation date of this subscription's prepaid hours
    date = fields.Datetime('Date', required=True)

    # If inactive the hours are hidden
    active = fields.Boolean('Active', default=True)


class AssignedPrepaidHours(models.Model):
    # Represents assigned hours to a specific Feature.
    _name = 'sale.subscription.prepaid_hours.assigned'

    # Date when the work hours were assigned
    date = fields.Datetime('Date:', required=True)

    # Amount of hours assigned
    quantity = fields.Float('Amount of Hours', required=True)

    # Specific "hour bag" to use
    prepaid_hours_id = fields.Many2one(
        'sale.subscription.prepaid_hours',
        required=True)


class PrepaidHoursApprovedValues(models.Model):
    # When the use of hours is going to be approved the details are stored
    # here. This is presented to the client, who then chooses what to do. Once
    # presented, this should not change. This object is only one of the current
    # "hour bags".
    _name = 'sale.subscription.prepaid_hours_approved_values'

    # The type of hours
    prepaid_hours_id = fields.Many2one('sale.subscription.prepaid_hours')

    # Amount of approved hours in the term
    prepaid_hours = fields.Float('Prepaid Hours')

    # Hours already spent in this term
    spent_hours = fields.Float('Spent Hours')

    # Remaining hours in the term
    remaining_hours = fields.Float('Remaining Hours')

    # Total of hours that require approval (this time)
    # todo Check the interpretation of this field
    hours_to_be_approved = fields.Float('Hours Awaiting Approval')

    # Amount of hours requested for a Feature
    requested_hours = fields.Float('Requested Hours')

    # Additional hours not included in the "hour bag"
    extra_hours = fields.Float('Additional Hours Requested')

    # The additional cost of said hours.
    extra_amount = fields.Float('Additional Amount Requested')

    # Several approved values are related to one approval
    approval_id = fields.Many2one('sale.subscription.prepaid_hours_approval')


class PrepaidHoursApprovalLines(models.Model):
    _name = 'sale.subscription.prepaid_hours_approval_line'

    prepaid_hours_id = fields.Many2one('sale.subscription.prepaid_hours')
    approval_id = fields.Many2one('sale.subscription.prepaid_hours_approval')
    work_type_id = fields.Many2one('project.work.type')
    requested_hours = fields.Float('Feature hours')
    extra_hours = fields.Float('Additional Hours Required')
    extra_amount = fields.Float('Additional Amount Required')


class SaleSubscription(models.Model):

    _inherit = 'sale.subscription'

    prepaid_hours_id = fields.One2many(
        'sale.subscription.prepaid_hours', 'subscription_id')

    def create_subscription_prepaid_hours_assigned(self):
        today = date.today().strftime('%Y-%m-%d')
        contracts = self.env['account.analytic.account'].search([])
        prepaid_hours_id =\
            self.env['sale.subscription.prepaid_hours'].search([])
        prepaid_hours_assigned =\
            self.env['sale.subscription.prepaid_hours.assigned']
        for contract in contracts:
            for qty_qroup in prepaid_hours_id:
                if qty_qroup.analitic_account_id.id == contract.id:
                    vals = {
                        'date': today,
                        'quantity': qty_qroup.quantity,
                        'group_id': qty_qroup.id,
                    }
                    prepaid_hours_assigned.create(vals)
        return True

    @api.model
    def create_account_analytic_prepaid_hours_assigned_api7(self):
        self.create_subscription_prepaid_hours_assigned()


class InvoiceType(models.Model):
    _inherit = 'invoice.type'

    prepaid_hours_id = fields.Many2one(
        'sale.subscription.prepaid_hours', string="Prepaid hours")
