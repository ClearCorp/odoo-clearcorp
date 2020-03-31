# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class website_config_settings(models.TransientModel):

    _inherit = 'website.config.settings'

    login_recaptcha_site_key = fields.Char(
        related='website_id.login_recaptcha_site_key',
        string='Login Google reCAPTCHA site Key')
    login_recaptcha_private_key = fields.Char(
        related='website_id.login_recaptcha_private_key',
        string='Login Google reCAPTCHA Private Key')
