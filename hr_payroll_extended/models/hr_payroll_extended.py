# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api
from datetime import datetime
from odoo.tools.translate import _


class Company(models.Model):

    _inherit = 'res.company'


    payslip_footer = fields.Text('Payslip footer')



class SalaryRule(models.Model):

    _inherit = 'hr.salary.rule'

    appears_on_report = fields.Boolean(
            'Appears on Report',
            help='Used to display the rule on reports', default=True)

class Job(models.Model):

    _inherit = 'hr.job'


    code = fields.Char('Code', size=128, required=False)



class PayslipRun(models.Model):

    _inherit = 'hr.payslip.run'

    schedule_pay = fields.Selection([
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('semi-annually', 'Semi-annually'),
            ('annually', 'Annually'),
            ('weekly', 'Weekly'),
            ('bi-weekly', 'Bi-weekly'),
            ('bi-monthly', 'Bi-monthly'),
            ], 'Scheduled Pay', index=True, readonly=True,
            states={'draft': [('readonly', False)]})


    def close_payslip_run(self):
        result = self.write({'state': 'close'})
        for batches in self:
            for payslip in batches.slip_ids:
                    if payslip.state == 'draft':
                        raise UserError(
                            _('Warning !'),
                            _('You did not confirm a payslip'))
                        break
        return result

    def confirm_payslips(self):
        for batches in self:
            for payslip in batches.slip_ids:
                    if payslip.state == 'draft':
                        payslip.compute_sheet()
                        payslip.process_sheet()
        return True

    def compute_payslips(self):
        for batches in self:
            for payslip in batches.slip_ids:
                if payslip.state == 'draft':
                    payslip.compute_sheet()
        return True


class Payslip(models.Model):

    _inherit = 'hr.payslip'

    name = fields.Char('Description', size=256, required=False,
            readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    def onchange_employee_id(self, date_from, date_to, employee_id=False, contract_id=False):
        res = super(Payslip, self).onchange_employee_id(date_from, date_to, employee_id=employee_id,
                                                        contract_id=contract_id)

        if (not employee_id) or (not date_from) or (not date_to):
            return res

        employee_obj = self.env['hr.employee']

        employee = employee_obj.browse(employee_id)

        if (not employee.contract_id):
            raise UserError(
                _('Warning !'),
                _('Contract not found for %s' % (employee.name,)))

        contract = employee.contract_id
        schedule_pay = ''
        if contract and contract.schedule_pay:
            # This is to translate the terms
            if contract.schedule_pay == 'weekly':
                schedule_pay = _('weekly')
            elif contract.schedule_pay == 'monthly':
                schedule_pay = _('monthly')

        # Format dates
        date_from_payslip = datetime.strptime(date_from, "%Y-%m-%d")
        date_from_payslip = date_from_payslip.strftime('%d-%m-%Y')
        date_to_payslip = datetime.strptime(date_to, "%Y-%m-%d")
        date_to_payslip = date_to_payslip.strftime('%d-%m-%Y')

        name = _('%s payroll of %s from %s to %s') % (
            schedule_pay, employee.name, date_from_payslip, date_to_payslip)
        name = name.upper()
        worked_days_line_list = []
        if res['value']['worked_days_line_ids']:
            day_lines = res['value']['worked_days_line_ids']
            # Check if there is an element with code HR
            has_hr = False
            for worked_days_line in day_lines:
                if worked_days_line['code'] == 'HR':
                    has_hr = True
            # Change lines where code == WORK100

            input_value = self.env.ref('hr_payroll_extended.data_input_value_1')
            for worked_days_line in day_lines:
                if worked_days_line['code'] == 'WORK100':
                    # Change it if there is no HN
                    if not has_hr:
                        worked_days_line['work_code'] = input_value.id
                        worked_days_line['code'] = input_value.code
                        worked_days_line['name'] = name
                    # Ignore it if there is another HN line
                    else:
                        continue
                worked_days_line_list.append(worked_days_line)

        res['value'].update({
                    'name': name,
                    'worked_days_line_ids': worked_days_line_list,
        })
        return res

    @api.model
    def get_worked_day_lines(self, contract_ids, date_from, date_to):
        res = []
        for contract in self.env['hr.contract'].browse(contract_ids):
            # Check if the contract uses fixed working hours
            if not contract.use_fixed_working_hours:
                continue
            attendances = {
                 'name': _("Worked Hours"),
                 'sequence': 1,
                 'work_code': contract.fixed_working_hours_code.id,
                 'code': contract.fixed_working_hours_code.code,
                 'number_of_days': contract.fixed_working_days,
                 'number_of_hours': contract.fixed_working_hours,
                 'contract_id': contract.id,
            }
            res += [attendances]
        res += super(Payslip, self).get_worked_day_lines(contract_ids, date_from, date_to)
        return res
