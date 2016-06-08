#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                    IMPORTS & GLOBALS
# ------------------------------------------------------------------------------------------

import re
import requests
import json
from src.utils import ini
from src.utils import logger

_VALIDATORS_ = {
    'email': re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'),
    'alphanum': re.compile('^\w+$'),
    'int': re.compile('^\d+$'),
    'double': re.compile('^\d+(\.\d+)?$'),
    'phone': re.compile('^(\+\d{2}(\s)?\d|\d{2})(\s)?(\d{2}(\s)?){4}$'),
    'year': re.compile('^\d{4}$'),
    'timestamp': re.compile('^\d{4}(-\d{2}){2}$')
}

# ------------------------------------------------------------------------------------------
#                               EXTERN FUNCTIONS
# ------------------------------------------------------------------------------------------

def validate(field, vtype=None):
    """
        (In)Validates data based on its type using regular expressions
    """
    if vtype in _VALIDATORS_.keys():
        return True if _VALIDATORS_[vtype].match(str(field)) else False
    else:
        return False

def is_empty(field):
    """
        Tests if a field is empty
    """
    return len(str(field).strip()) == 0

def check_captcha(request):
    """
        Google ReCaptcha validation process
    """
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

# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

def test():
    """
        Module unit tests
    """
    print('VALIDATOR - validate(john.doe@insa-lyon.fr, email) returned {0}'.format(validate('john.doe@insa-lyon.fr', 'email')))
    print('VALIDATOR - validate(john.doe@log, email) returned {0}'.format(validate('john.doe@log', 'email')))
    print('VALIDATOR - validate(doe@hotmail.fr, email) returned {0}'.format(validate('doe@hotmail.fr', 'email')))
    print('VALIDATOR - validate(john.doe@log, email) returned {0}'.format(validate('john.doe@log', 'email')))
    print('VALIDATOR - add tests here <!>')
