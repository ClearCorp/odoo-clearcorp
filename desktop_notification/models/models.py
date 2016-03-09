# -*- coding: utf-8 -*-
# © <2016> ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, api


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
        message_id = super(MailMessage, self).create(vals)
        bus_obj = self.env['bus.bus']
        model = self.env['ir.model'].sudo().search(
            [('model', '=', message_id.model)], limit=1)
        for partner in message_id.notified_partner_ids:
            for user in partner.user_ids:
                desktop_session = self.env['desktop.session'].sudo().search(
                    [('user_id', '=', user.id)])
                for session in desktop_session:
                    notification = [[
                        session.uuid,
                        {
                            'create_date': '2016-03-01 19:18:55',
                            'to_id': (session.user_id.id, session.uuid),
                            'message': message_id.body,
                            'model': model.name,
                            'record_name': message_id.record_name,
                            'type': u'notification',
                            'id': message_id.id,
                            'from_id': (message_id.author_id.id,
                                        message_id.author_id.name)
                        }]]
                    bus_obj.sendmany(notification)
                    desktop_notification_obj = self.env['desktop.message']
                    desktop_notification_obj.sudo().create(
                        {'to_id': session.id, 'message': message_id.body})
        return message_id
