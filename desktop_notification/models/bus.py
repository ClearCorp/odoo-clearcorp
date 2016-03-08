# -*- coding: utf-8 -*-
# © <2016> ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, api
import simplejson


class ImBus(models.Model):

    _inherit = 'bus.bus'

    def sendmany(self, cr, uid, notifications):
        print "\n Metodo heredado \n", notifications
        super(ImBus, self).sendmany(cr, uid, notifications)


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
        message_id = super(MailMessage, self).create(vals)
        print "\n create heredado \n", vals
        bus_obj = self.env['bus.bus']
        
        message_obj = self.env['mail.message'].browse([message_id])
        
        desktop_session = self.env['desktop.session'].sudo().search([('user_id', '=', self._uid)])
        print desktop_session
        for session in desktop_session:
            notification =\
                [[session.uuid,
                  {
                      'create_date': '2016-03-01 19:18:55',
                      'to_id': (session.user_id.id, session.uuid),
                      'message': vals['body'],
                      'type': u'notification',
                      'id': message_id,
                      'from_id': (session.user_id.id, session.user_id.name)
                   }
                  ]] 
            bus_obj.sendmany(notification)
            desktop_notification_obj = self.env['desktop.message']
            desktop_notification_obj.sudo().create({'to_id': session.id, 'message': vals['body']})
        return message_id
