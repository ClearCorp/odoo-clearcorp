# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class SalaryRule(models.Model):

    _RULE_TYPES = [
        ('partner', 'Partner'),
        ('employee', 'Employee'),
    ]

    _inherit = 'hr.salary.rule'
    rule_type_credit = fields.Selection(
        _RULE_TYPES, string='Credit Rule Type', default='employee'),
    rule_type_debit = fields.Selection(
        _RULE_TYPES, string='Debit Rule Type', default='employee'),
    res_partner_credit = fields.Many2one(
        'res.partner', string='Credit Partner'),
    res_partner_debit = fields.Many2one(
        'res.partner', string='Debit Partner'),


class PaySlip(models.Model):

    _inherit = 'hr.payslip'

    def process_sheet(self, cr, uid, ids, context=None):
        res = super(PaySlip, self).process_sheet(cr, uid, ids, context=context)
        for payslip in self.browse(cr, uid, ids, context=context):
            for line in payslip.line_ids:
                if line.salary_rule_id:
                    # Check is salary rule has debit
                    if line.salary_rule_id.account_debit:
                        # Check if rule has rule_type_debit
                        if line.salary_rule_id.rule_type_debit:
                            move_line_obj = self.pool.get('account.move.line')
                            # Check the rule_type if partner
                            if line.salary_rule_id.rule_type_debit == 'partner':
                                move_line_ids = move_line_obj.search(cr, uid,
                                [('move_id','=',payslip.move_id.id), ('debit','=',line.total),
                                 ('account_id','=',line.salary_rule_id.account_debit.id)], context=context)
                                if move_line_ids:
                                    move_line_obj.write(cr, uid, move_line_ids[0],
                                    {'partner_id': line.salary_rule_id.res_partner_debit.id}, context=context)
                            # Rule type is employee
                            else:
                                move_line_ids = move_line_obj.search(cr, uid,
                                [('move_id','=',payslip.move_id.id), ('debit','=',line.total),
                                 ('account_id','=',line.salary_rule_id.account_debit.id)], context=context)
                                if move_line_ids:
                                    move_line_obj.write(cr, uid, move_line_ids[0],
                                    {'partner_id': payslip.employee_id.address_home_id.id}, context=context)
                    # Credit check if salary rule has credit
                    if line.salary_rule_id.account_credit:
                        # Check if rule has rule_type credit
                        if line.salary_rule_id.rule_type_credit:
                            move_line_obj = self.pool.get('account.move.line')
                            # Check if rule_type is partner
                            if line.salary_rule_id.rule_type_credit == 'partner':
                                move_line_ids = move_line_obj.search(cr, uid,
                                    [('move_id','=',payslip.move_id.id), ('credit','=',line.total),
                                     ('account_id','=',line.salary_rule_id.account_credit.id)], context=context)
                                if move_line_ids:
                                    move_line_obj.write(cr, uid, move_line_ids[0],
                                    {'partner_id': line.salary_rule_id.res_partner_credit.id}, context=context)
                            # Rule type is employee
                            else:
                                move_line_ids = move_line_obj.search(cr, uid,
                                    [('move_id','=',payslip.move_id.id), ('credit','=',line.total),
                                     ('account_id','=',line.salary_rule_id.account_credit.id)], context=context)
                                if move_line_ids:
                                    move_line_obj.write(cr, uid, move_line_ids[0],
                                    {'partner_id': payslip.employee_id.address_home_id.id}, context=context)
        return res
