# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from lxml import etree


_TABLE = """
<group>
    <div style="padding-bottom:16px">
        <h2 style="display:inline; margin-right:24px">Approval</h2>
        <span>
            Estado
            <button style="margin-left:16px"
                name="_approve_approval" string="Approve"
                context="{'approval_id': 1}"/>
        </span>
    </div>
    <table>
        <thead>
            <tr>
                <th></th>
                <th style="text-align:right">%s</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Horas Bolsa</td>
                <td style="text-align:right">%s</td>
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
                    <b>SUMA DE OTROS APPROVALS</b>
                </td>
            </tr>
            <tr>
                <td>
                    <b>Horas requeridas</b>
                    <ul style="list-style-type:none">
                        <li>%s</li>
                    </ul>
                </td>
                <td style="text-align:right">
                    <b>SUMA</b>
                    <ul style="list-style-type:none">
                        <li>%s</li>
                    </ul>
                </td>
            </tr>
        </tbody>
    </table>
    </group>"""


class PrepaidHoursApproval(models.Model):
    _name = 'account.analytic.prepaid_hours_approval'

    @api.model
    def _default_sequence(self):
        approval_sequence =\
            self.env['account.analytic.prepaid_hours_approval'].search_count(
                [('ticket_id', '=', self.id)])
        return approval_sequence + 1

    ticket_id = fields.Many2one('project.issue', string='Ticket')
    sequence = fields.Integer('sequence', default=_default_sequence)
    user_id = fields.Many2one('res.partner', string='User')
    date = fields.Date('Date')
    state = fields.Selection([('2b_approved', 'To approved'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected')],
                             string='State', default='2b_approved')
    approval_line_ids = fields.One2many(
        'account.analytic.prepaid_hours_approval_line', 'approval_id',
        string='Approval lines')
    approval_values = fields.One2many(
        'account.analytic.prepaid_hours_approved_values', 'approval_id',
        string='Approval values')

    def _get_approval_line_by_prepaid_hours(self, ticket):
        wt_feature_ids = [hours.work_type_id.id
                          for hours in ticket.feature_id.hour_ids]
        invoice_types_ids = self.env['invoice.type'].search(
            [('contract_type_id', '=', ticket.project_id.analytic_account_id.id
              ),
             ('name', 'in', wt_feature_ids)], order='price desc')
        data = []
        for line in invoice_types_ids:
            data.append(
                {'wt_id': line.name.id,
                 'prepaid': line.prepaid_hours_id.id,
                 'price':
                 line.product_id.lst_price if line.product_price
                    else line.price})
        wt_contract = [it.prepaid_hours_id.id for it in invoice_types_ids]
        print "\n line-bolsa", wt_feature_ids, wt_contract, data

    def _get_consumed_hours(self, ticket_id, approval_id):
        date = fields.Date.from_string(fields.Date.today())
        analityc_id = ticket_id.project_id.analytic_account_id.id
        query = """select id, date from account_analytic_prepaid_hours
                    where extract(month from date) = %s and
                    extract(year from date) = %s and
                    analitic_account_id = %s""" % (date.month, date.year,
                                                   analityc_id)
        query2 = """
                select id, date from account_analytic_prepaid_hours_approval
                    where extract(month from date) = %s and
                    extract (year from date) = %s and
                    ticket_id = %s and
                    state = '%s'""" % (date.month, date.year, ticket_id.id,
                                       'approved')
        self._cr.execute(query)
        prepaid_hours = self.env['account.analytic.prepaid_hours'].browse(
            [ids['id'] for ids in self._cr.dictfetchall()])
        self._cr.execute(query2)
        approvals = self.env['account.analytic.prepaid_hours_approval'].browse(
            [ids['id'] for ids in self._cr.dictfetchall()])
        print "-----", date, query, prepaid_hours, approvals, "--------"
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
            prepaid_hours['names'] += name
        print "\nprepaid: ", prepaid_hours,
        return prepaid_hours

    def _get_table(self):
        ticket_id = self.env['project.issue'].browse(
            self._context.get('issue_id'))
        self._get_consumed_hours(ticket_id, 0)
        approvals = ticket_id.prepaid_hours_approval_id
        _TABLE = """<group col="1" colspan="1">"""
        for approval in approvals:
            print approval.id
            _TABLE += """
    <group>
        <div style="padding-bottom:16px">
            <h2 style="display:inline; margin-right:24px">Approval</h2>
            <span>
                Estado
                <button style="margin-left:16px"
                    name="do_approve_approval" string="Approve" type="object"
                    context="{'approval_id':""" + str(approval.id) + """}"/>
            </span>
        </div>
        <br/>
        <table style="width:100%">
            <thead>
                <tr>
                    <th style="width:25%"></th>
                    """ +\
                self._get_prepaid_hours()['names'] +\
                """
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Horas Bolsa</td>""" +\
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
                """
                        </ul>
                    </td>
                </tr>
            </tbody>
        </table>
        </group><br/>
        """
        _TABLE += "</group>"
        return _TABLE

    @api.multi
    def do_approve_approval(self):
        approval_id = self._context.get('approval_id')
        print self._context
        if approval_id:
            print "\napproval_id: ", approval_id

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):

        if self._context is None:
            self._context = {}
        res = super(PrepaidHoursApproval, self).fields_view_get(
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
        return res
