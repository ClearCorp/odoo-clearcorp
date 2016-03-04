from openerp import models, fields, api
from openerp.http import request as rqst
import uuid
import openerp.addons.bus.bus
import simplejson


class DesktopMessage(models.Model):
    _name = 'desktop.message'
    to_id = fields.Many2one('desktop.session')
    message = fields.Char(string='Message')

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
        print _uuid
        self.uuid = _uuid

    uuid = fields.Char(
        string='UUID', size=50, select=True, readonly=True,
        compute='_compute_uuid', store=True)
    message_ids = fields.One2many('desktop.message', 'to_id', string='Message')
    user_id = fields.Many2one('res.users', string='Session Users')
#   user_ids = fields.Many2many('res.users', string='Session Users', )

    @api.model
    def session_get(self, user_id):
        if user_id:
            session_obj = self.env['desktop.session'].browse([user_id])
            """if session_obj:
                session_id = session_obj._ids[0]
            else:"""
            user_id = self._uid
            session_id = self.sudo().create({'user_id': user_id})
            return simplejson.dumps(
                {
                    'id': session_id.id,
                    'uuid': session_id.uuid,
                    'user_id': user_id,
#                   'user_ids': [id for id in session_id.user_ids]
                })


class DesktopUser(models.Model):

    _inherit = 'res.users'

    desktop_notification_id = fields.One2many(
        'desktop.session', 'user_id', required=True)


class Controller(openerp.addons.bus.bus.Controller):
    def _pool(self, dbname, channels, last, options):
        registry, cr, uid, context = \
            rqst.registry, rqst.cr, rqst.session.uid, rqst.context
        channels.append((rqst.db, 'desktop.session', rqst.uid),)
        return super(Controller, self)._poll(dbname, channels, last, options)

    @openerp.http.route('/desktop_notification/init', type='json', auth=None)
    def init(self):
        pass

    @openerp.http.route('/desktop_notification/post', type='json', auth=None)
    def post(self, uuid, message):
        registry, uid = rqst.registry, rqst.session.uid
        message_id = registry['desktop.message'].sudo().post(uid, uuid, message)
        return message_id
