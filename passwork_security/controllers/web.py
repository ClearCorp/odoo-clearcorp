# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import http
from openerp.addons.web.controllers import main
from openerp.http import request
from werkzeug.utils import cached_property
from werkzeug.wrappers import BaseRequest
from werkzeug.contrib.securecookie import SecureCookie
import openerp
import os

SECRET_KEY = "23dfsDSghaSAgJUUYjgbnMiopgs"


class Home(main.Home):

    def _load_cookie(self, name):
        _data = request.httprequest.cookies.get('session_data')
        return SecureCookie.load_cookie(request.httprequest, key=name
                                        , secret_key=SECRET_KEY)

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        print "\nlogin custom\n"
        session = request.session
        response = super(Home, self).web_login(redirect, **kw)
        secure_cookie = self._load_cookie('session_data')
        login_attemps = int(secure_cookie['login_attemps'])
        secure_cookie['login_attemps'] = str(login_attemps + 1)
        if secure_cookie.should_save:
            print secure_cookie
        else:
            secure_cookie['login_attemps'] = str(0)
            print secure_cookie
            #ession_data['login_attemps'] = 0
        if hasattr(response, 'set_cookie'):
            secure_cookie.save_cookie(response, 'session_data', httponly=True)
        print "qcontext: ", response.qcontext, session
        print response
        return response
