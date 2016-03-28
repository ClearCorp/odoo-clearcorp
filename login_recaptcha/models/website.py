# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models
import json
import requests


class Website(models.Model):

    _inherit = 'website'

    login_recaptcha_site_key = fields.Char(
        string='Login Google reCAPTCHA site Key',
        default='6Lf8ghoTAAAAANdd_v5uNvdKa0qWYlOJTdr0TOIy')
    login_recaptcha_private_key = fields.Char(
        string='Login Google reCAPTCHA Private Key',
        default='6Lf8ghoTAAAAAEyfOnnXXg0VAIpeCbvESlS3mH3b')

    def is_captcha_valid(self, response):
        for website in self.browse(self._ids):
            get_res = {'secret': website.login_recaptcha_private_key,
                       'response': response}
            try:
                response = requests.get(
                    'https://www.google.com/recaptcha/api/siteverify',
                    params=get_res)
            except Exception, e:
                raise models.except_orm(('Invalid Data!'), ("%s.") % (e))
            res_con = json.loads(response.content)
            if 'success' in res_con and res_con['success']:
                return True
        return False
