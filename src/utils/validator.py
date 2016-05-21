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
    'email': re.compile('^[\w\.\_\-]+@[\w\.\_\-]+\.\w{2,3}$'),
    'alphanum': re.compile('^\w+$'),
    'num': re.compile('^\d+$'),
    'price': re.compile('^\d+(\.\d+)$'),
    'phone': re.compile('^(\+\d{2}(\s)?\d|\d{2})(\s)?(\d{2}(\s)?){4}$'),
    'year': re.compile('^\d{4}$')
}

# ------------------------------------------------------------------------------------------
#                               EXTERN FUNCTIONS
# ------------------------------------------------------------------------------------------

def validate(field, vtype=None):
    if vtype in _VALIDATORS_.keys():
        return _VALIDATORS_[vtype].match(field)
    else:
        return False

def is_empty(field):
    return len(field.strip()) == 0

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

# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

if __name__ == '__main__':
    logger.mprint('TESTS NOT IMPLEMENTED')
