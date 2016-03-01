# -*- coding: utf-8 -*-
# © <2016> ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, api


class ImBus(models.Model):

    _inherit = 'bus.bus'

    @api.model
    def sendmany(self, notifications):
        print "\n Metodo heredado \n"
        super(ImBus, self).sendmany(self._cr, self._uid, notifications)
