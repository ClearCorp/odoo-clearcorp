from openerp import models, fields
import uuid
import openerp.addons.bus.bus
from openerp.http import request


class DesktopMessage(models.Model):
    _name = 'desktop.message'
    to_id = fields.Many2one('desktop.session')


class DesktopSession(models.Model):
    _name = 'desktop.session'
    _order = 'id desc'
    _rec_name = 'uuid'

    uuid = fields.Char(
        string='UUID', size=50, select=True,
        compute=lambda *args: '%s' % uuid.uuid4(), store=True)
    message_ids = fields.One2many('desktop.message', 'to_id', string='Message')
    user_ids = fields.Many2many(
        'res.user', 'desktop_session_res_users_rel', 'session_id', 'user_id',
        'Session Users')


class Controller(openerp.addons.bus.bus.Controller):
    def _pool(self, dbname, channels, last, options):
        registry, cr, uid, context =\
            request.registry, request.cr, request.session.uid, request.context
        channels.append((request.db, 'desktop.session', request.uid),)
        return super(Controller, self)._poll(dbname, channels, last, options)
