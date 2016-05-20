
import re
import requests
import json
from src.utils import ini

VALIDATORS = {
    'email': re.compile('^[\w\.\_\-]+@[\w\.\_\-]+\.\w{2,3}$'),
    'alphanum': re.compile('^\w+$'),
    'num': re.compile('^\d+$'),
    'price': re.compile('^\d+(\.\d+)$'),
    'phone': re.compile('^(\+\d{2}(\s)?\d|\d{2})(\s)?(\d{2}(\s)?){4}$'),
    'year': re.compile('^\d{4}$')
}

def validate(field, vtype=None):
    if vtype in VALIDATORS.keys():
        return VALIDATORS[vtype].match(field)
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
    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=json.dumps(payload))
    print(resp.text)
    data = json.loads(resp.text)
    return data['success']

