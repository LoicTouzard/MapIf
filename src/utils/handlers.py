# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                           IMPORTS
# ------------------------------------------------------------------------------------------

import time
from flask.ext.responses import json_response
from functools import wraps
from src.utils.response import Response
from src.utils import logger

# ------------------------------------------------------------------------------------------
#                                          DECORATOR
# ------------------------------------------------------------------------------------------

def internal_error_handler(err_code):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                timestamp = time.strftime('%d%m%H%M%S')
                logger.log_error('mapif.{0}() at {1} error: details below.'.format(f.__name__, timestamp), e)
                code = '{0}.{1}'.format(self.err_code, timestamp)
                return json_response(Response(has_error=True, code=code, content='').json(), status_code=500)
        return decorated_function
    return decorator