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

    def start_approval(self, vals):
        # Creates a new approval
        approval = self._create_approval()
        # Creates a new approval line, minus a few fields
        self._create_approval_line(approval.id)


        # Creates

    def _get_prepaid_hours(self):
        self.feature_id.work_type

    def _values(self, prepaid_hours_id):
        used_time = 0
        to_be_approved_time = 0
        approval_lines_obj = self.env[
            'sale.subscription.prepaid_hours_approval_line'].search(
                [('prepaid_hours_id', '=', prepaid_hours_id)])
        for approval_line in approval_lines_obj:
            if approval_line.approval_id.state == 'approved':
                    used_time = used_time + approval_line.requested_hours
            else:
                if approval_line.approval_id.state == '2b_approved':
                    to_be_approved_time = to_be_approved_time +\
                        approval_line.requested_hours
        remaining_time = prepaid_hours_id.quantity - used_time
        return {
            'used_time': used_time,
            'to_be_approved_time': to_be_approved_time,
            'remaining_time': remaining_time,
        }

    def _calculate_extra_amount(self):
        _type = self.feature_id
        _price = self.project_id.analytic_account_id.invoice_type_id.search(
            [('name', '=', '')]).product_price

    def _create_approval_values(self, approval_id, prepaid_hours_id):
        _approval_values_obj = self.env[
            'sale.subscription.prepaid_hours_approved_values']
        values = self._values(prepaid_hours_id)
        _approval_values_values = {
            'prepaid_hours_id': prepaid_hours_id,
            'prepaid_hours': prepaid_hours_id.quantity,
            'spent_hours': values['used_time'],
            'remaining_hours': values['remaining_time'],
            'to_be_approved': values['to_be_approved_time'],
            # There has to be a related feature, where the time has been
            # estimated.
            'requested_hours': self.task_id.feature_id.expected_hours,
            'extra_hours': values['remaining_time'] -
            self.feature_id.expected_hours,
            # 'extra_amount':,
            'approval_id': approval_id,
        }

    def _create_approval_line(self, approval_id):
        # Loops over the types of work needed and compares it to the types
        # in a clients subscription.
        # It has to check the correct client's Subscription and it needs
        # a related Feature
        approval_line_obj = self.env[
            'sale.subscription.prepaid_hours_approval_line']
        subscription_obj = self.env['sale.subscription']
        # Loops over the types of work that have to be done
        for hour_type in self.task_id.feature_id.hour_ids:
            print "\n\n", hour_type
            approval_line_values = {}
            # Get analytic account id for the subscription
            _ana_acc = self.project_id.analytic_account_id
            prepaid_hours_id = False
            wt = hour_type.work_type_id
            for invoice_type in _ana_acc.invoice_type_id:
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
