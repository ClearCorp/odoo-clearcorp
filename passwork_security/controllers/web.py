# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import http
from openerp.addons.web.controllers import main
from openerp.http import request


class Home(main.Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        print "\nlogin custom\n"
        request_obj = request
        res = super(Home, self).web_login(redirect, **kw)
        if res.qcontext:
            print "qcontext: ",  res.qcontext, request_obj
        print res
        return res
