# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by CLEARCORP S.A.
#    Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv

class accountSalereportWizard(osv.osv_memory):
    _name = "invoicing.report.wiz"
    _inherit = 'account.report.wiz'
    _description = "Account Invoicing Report Wizard"

    _columns = {
        'date_from': fields.date("Start Date"),
        'date_to': fields.date("End Date"),
        'account_tax_ids': fields.many2many('account.tax', string='Taxes'),
    }
    
    def _build_contexts(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        result = {}
        
        result['date_from'] = 'date_from' in data['form'] and data['form']['date_from'] or False
        result['date_to'] = 'date_to' in data['form'] and data['form']['date_to'] or False
        
        #m2m, m2o fields
        result['account_tax_ids'] = 'account_tax_ids' in data['form'] and data['form']['account_tax_ids'] or False
        
        return result
    
    def _print_report(self, cr, uid, ids, data, context=None):
        mimetype = self.pool.get('report.mimetypes')
        report_obj = self.pool.get('ir.actions.report.xml')
        report_name = ''
      
        context = context or {}
            
        #=======================================================================
        # onchange_in_format method changes variable out_format depending of 
        # which in_format is choose. 
        # If out_format is pdf -> call record in odt format and if it's choose
        # ods or xls -> call record in ods format.
        # ods and xls format are editable format, because they are arranged 
        # to be changed by user and, for example, user can check and change info.    
        #=======================================================================
       
        #=======================================================================
        # If mimetype is PDF -> out_format = PDF (search odt record)
        # If mimetype is xls or ods -> search ods record. 
        # If record doesn't exist, return a error.
        #=======================================================================
        
        #=======================================================================
        # Create two differents records for each format, depends of the out_format
        # selected, choose one of this records
        #=======================================================================
        
        #1. Find out_format selected
        out_format_obj = mimetype.browse(cr, uid, [int(data['form']['out_format'])], context)[0]

        #2. Check out_format and set report_name for each format
        if out_format_obj.code == 'oo-pdf':
            report_name = 'account_invoicing_report_odt' 
           
        elif out_format_obj.code == 'oo-xls' or out_format_obj.code == 'oo-ods': 
            report_name = 'account_invoicing_report_ods'
        
        # If there not exist name, it's because not exist a record for this format   
        if report_name == '':
            raise osv.except_osv(_('Error !'), _('There is no template defined for the selected format. Check if aeroo report exist.'))
                
        else:
            #Search record that match with the name, and get some extra information
            report_xml_id = report_obj.search(cr, uid, [('report_name','=', report_name)],context=context)
            report_xml = report_obj.browse(cr, uid, report_xml_id, context=context)[0]
            data.update({'model': report_xml.model, 'report_type':'aeroo', 'id': report_xml.id})
            
            #Write out_format choosed in wizard
            report_xml.write({'out_format': out_format_obj.id}, context=context)
            
            data['ids'] = []
            
            return {
                'type': 'ir.actions.report.xml',
                'report_name': report_name,
                'datas': data,
                'context':context
            }
            
    def check_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        
        data = {}
        data['form'] = self.read(cr, uid, ids, ['date_from','date_to','type','account_tax_ids','out_format'], context=context)[0]
        #Extract ids for m2o and m2m fields
        for field in ['account_tax_ids']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        
        #Check if the fields exist, otherwise put false in the field.
        used_context = self._build_contexts(cr, uid, ids, data, context=context)
        data['form']['used_context'] = used_context
        
        return self._print_report(cr, uid, ids, data, context=context)
    
        
