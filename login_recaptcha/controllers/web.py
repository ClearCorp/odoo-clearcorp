# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import http, _
from openerp.addons.web.controllers import main
from openerp.http import request
from werkzeug.contrib.securecookie import SecureCookie
import json

SECRET_KEY = '\x9a\x832I\x80\\\x83\x88\x1c\xc0\xd4u)\x8f\xed\xbb\xdbK\x8e\xb6'


class JSONSecureCookie(SecureCookie):
    serialization_method = json


class Home(main.Home):

    def _load_cookie(self, name):
        _data = request.httprequest.cookies.get('session_data')
        return JSONSecureCookie.load_cookie(request.httprequest, key=name,
                                            secret_key=SECRET_KEY)

    def _action_reset_password(self, login):
        user = request.website.env['res.users'].sudo().search(
            [('login', '=', login)])
        if user:
            user.action_reset_password()
            return True
        return False

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        cookie = self._load_cookie('session_data')
        login_attemps = 0
        if 'login_attemps' in cookie:
            login_attemps = int(cookie['login_attemps'])
        if 'g-recaptcha-response' in kw and\
                not request.website.is_captcha_valid(
                    kw['g-recaptcha-response']):
            response = super(Home, self).web_login(redirect, **kw)
            if login_attemps >= 8:
                response.qcontext.update({
                    'error': _(
                        """The amount of login attemps have exceeded the
                        restriction.
                        A password reset link has been sent to the user's
                        email.
                        """)
                    }
                )
            else:
                response.qcontext.update({
                    'error': _("Wrong Captcha")
                    }
                )
            return request.render('web.login', response.qcontext)
        else:
            response = super(Home, self).web_login(redirect, **kw)
            secure_cookie = self._load_cookie('session_data')
            if 'error' in response.qcontext:
                if 'login_attemps' in secure_cookie:
                    login_attemps = int(secure_cookie['login_attemps'])
                    secure_cookie['login_attemps'] = str(login_attemps + 1)
                else:
                    secure_cookie['login_attemps'] = str(1)
            elif 'login_attemps' in secure_cookie:
                pass
            else:
                secure_cookie['login_attemps'] = str(0)
            response.qcontext.update(
                {'login_attemps': int(secure_cookie['login_attemps'])})
            if hasattr(response, 'set_cookie'):
                secure_cookie.save_cookie(response, 'session_data',
                                          httponly=True, max_age=60*3)
            return response
