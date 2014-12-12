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
{
    'name': 'Currency Second Rate',
    'version': '1.0',
    #'author': 'ClearCorp',
    'author': 'ClearCorp',    
    'category': 'Generic Modules/Base',
    'description': """
    
IMPORT THE EXCHANGES FOR THE SECOND RATE.
==================================
    This module permits for each currency that have the web service 
    of BCCR, take the value of the second rate
    """,
    'depends': [
                "base",
                "currency_rate_update",
                ],
    'data': [
             'res_currency_secondrate.xml',
             ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
