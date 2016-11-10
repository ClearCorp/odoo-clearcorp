# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
#from lxml import etree
from table_format import APP_ID, PREPAID_NAME, PREPAID_TIME, FOOTER
from openerp.exceptions import ValidationError


class HourApproval(models.Model):
    _name = 'sale.subscription.prepaid_hours_approval'

    @api.model
    def _default_sequence(self):
        #print self.env.context
        approval_sequence =\
            self.env['sale.subscription.prepaid_hours_approval'].search_count(
                [('ticket_id', '=',
                  self.env.context.get('default_ticket_id')),
                 ('user_id', '=',
                  self.env.context.get('user_id'))
                 ])
        return approval_sequence + 1

    ticket_id = fields.Many2one('project.issue', string='Ticket')
    sequence = fields.Integer('Sequence', default=_default_sequence)
    user_id = fields.Many2one('res.partner', string='Customer')
    date = fields.Date('Date')
    state = fields.Selection([('2b_approved', 'To be approved'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected')],
                             string='State', default='2b_approved')
    approval_line_ids = fields.One2many(
        'sale.subscription.prepaid_hours_approval_line', 'approval_id',
        string='Approval Lines')
    approval_values = fields.One2many(
        'sale.subscription.prepaid_hours_approved_values', 'approval_id',
        string='Approval Values')

    def _check_prepaid_hours(self, prepaid_hours_id):
        times = self._check_approved_lines()
        time_already_approved = times.get('time_already_approved')
        remaining_time = prepaid_hours_id.quantity - time_already_approved
        times['remaining_time'] = remaining_time
        return times

    def _check_approval_lines(self):
        time_already_approved = 0
        time_to_be_approved = 0
        # Gets previously approved lines for the current approval (in an issue)
        for approval_line in self.approval_line_ids:
            if approval_line.approval_id.state == 'approved':
                time_already_approved = time_already_approved + \
                                        approval_line.requested_hours
            else:
                if approval_line.approval_id.state == '2b_approved':
                    time_to_be_approved = time_to_be_approved + \
                                          approval_line.requested_hours
        return {
            'time_already_approved': time_already_approved,
            'time_to_be_approved': time_to_be_approved,
        }

    @api.multi
    @api.depends('user_id')
    def fill_proposed_hour_values(self):
        # Fills proposed hour values for a given approval.
        # Gets related client's subscription.
        client_id = self.user_id
        client_subscription = self.env['sale.subscription'].search(
            [('partner_id', '=', client_id.id)])

        # Adds all of the prepaid hours to a list
        hour_bags = []
        # And the bags to a dict
        prepaid_hours = {}
        for hour_bag in client_subscription.prepaid_hours_id:
            hour_bags.append(hour_bag.name)
            prepaid_hours[hour_bag.name] = hour_bag

        # Processes the different hour bags a client's subscription has, to
        # fill proposed_hour_values.
        for proposed_values in self.approval_values:
            hour_type = proposed_values.prepaid_hours_id.name

            if hour_type in hour_bags:
                current_bag = prepaid_hours[hour_type]
                if current_bag.active:
                    current_bag_values = self._check_prepaid_hours(current_bag)
                    extra_hours = abs(current_bag_values['remaining_time'] -
                                      proposed_values.requested_hours)
                    extra_amount = 0.0
                    if extra_hours > 0.0:
                        extra_amount = self._calculate_extra_amount(
                            hour_type, extra_hours)
                    proposal_values = {
                        'prepaid_hours': current_bag.quantity,
                        'time_already_approved':
                            current_bag_values['time_already_approved'],
                        'remaining_hours': current_bag_values['remaining_time'],
                        'hours_to_be_approved':
                            current_bag_values['time_to_be_approved'],
                        'extra_hours': extra_hours,
                        # There is an extra amount to be calculated according
                        # to the type of (extra) hour that depends on the type
                        # of bag.
                        'extra_amount': extra_amount
                    }
            else:
                extra_hours = proposed_values.requested_hours
                approval_line_times = self._check_approval_lines()
                proposal_values = {
                    'prepaid_hours': 0.0,
                    'time_already_approved':
                        approval_line_times['time_already_approved'],
                    'remaining_hours': 0.0,
                    'hours_to_be_approved':
                        approval_line_times['time_to_be_approved'],
                    'extra_hours': extra_hours,
                    # There is an extra amount to be calculated according
                    # to the type of (extra) hour that depends on the type
                    # of bag.
                    'extra_amount': self._calculate_extra_amount(
                        hour_type, extra_hours)
                }

            proposed_values.update(proposal_values)
            print "\n Proposal values: ", proposal_values
            self._fill_extra_values_approval_line(
                hour_type, extra_hours, extra_amount)

    def _fill_extra_values_approval_line(
            self, hour_type, extra_hours, extra_amount):
        return

    # TODO define unique constraint prepaid_hours_id for approval_lines

    def _calculate_extra_amount(self, prepaid_hour_name, hours):
        # Calculates the amount the client has to pay for the extra hours
        # required to attend an issue.
        extra_amount = 0.0
        validation_error = "There was an error calculating the extra amount." \
                           "There must be a related invoice type of the " \
                           "same general work hours type as the prepaid " \
                           "hours types."

        # The unit cost is obtained through the client's subscription.
        client_id = self.user_id
        client_subscription = self.env['sale.subscription'].search(
            [('partner_id', '=', client_id.id)])
        invoice_types = client_subscription.invoice_type_ids

        # Only if invoice_type.is_extra is true its price is taken into
        # account. If there is more than 1 invoice_type labeled as 'extra'
        # for a general_work_type, the calculation could be wrong.
        for product in invoice_types:
            if product.is_extra and \
                            prepaid_hour_name == product.general_work_type:
                extra_amount += product.price * hours
        # The hours can't be zero when this is called, so
        if extra_amount == 0.0:
            raise ValidationError(validation_error)
        return extra_amount

    def create_approval_line(self):
        # Fills approval line data and creates basic data for related
        # proposal.
        # Gets the hours needed to complete the feature / fix the issue.
        expected_hours = self.ticket_id.feature_id.expected_hours
        validation_error = "There was an error checking the expected hours " \
                           "of the related feature and the requested hours. " \
                           "The requested hours must be less than the " \
                           "expected hours in the feature."

        # Checks if the requested time is less than the total time allowed.
        for approval_line in self.approval_line_ids:
            if approval_line.requested_hours > expected_hours:
                raise ValidationError(validation_error)
            # Creates a proposal for each line
            vals = {
                'prepaid_hour_id': approval_line.prepaid_hours_id,
                'requested_hours': approval_line.requested_hours,
                'approval_id': approval_line.approval_id
            }
            self.approval_values = [(0, 0, vals)]

    def _get_approval_line_by_prepaid_hours(self, ticket):
        # Gets work_type ids from ticket
        wt_feature_ids = [hours.work_type_id.id
                          for hours in ticket.feature_id.hour_ids]

        # Gets invoice_type related to the ticket's project contract,
        # this should return the client's subscription
        invoice_type_ids = self.env['invoice.type'].search(
            [('contract_type_ids',
              '=', ticket.project_id.analytic_account_id.subscription_ids.id),
             ('name', 'in', wt_feature_ids)], order='price desc')

        data = []
        for line in invoice_type_ids:
            data.append(
                {'wt_id': line.name.id,
                 'prepaid': line.prepaid_hours_id.id,
                 'price':
                 line.product_id.lst_price if line.product_price
                    else line.price})
        wt_contract = [it.prepaid_hours_id.id for it in invoice_type_ids]
        print "\nInvoice Lines", wt_feature_ids, wt_contract, data

    def _get_current_month_consumed_hours(self, ticket_id):
        date = fields.Date.from_string(fields.Date.today())
        analytic_id = ticket_id.project_id.analytic_account_id.id

        query = """select id, date from sale_subscription_prepaid_hours
                    where extract(month from date) = %s and
                    extract(year from date) = %s and
                    subscription_id = %s""" % (date.month, date.year,
                                               analytic_id)

        query2 = """
                select id, date from sale_subscription_prepaid_hours_approval
                    where extract(month from date) = %s and
                    extract (year from date) = %s and
                    ticket_id = %s and
                    state = '%s'""" % (date.month, date.year, ticket_id.id,
                                       'approved')
        self._cr.execute(query)

        prepaid_hours = self.env['sale.subscription.prepaid_hours'].browse(
            [ids['id'] for ids in self._cr.dictfetchall()])

        self._cr.execute(query2)

        approvals = self.env['sale.subscription.prepaid_hours_approval'].\
            browse([ids['id'] for ids in self._cr.dictfetchall()])

        print "-----", date, prepaid_hours, approvals, "--------"
        self._get_approval_line_by_prepaid_hours(ticket_id)

    def _get_approval_lines(self, issue_id):
        lines = {
            'hours': '',
            'names': ''
        }
        ticket_id = self.env['project.issue'].browse(
            self._context.get('issue_id'))
        approval = ticket_id.prepaid_hours_approval_id[0]
        for line in approval.approval_line_ids:
            lines['names'] += '<li>%s</li>' % line.work_type_id.name
            lines['hours'] += '<li>%s</li>' % (line.requested_hours*10000)
        print "\nLines: ", lines, self.approval_line_ids
        return lines

    def _get_prepaid_hours(self):
        prepaid_hours = {
            'quantity': '',
            'names': ''
        }
        ticket_id = self.env['project.issue'].browse(
            self._context.get('issue_id'))
        for prepaid in\
                ticket_id.project_id.analytic_account_id.prepaid_hours_id:
            quantity = '<td style="text-align:right">%s</td>' %\
                (prepaid.quantity*10000)
            prepaid_hours['quantity'] += quantity
            name = '<th style="text-align:right; width:25%s">%s</th>' % (
                '%', prepaid.name)
            # todo Check for correct concatenation
            prepaid_hours['names'] += name
        print "\nprepaid: ", prepaid_hours,
        return prepaid_hours

    def _get_table(self):
        ticket_id = self.env['project.issue'].browse(
            self._context.get('issue_id'))
        self._get_current_month_consumed_hours(ticket_id)
        approvals = ticket_id.prepaid_hours_approval_id
        _TABLE = """<group col="1" colspan="1">"""
        for approval in approvals:
            print approval.id
            _TABLE += APP_ID + str(approval.id) + PREPAID_NAME + \
                self._get_prepaid_hours()['names'] + \
                PREPAID_TIME + \
                str(self._get_prepaid_hours()['quantity']) +\
                """
                </tr>
                <tr>
                    <td>Horas Consumidas</td>
                    <td style="text-align:right">-</td>
                </tr>
                <tr style="border-top:1px solid black">
                    <td style="padding-bottom:16px">
                        <b>Horas Restantes</b>
                    </td>
                    <td style="text-align:right">
                        <b>-</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        <b>Horas por aprobar</b>
                    </td>
                    <td style="text-align:right">
                        <b>SUMA APPROVALS</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        <b>Horas requeridas</b>
                        <ul style="list-style-type:none">""" +\
                self._get_approval_lines(0)['names'] +\
                """
                        </ul>
                    </td>
                    <td style="text-align:right">
                        <b>SUMA</b>
                        <ul style="list-style-type:none">""" +\
                str(self._get_approval_lines(0)['hours']) +\
                FOOTER
        _TABLE += "</group>"
        return _TABLE

    @api.multi
    def do_approve_approval(self):
        approval_id = self._context.get('approval_id')
        print self._context
        if approval_id:
            print "\napproval_id: ", approval_id

"""    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):

        if self._context is None:
            self._context = {}
        res = super(HourApproval, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=False)
        doc = etree.fromstring(res['arch'])
        table = etree.fromstring(self._get_table())
        # print etree.tostring(table, pretty_print=True)
        for node in doc.iter():
            if node.tag == 'sheet':
                node.append(table)
                break
            # print node.tag, type(node)
        # print etree.tostring(doc, pretty_print=True)
        res['arch'] = etree.tostring(doc, pretty_print=True)
        return res"""
