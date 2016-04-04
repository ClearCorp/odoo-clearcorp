# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, api, _
from openerp.exceptions import Warning
import re


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        if 'password' in vals:
            password = vals['password']
            self._validate_password(password)
        return super(ResUsers, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'password' in vals:
            password = vals['password']
            self._validate_password(password)
        return super(ResUsers, self).write(vals)

    def _validate_password(self, password):
        params = self._load_params()
        messages = []
        regex = ''
        if bool(params['password_security_validate']):
            length_password = int(params['password_security_length'])
            if length_password != 0:
                regex = (".{%s,}" % length_password)
                if not(re.search(regex, password)):
                    messages.append(_(
                        "Have at least %s characters long"
                        % length_password))
            if bool(params['password_security_include_letters']):
                if bool(params['password_security_include_uppercase']):
                    length_uppercase = \
                        int(params['password_security_uppercase_length'])
                    if length_uppercase != 0:
                        regex = ('.[A-Z]{%s,}' % length_uppercase)
                        if not (re.search(regex, password)):
                            messages.append(_(
                                """Have at least %s uppercase letters"""
                                % length_uppercase))
                if bool(params['password_security_include_lowercase']):
                    length_lowercase = \
                        int(params['password_security_lowercase_length'])
                    if length_lowercase != 0:
                        regex = ('.[a-z]{%s,}' % length_lowercase)
                        if not (re.search(regex, password)):
                            messages.append(_(
                                """Have at least %s lowercase letters"""
                                % length_lowercase))
            if bool(params['password_security_include_numbers']):
                length_numbers = \
                    int(params['password_security_numbers_length'])
                if length_numbers != 0:
                    regex = ('.[0-9]{%s,}' % length_numbers)
                    if not (re.search(regex, password)):
                        messages.append(_(
                            """Have at least %s numbers"""
                            % length_numbers))
            if bool(params['password_security_include_special']):
                length_special = \
                    int(params['password_security_special_length'])
                if length_special != 0:
                    regex = r'[!#$%&\'\*\+\-/=\?\^`\{\|\}~]{' +\
                        str(length_special) + ',}'
                    if not (re.search(regex, password)):
                        messages.append(_(
                            """Have at least %s special characters"""
                            % length_special))
        if len(messages) > 0:
            warning = _(
                "The password must satisfy the following criteria:\n\n")
            for message in messages:
                warning += "* " + message + "\n"
            raise Warning(warning)

    def _load_params(self):
        params = {'password_security_validate': '',
                  'password_security_length': '',
                  'password_security_include_letters': '',
                  'password_security_include_uppercase': '',
                  'password_security_uppercase_length': '',
                  'password_security_include_lowercase': '',
                  'password_security_lowercase_length': '',
                  'password_security_include_numbers': '',
                  'password_security_numbers_length': '',
                  'password_security_include_special': '',
                  'password_security_special_length': ''
                  }
        for param in params:
            params[param] = self._get_param_value(param)
        return params

    def _get_param_value(self, param):
        ir_config_parameter = self.env["ir.config_parameter"]
        domain = ir_config_parameter.get_param(param)
        return domain

    @api.model
    def signup(self, values, token=None):
        partner = self.env['res.partner']._signup_retrieve_partner(
            token, check_validity=False, raise_exception=False)
        try:
            return super(ResUsers, self).signup(values, token)
        except Warning as e:
            partner.write({'signup_token': token})
            raise Warning(e.message)
