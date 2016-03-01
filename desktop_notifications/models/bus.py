# -*- coding: utf-8 -*-
# © <2016> ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models


class ImBus(models.Model):

    _inherit = 'bus.bus'

    def sendmany(self, cr, uid, notifications):
        print "\n Metodo heredado \n"
        super(ImBus, self).sendmany(cr, uid, notifications)
