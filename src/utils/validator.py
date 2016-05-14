
import re

VALIDATORS = {
    'email': re.compile('^[\w\.\_]+@[\w\_\.]+\.\w{2,3}$'),
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

