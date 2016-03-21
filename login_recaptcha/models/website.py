# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class Website(models.Model):

    _inherit = 'website'

    login_recaptcha_site_key = fields.Char(
        string='Login Google reCAPTCHA site Key',
        default='6Lf8ghoTAAAAANdd_v5uNvdKa0qWYlOJTdr0TOIy')
    login_recaptcha_private_key = fields.Char(
        string='Login Google reCAPTCHA Private Key',
        default='6Lf8ghoTAAAAAEyfOnnXXg0VAIpeCbvESlS3mH3b')
