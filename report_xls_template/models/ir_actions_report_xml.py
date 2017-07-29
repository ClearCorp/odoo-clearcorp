# -*- coding: utf-8 -*-
# © 2014 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api

REPORT_TYPES = [
    ('qweb-xls', 'Office Open XML Spreadsheet (.xlsx)'),
    ('qweb-ods', 'Open Document Spreadsheet (.ods)')]


class ReportAction(models.Model):

    _inherit = 'ir.actions.report.xml'

    @api.model_cr
    def _lookup_report(self, name):
        """
        Look up a report definition.
        """
        self._cr.execute(
            'SELECT * FROM ir_act_report_xml WHERE report_name=%s',
            (name,))
        r = self._cr.dictfetchone()
        if r:
            # Check if the report type fits with xls or ods reports
            if r['report_type'] in ['qweb-xls', 'qweb-ods']:
                # Return tuple (report name, report_type, module name)
                return (r['report_name'],
                        r['report_type'],
                        'report_xls_template')
        return super(ReportAction, self)._lookup_report(name)

    @api.model
    def render_report(self, res_ids, name, data):
        """
        Look up a report definition and render the report for the provided IDs.
        """
        new_report = self._lookup_report(name)

        if isinstance(new_report, tuple):  # Check the type of object
            # Check if the module is report_xls_template
            if new_report[2] == 'report_xls_template':
                # Check report type
                if new_report[1] == 'qweb-xls':
                    return self.env['report'].get_xls(res_ids, new_report[0], data=data), 'xls'
                elif new_report[1] == 'qweb-ods':
                    return self.env['report'].get_ods(res_ids, new_report[0], data=data), 'xls'
        return super(ReportAction, self).render_report(res_ids, name, data)

    report_type = fields.Selection(selection_add=REPORT_TYPES)
