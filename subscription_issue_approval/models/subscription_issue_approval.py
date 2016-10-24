# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields
from datetime import date


class ProjectIssue(models.Model):

    _inherit = 'project.issue'

    # Related approvals.
    prepaid_hours_approval_id = fields.One2many(
        'sale.subscription.prepaid_hours_approval', 'ticket_id',
        string="Group Approved")

    # Approved hours for this issue.
    approved_hours_id = fields.One2many(
        'sale.subscription.prepaid_hours_assigned', 'assigned_hours_id',
        string='Approved Hours for this Issue')

    # Feature that will solve this issue. There should be a unique feature
    # related to a unique issue, but there isn't a one to one related field.
    feature_id = fields.Many2one('project.scrum.feature', string='Feature')

    def start_approval(self):
        # Starts the approval - proposal - client's go ahead - invoice cycle.
        # Creates a new approval
        approval = self._create_approval()
        # Creates a new approval line, minus a few fields
        self._create_approval_line(approval.id)
        self._create_proposed_hour_values(approval.id)

    def create_formatted_proposal(self, vals):
        # Creates a proposal table for the client to approve. It needs an
        # approval that is still in 2bapproved state.
        # It loops over the different prepaid hours in a subscription
        # to subtract the hours for its proposed use.
        # vals contain all the types of hours required (amounts) and the
        # approval_id.
        return

        # Calls Hour Approval class for the formatting
        # Creates

    def _get_prepaid_hours(self):
        self.feature_id.work_type

    def _values(self, prepaid_hours_id):
        time_already_approved = 0
        to_be_approved_time = 0
        approval_lines_obj = self.env[
            'sale.subscription.prepaid_hours_approval_line'].search(
                [('prepaid_hours_id', '=', prepaid_hours_id)])
        for approval_line in approval_lines_obj:
            if approval_line.approval_id.state == 'approved':
                    time_already_approved = time_already_approved + \
                                            approval_line.requested_hours
            else:
                if approval_line.approval_id.state == '2b_approved':
                    to_be_approved_time = to_be_approved_time +\
                        approval_line.requested_hours
        remaining_time = prepaid_hours_id.quantity - time_already_approved
        return {
            'time_already_approved': time_already_approved,
            'to_be_approved_time': to_be_approved_time,
            'remaining_time': remaining_time,
        }

    def _calculate_extra_amount(self, subscription, hours):
        # Calculates the amount the client has to pay for the extra hours
        # required to attend an issue.
        extra_amount = 0.0

        # The unit cost is obtained through the client's subscription.
        invoice_types = subscription.invoice_type_ids

        # Only the 'extra' type is relevant
        for product in invoice_types:
            if invoice_types.general_work_type == 'extra':
                extra_amount += invoice_types.price * hours

        return extra_amount

    def _create_proposed_hour_values(self, approval_id):
        # Fills proposed hour values for a given approval.
        client_id = self.company_id or self.partner_id
        client_subscription = self.env['sale.subscription'].search(client_id)
        approval_values_obj = self.env[
            'sale.subscription.prepaid_hours_approved_values']

        # Processes the different hour bags a client's subscription has, to
        # create proposed_hour_values.
        for hour_bag in client_subscription.prepaid_hours_id:
            # The hour_bag should be active.
            issue_values = self._values(hour_bag)
            extra_hours = issue_values['remaining_time'] - \
                          self.feature_id.expected_hours
            proposal_values = {
                'prepaid_hours_id': hour_bag,
                'prepaid_hours': hour_bag.quantity,
                'time_already_approved': issue_values['time_already_approved'],
                'requested_hours': self.feature_id.expected_hours,
                'extra_hours': extra_hours,
                'extra_amount': self._calculate_extra_amount(client_subscription, extra_hours),
                'approval_id': approval_id,
            }
            proposal = approval_values_obj.create(proposal_values)
            print "\n Proposal values: ", proposal

    def _create_approval_line(self, approval_id):
        # Loops over the types of work needed and compares it to the types
        # in a client's subscription.
        # It has to check the correct client's Subscription and it needs
        # a related Feature.
        approval_line_obj = self.env[
            'sale.subscription.prepaid_hours_approval_line']
        client_id = self.company_id or self.partner_id
        client_subscription = self.env['sale.subscription'].search(client_id)
        # Loops over the types of work that have to be done
        for hour_type in self.feature_id.hour_ids:
            print "\n\n", hour_type
            approval_line_values = {}
            prepaid_hours_id = False
            wt = hour_type.work_type_id
            # Loops over subscription's issue_type_ids
            for invoice_type in client_subscription.invoice_type_id:
                # Selects the correct type of work and its corresponding
                # prepaid hours id
                if wt.id == invoice_type.name.id:
                    prepaid_hours_id = invoice_type.prepaid_hours_id.id
            approval_line_values.update({
                'prepaid_hours_id': prepaid_hours_id,
                'approval_id': approval_id,
                'work_type_id': hour_type.work_type_id.id,
                'requested_hours': hour_type.expected_hours,
                # 'extra_hours': self._create_approval_line(prepaid_hours_id)
            })
            res = approval_line_obj.create(approval_line_values)
            print "\n create approval line: ", res

    def _create_approval(self):
        # Creates a new approval
        today = date.today().strftime('%Y-%m-%d')
        approval_obj = self.env['sale.subscription.prepaid_hours_approval']
        approval_values = {
            'ticket_id': self.id,
            'user_id': self.user_id.id,
            'date': today,
            'state': '2b_approved',
        }
        res = approval_obj.create(approval_values)
        return res
