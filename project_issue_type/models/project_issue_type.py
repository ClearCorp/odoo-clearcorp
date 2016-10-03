# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class TicketInvoiceTypeName (models.Model):
    _name = 'ticket.invoice.type.name'

    name = fields.Char('Name', required='True')
    ticket_type = fields.Selection(
        [('change_request', 'Change Request'),
         ('service_request', 'Service Request'),
         ('issue', 'Issue'), ('problem', 'Problem')],
        string='Issue Type', default='issue', required=True)


class TicketInvoiceType (models.Model):
    _name = 'ticket.invoice.type'
    
    name = fields.Many2one('ticket.invoice.type.name', required='True')
    warranty = fields.Boolean('Warranty?')
    # This points to the client's Subscription (contract)
    contract_type_id = fields.Many2one('sale.subscription')


class ProjectIssue(models.Model):
    _inherit = 'project.issue'
    
    @api.one
    @api.depends("project_id")
    def _compute_invoice_ticket(self):
        if self.project_id:
            for ticket_kind in self.project_id.\
                    analytic_account_id.ticket_invoice_type_ids:
                if ticket_kind.name == self.issue_type.name:
                    if ticket_kind.warranty:
                        self.invoiced = 'warranty'
                        return False
                    else:
                        self.invoiced = 'invoice'
                        return True

    issue_type = fields.Many2one('ticket.invoice.type', string='Type')
    invoiced = fields.Selection(
        [('invoice', 'Invoice'),
         ('warranty', 'Warranty'),
         ('2beinvoice', 'To be Invoiced'),
         ('invoiced', 'Invoiced')],
        string="Invoice", help="It's an invoiced task",
        compute='_compute_invoice_ticket', store=True)


class AccountAnalitic(models.Model):

    _inherit = 'account.analytic.account'
    
    ticket_invoice_type_ids = fields.One2many('ticket.invoice.type',
                                              'contract_type_id',
                                              string='Ticket Type')
