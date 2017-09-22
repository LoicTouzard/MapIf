#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: validator.py
#    date: 2017-09-22
# authors: paul.dautry, ...
# purpose:
#       Defines several functions used for user input validation. 
# license:
#    MapIF - Where are INSA de Lyon IF students right now ?
#    Copyright (C) 2017  Loic Touzard
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#===============================================================================
# IMPORTS
#===============================================================================
import re
import requests
import json
from src.utils import ini
from src.utils import logger
#===============================================================================
# GLOBALS
#===============================================================================
_VALIDATORS_ = {
    'email': re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'),
    'alphanum': re.compile('^\w+$'),
    'int': re.compile('^\d+$'),
    'double': re.compile('^\d+(\.\d+)?$'),
    'phone': re.compile('^(\+\d{2}(\s)?\d|\d{2})(\s)?(\d{2}(\s)?){4}$'),
    'year': re.compile('^\d{4}$'),
    'timestamp': re.compile('^\d{4}(-\d{2}){2}$')
}
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# validate
#   (In)Validates data based on its type using regular expressions
#-------------------------------------------------------------------------------
def validate(field, vtype=None):
    if vtype in _VALIDATORS_.keys():
        return True if _VALIDATORS_[vtype].match(str(field)) else False
    else:
        return False
#-------------------------------------------------------------------------------
# is_empty
#   Tests if a field is empty
#-------------------------------------------------------------------------------
def is_empty(field):
    return len(str(field).strip()) == 0
#-------------------------------------------------------------------------------
# check_captcha 
#   Google ReCaptcha validation process
#-------------------------------------------------------------------------------
def check_captcha(request):
    payload = {
        'secret': ini.config('RECAPTCHA','recaptcha_secret_key'),
        'response': request.form['g-recaptcha-response'],
        'remoteip': request.remote_addr
    }
    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', params=payload)
    data = json.loads(resp.text)
    if not data['success']:
        logger.log_trace("from validator: {0} may be a bot !".format(request.remote_addr))
    return data['success']
#===============================================================================
# TESTS 
#===============================================================================
def test():
    print('VALIDATOR - validate(john.doe@insa-lyon.fr, email) returned {0}'.format(validate('john.doe@insa-lyon.fr', 'email')))
    print('VALIDATOR - validate(john.doe@log, email) returned {0}'.format(validate('john.doe@log', 'email')))
    print('VALIDATOR - validate(doe@hotmail.fr, email) returned {0}'.format(validate('doe@hotmail.fr', 'email')))
    print('VALIDATOR - validate(john.doe@log, email) returned {0}'.format(validate('john.doe@log', 'email')))
    print('VALIDATOR - add tests here <!>')
