# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import http
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

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        session = request.session
        response = super(Home, self).web_login(redirect, **kw)
        secure_cookie = self._load_cookie('session_data')
        if 'error' in response.qcontext:
            print "secure cookie: ", secure_cookie
            if 'login_attemps' in secure_cookie:
                login_attemps = int(secure_cookie['login_attemps'])
                secure_cookie['login_attemps'] = str(login_attemps + 1)
            else:
                secure_cookie['login_attemps'] = str(0)
                print secure_cookie
            if hasattr(response, 'set_cookie'):
                secure_cookie.save_cookie(response, 'session_data',
                                          httponly=True, max_age=60*3)
        else:
            secure_cookie['login_attemps'] = str(0)
            print secure_cookie
        print "qcontext: ", response.qcontext, session
        return response
