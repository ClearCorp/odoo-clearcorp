# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    password_security_validate = fields.Boolean(
        string='Validate user password')
    password_security_length = fields.Integer(string='Length', default=1)
    password_security_include_letters = fields.Boolean(
        string='Include Letters')
    password_security_include_uppercase = fields.Boolean(
        string='Include uppercase letters')
    password_security_uppercase_length = fields.Integer(
        string='Length uppercase letters', default=1)
    password_security_include_lowercase = fields.Boolean(
        string='Include lowercase letters')
    password_security_lowercase_length = fields.Integer(
        string='Length lowercase letters', default=1)
    password_security_include_numbers = fields.Boolean(
        string='Include numbers')
    password_security_numbers_length = fields.Integer(
        string='Length numbers', default=1)
    password_security_include_special = fields.Boolean(
        string='Include special characters (@#$%+=-*)')
    password_security_special_length = fields.Integer(
        string='Length special characters', default=1)

    @api.multi
    def set_password_security_validate(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_validate",
                record.password_security_validate or '')

    @api.multi
    def get_default_password_security_validate(self):
        password_security_validate =\
            self.env["ir.config_parameter"].get_param(
                "password_security_validate", default=None)
        return {
            'password_security_validate': password_security_validate or False
            }

    @api.multi
    def set_password_security_length(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_length",
                record.password_security_length or '')

    @api.multi
    def get_default_password_security_length(self):
        password_security_length =\
            self.env["ir.config_parameter"].get_param(
                "password_security_length", default=None)
        return {
            'password_security_length': int(password_security_length) or False
            }

    @api.multi
    def set_password_security_include_letters(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_include_letters",
                record.password_security_include_letters or '')

    @api.multi
    def get_default_password_security_include_letters(self):
        password_security_include_letters =\
            self.env["ir.config_parameter"].get_param(
                "password_security_include_letters", default=None)
        return {
            'password_security_include_letters':
            password_security_include_letters or False
            }

    @api.multi
    def set_password_security_include_uppercase(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_include_uppercase",
                record.password_security_include_uppercase or '')

    @api.multi
    def get_default_password_security_include_uppercase(self):
        password_security_include_uppercase =\
            self.env["ir.config_parameter"].get_param(
                "password_security_include_uppercase", default=None)
        return {
            'password_security_include_uppercase':
            password_security_include_uppercase or False
            }

    @api.multi
    def set_password_security_uppercase_length(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_uppercase_length",
                record.password_security_uppercase_length or '')

    @api.multi
    def get_default_password_security_uppercase_length(self):
        password_security_uppercase_length =\
            self.env["ir.config_parameter"].get_param(
                "password_security_uppercase_length", default=None)
        return {
            'password_security_uppercase_length':
            int(password_security_uppercase_length) or False
            }

    @api.multi
    def set_password_security_include_lowercase(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_include_lowercase",
                record.password_security_include_lowercase or '')

    @api.multi
    def get_default_password_security_include_lowercase(self):
        password_security_include_lowercase =\
            self.env["ir.config_parameter"].get_param(
                "password_security_include_lowercase", default=None)
        return {
            'password_security_include_lowercase':
            password_security_include_lowercase or False
            }

    @api.multi
    def set_password_security_lowercase_length(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_lowercase_length",
                record.password_security_lowercase_length or '')

    @api.multi
    def get_default_password_security_lowercase_length(self):
        password_security_lowercase_length =\
            self.env["ir.config_parameter"].get_param(
                "password_security_lowercase_length", default=None)
        return {
            'password_security_lowercase_length':
            int(password_security_lowercase_length) or False
            }

    @api.multi
    def set_password_security_include_numbers(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_include_numbers",
                record.password_security_include_numbers or '')

    @api.multi
    def get_default_password_security_include_numbers(self):
        password_security_include_numbers =\
            self.env["ir.config_parameter"].get_param(
                "password_security_include_numbers", default=None)
        return {
            'password_security_include_numbers':
            password_security_include_numbers or False
            }

    @api.multi
    def set_password_security_numbers_length(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_numbers_length",
                record.password_security_numbers_length or '')

    @api.multi
    def get_default_password_security_numbers_length(self):
        password_security_numbers_length =\
            self.env["ir.config_parameter"].get_param(
                "password_security_numbers_length", default=None)
        return {
            'password_security_numbers_length':
            int(password_security_numbers_length) or False
            }

    @api.multi
    def set_password_security_include_special(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_include_special",
                record.password_security_include_special or '')

    @api.multi
    def get_default_password_security_include_special(self):
        password_security_include_special =\
            self.env["ir.config_parameter"].get_param(
                "password_security_include_special", default=None)
        return {
            'password_security_include_special':
            password_security_include_special or False
            }

    @api.multi
    def set_password_security_special_length(self):
        config_parameters = self.env["ir.config_parameter"]
        for record in self.browse(self._ids):
            config_parameters.set_param(
                "password_security_special_length",
                record.password_security_special_length or '')

    @api.multi
    def get_default_password_security_special_length(self):
        password_security_special_length =\
            self.env["ir.config_parameter"].get_param(
                "password_security_special_length", default=None)
        return {
            'password_security_special_length':
            int(password_security_special_length) or False
            }
