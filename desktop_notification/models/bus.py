# -*- coding: utf-8 -*-
# © <2016> ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, api


class ImBus(models.Model):

    _inherit = 'bus.bus'

    def sendmany(self, cr, uid, notifications):
        print "\n Metodo heredado \n", notifications
        super(ImBus, self).sendmany(cr, uid, notifications)


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        print "\n create heredado \n", vals
        bus_obj = self.env['bus.bus']
        notification =\
            [[(u'cc_notificaciones', 'im_chat.session', 5),
              {
                  'create_date': '2016-03-01 19:18:55',
                  'to_id': (2, u'59f32ef1-1557-464d-a73f-20d2b85d9f1f'),
                  'message': vals['body'],
                  'type': u'message',
                  'id': 155,
                  'from_id': (5, u'lesmed')
               }
              ]] 
        bus_obj.sendmany(notification)
        desktop_notification_obj = self.env['desktop.message']
        desktop_notification_obj.sudo().create({'to_id': 5, 'message': vals['body']})
        return models.Model.create(self, vals)
