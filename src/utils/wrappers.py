# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                           IMPORTS
# ------------------------------------------------------------------------------------------

import time
from flask.ext.responses import json_response
from flask import session
from functools import wraps
from src.utils.response import Response
from src.utils import logger

# ------------------------------------------------------------------------------------------
#                                          DECORATOR
# ------------------------------------------------------------------------------------------

def internal_error_handler(err_code):
    def wrapper(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                timestamp = time.strftime('%d%m%H%M%S')
                logger.log_error('mapif.{0}() at {1} error: details below.'.format(f.__name__, timestamp), e)
                code = '{0}.{1}'.format(err_code, timestamp)
                return json_response(Response(has_error=True, code=code, content='').json(), status_code=500)
        return wrapped_f
    return wrapper


def require_connected():
    def wrapper(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            if not session.get('user', None):
                return json_response(Response(True, "Opération interdite vous n'êtes pas connecté !").json(), status_code=403)
            else:
                return f(*args, **kwargs)
        return wrapped_f
    return wrapper

def require_disconnected():
    def wrapper(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            if session.get('user', None):
                return json_response(Response(True, "Opération interdite vous n'êtes pas déconnecté !").json(), status_code=403)
            else:
                return f(*args, **kwargs)
        return wrapped_f
    return wrapper