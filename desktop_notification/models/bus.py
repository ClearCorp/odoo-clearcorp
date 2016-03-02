# -*- coding: utf-8 -*-
# © <2016> ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, api


class ImBus(models.Model):

    _inherit = 'bus.bus'

    def sendmany(self, cr, uid, notifications):
        print "\n Metodo heredado \n", notifications
        notification =\
            [[(u'cc_notificaciones', 'im_chat.session', 5),
              {
                  'create_date': '2016-03-01 19:18:55',
                  'to_id': (2, u'59f32ef1-1557-464d-a73f-20d2b85d9f1f'),
                  'message': '1,2,3,4,5,6,7,8,9',
                  'type': u'message',
                  'id': 155,
                  'from_id': (5, u'lesmed')
               }
              ]] 
        super(ImBus, self).sendmany(cr, uid, notifications)


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        print "\n create heredado \n"
        bus_obj = self.env['bus.bus']
        bus_obj.sendone("59f32ef1-1557-464d-a73f-20d2b85d9f1f",
            "Mensaje de prueba")
        return models.Model.create(self, vals)
