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

from osv import osv, fields

class AccountAccount(osv.osv):
    _inherit = "account.account"
    
    _columns = {
        'reconcile_forced_partner': fields.boolean('Allow reconcile with different partners'),
    }

class AccountMoveReconcile(osv.osv):
    _inherit = 'account.move.reconcile'

    def _check_same_partner(self, cr, uid, ids, context=None):
        for reconcile in self.browse(cr, uid, ids, context=context):
            move_lines = []
            if reconcile.line_id:
                first_account = reconcile.line_id[0].account_id.id
                move_lines = reconcile.line_id
            elif reconcile.line_partial_ids:
                first_account = reconcile.line_partial_ids[0].account_id.id
                move_lines = reconcile.line_partial_ids
            if not any([(line.account_id.reconcile_forced_partner) for line in move_lines]):
                return super(AccountMoveReconcile, self)._check_same_partner(cr, uid, ids, context=context)
        return True
    
    _constraints = [
        (_check_same_partner, 'You can only reconcile journal items with the same partner.', ['line_id']),
    ]
    












