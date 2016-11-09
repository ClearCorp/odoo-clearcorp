# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import date


class ProjectIssue(models.Model):

    _inherit = 'project.issue'

    # Related approvals.
    prepaid_hours_approval_id = fields.One2many(
        'sale.subscription.prepaid_hours_approval', 'ticket_id',
        string="Approval")

    # Approved hours for this issue.
    approved_hours_id = fields.One2many(
        'sale.subscription.prepaid_hours_assigned', 'assigned_hours_id',
        string='Approved Hours for this Issue')

    # Feature that will solve this issue. There should be a unique feature
    # related to a unique issue, but there isn't a one to one related field.
    # This relates many issues to one feature, but it's not meant to be used
    # that way.
    feature_id = fields.Many2one(
        'project.scrum.feature',
        string='Feature',
        help='The Issue must have a related Feature to add approvals.')

    def change_proposal_status_approved(self):
        # Finishes the creation of approval lines and changes approval's status
        # to 'approved'.
        return

    def _get_prepaid_hours(self):
        self.feature_id.work_type

    def _create_approval_line(self, approval_id):
        # Loops over the types of work needed and compares it to the types
        # in a client's subscription. It has to check the correct client's
        # Subscription and it needs a related Feature.
        approval_line_obj = self.env[
            'sale.subscription.prepaid_hours_approval_line']
        client_id = self.company_id or self.partner_id
        client_subscription = self.env['sale.subscription'].search(
            [('partner_id', '=', client_id.id)])
        # Loops over the types of work that have to be done
        for hour_type in self.feature_id.hour_ids:
            print "\n\n", hour_type
            approval_line_values = {}
            prepaid_hours_id = False
            wt = hour_type.work_type_id
            # Loops over subscription's issue_type_ids
            for invoice_type in client_subscription.invoice_type_ids:
                # Selects the correct type of work and its corresponding
                # prepaid hours id
                if wt.id == invoice_type.name.id:
                    prepaid_hours_id = invoice_type.prepaid_hours_id.id
            approval_line_values.update({
                'prepaid_hours_id': prepaid_hours_id,
                'approval_id': approval_id,
                'work_type_id': hour_type.work_type_id.id,
                'requested_hours': hour_type.expected_hours,
                # The approval line doesn't know the extra hours/amount yet.
                # If the proposal is accepted, this fields will be filled
                # later.
            })
            res = approval_line_obj.create(approval_line_values)
            print "\n create approval line: ", res

    def create_formatted_proposal(self, approval_id):
        # Creates a proposal table for the client to approve. It needs an
        # approval that is still in 2bapproved state and a related feature with
        # the necessary expected hours. This calls for the creation of
        # proposed_hour_values and its related approval_line.
        self._create_approval_line(approval_id)
        self._create_proposed_hour_values(approval_id)
        current_approval = self.env[
            'sale.subscription.prepaid_hours_approval'].search(
            [('approval_id', '=', approval_id)])
        # approval test
        return current_approval._get_table()

        # Calls Hour Approval class for the formatting
        # Creates

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
        approval_obj.create(approval_values)
        return True
