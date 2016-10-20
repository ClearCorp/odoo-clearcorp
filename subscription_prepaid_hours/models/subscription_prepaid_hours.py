# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import date


class PrepaidHours(models.Model):
    # Represents the prepaid hours clients can have in their subscription
    # (the client's "hour bag").
    _name = 'sale.subscription.prepaid_hours'

    # Classifies prepaid hours as development, support, or training.
    name = fields.Selection(
        [('dev', 'Development Hours'),
         ('sup', 'Support Hours'),
         ('tra', 'Training Hours'),
         ],
        string='Hour Type', required=True)

    # Amount of hours of a certain type
    quantity = fields.Float('Amount of Hours', required=True)

    # One subscription has several prepaid hours
    subscription_id = fields.Many2one(
        'sale.subscription', string='Subscription')

    # Creation date of this subscription's prepaid hours
    date = fields.Datetime('Date', required=True)

    # If inactive the hours are hidden
    active = fields.Boolean('Active', default=True)


class HourAssignment(models.Model):
    # Represents assigned hours to a specific Issue.
    _name = 'sale.subscription.prepaid_hours_assigned'

    # Date when the work hours were assigned
    date = fields.Datetime('Date:', required=True)

    # Amount of hours assigned
    quantity = fields.Float('Amount of Hours', required=True)

    # Specific "hour bag" used
    prepaid_hours_id = fields.Many2one(
        'sale.subscription.prepaid_hours',
        required=True)

    # Issue related to this hour assignment
    assigned_hours_id = fields.Many2one(
        'project.issue', string='Assigned Hours')


class ProposedHourValues(models.Model):
    # When the use of hours is going to be approved the details are stored
    # here. This is presented to the client, who then chooses what to do. Once
    # presented, this should not change. This object is only one of the current
    # "hour bags".
    # Several proposals could be added and only the one approved by the client
    # will become an actual approval line.
    _name = 'sale.subscription.prepaid_hours_approved_values'

    # The type of hours
    prepaid_hours_id = fields.Many2one('sale.subscription.prepaid_hours')

    # Amount of prepaid hours in the current term
    prepaid_hours = fields.Float('Prepaid Hours')

    # Hours already spent in this term
    spent_hours = fields.Float('Spent Hours')

    # Remaining hours in the term
    remaining_hours = fields.Float('Remaining Hours')

    # Total of hours that require approval (this time)
    hours_to_be_approved = fields.Float('Requested Hours Awaiting Approval')

    # Additional hours not included in the "hour bag"
    # If hours are not obtained from a bag, they are always extra
    extra_hours = fields.Float('Additional Hours Requested')

    # The additional cost of said hours.
    extra_amount = fields.Float('Additional Amount Requested')

    # Several approved values are related to one approval
    approval_id = fields.Many2one('sale.subscription.prepaid_hours_approval')


class ApprovalLines(models.Model):
    # When an approval is issued, this is the content of the specific view.
    # A line summarizes an approval, like invoice lines.
    _name = 'sale.subscription.prepaid_hours_approval_line'

    prepaid_hours_id = fields.Many2one('sale.subscription.prepaid_hours')
    approval_id = fields.Many2one('sale.subscription.prepaid_hours_approval')
    work_type_id = fields.Many2one('project.work.type')
    requested_hours = fields.Float('Requested Hours')
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
            self.env['sale.subscription.prepaid_hours_assigned']
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
