# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from Tkconstants import CASCADE
import uuid
import simplejson


class DesktopMessage(models.Model):
    _name = 'desktop.message'
    to_id = fields.Many2one('desktop.session', ondelete=CASCADE)
    message = fields.Char(string='Message', ondelete=CASCADE)

    def post(self, uid, uuid, message):
        message_id = False
        session_obj = self.env['desktop.message']
        sessions = session_obj.search([('uuid', '=', uuid)])
        notifications = []
        for session in sessions:
            vals = {
                'to_id': session.id,
                'message': message
            }
            message_id = self.create(vals)
            data = self.read(['to_id', 'message'])
            notifications.append([message_id, data])
            self.env['bus.bus'].sendmany(notifications)
        return message_id


class DesktopSession(models.Model):
    _name = 'desktop.session'
    _order = 'id desc'
    _rec_name = 'uuid'

    @api.one
    @api.depends("user_id")
    def _compute_uuid(self):
        _uuid = uuid.uuid4()
        self.uuid = _uuid

    uuid = fields.Char(
        string='UUID', size=50, select=True, readonly=True,
        compute='_compute_uuid', store=True)
    message_ids = fields.One2many('desktop.message', 'to_id', string='Message',
                                  ondelete=CASCADE)
    user_id = fields.Many2one('res.users', string='Session Users',
                              ondelete=CASCADE)

    @api.model
    def session_get(self, user_id):
        if user_id:
            user_id = self._uid
            session_id = self.sudo().search([('user_id', '=', user_id)],
                                            limit=1)
            if session_id:
                return simplejson.dumps(
                    {
                        'id': session_id.id,
                        'uuid': session_id.uuid,
                        'user_id': user_id,
                    })
            else:
                session_id = self.sudo().create({'user_id': user_id})
                return simplejson.dumps(
                    {
                        'id': session_id.id,
                        'uuid': session_id.uuid,
                        'user_id': user_id,
                    })


class DesktopUser(models.Model):

    _inherit = 'res.users'

    desktop_notification_id = fields.One2many(
        'desktop.session', 'user_id', required=True)
