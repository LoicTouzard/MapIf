#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: wrappers.py
#    date: 2017-09-22
# authors: paul.dautry, ... 
# purpose:
#       Useful wrappers for Flask application.
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
import time
import traceback
from flask_responses import json_response
from flask import session
from functools import wraps
from core.utils.response import Response
from core.utils import logger
from core.utils import notification
#===============================================================================
# DECORATORS
#===============================================================================
#-------------------------------------------------------------------------------
# internal_error_handler
#-------------------------------------------------------------------------------
def internal_error_handler(err_code):
    def wrapper(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                timestamp = time.strftime('%d%m%H%M%S')
                desc = '`mapif.{0}()` at `{1}` error: details below.'.format(
                    f.__name__, timestamp
                )
                logger.log_error(desc, e)
                code = '{0}.{1}'.format(err_code, timestamp)
                value = """internal error code: `{0}`
function: {1}
```
{2}```
""".format(code, desc, traceback.format_exc())
                notification.notify_err(value)
                resp = Response(has_error=True, code=code, content='')
                return json_response(resp.json(), status_code=500)
        return wrapped_f
    return wrapper
#-------------------------------------------------------------------------------
# require_connected
#-------------------------------------------------------------------------------
def require_connected():
    def wrapper(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            if not session.get('user', None):
                resp = Response(True, "Opération interdite vous n'êtes pas connecté !")
                return json_response(resp.json(), status_code=403)
            else:
                return f(*args, **kwargs)
        return wrapped_f
    return wrapper
#-------------------------------------------------------------------------------
# require_disconnected
#-------------------------------------------------------------------------------
def require_disconnected():
    def wrapper(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            if session.get('user', None):
                resp = Response(True, "Opération interdite vous n'êtes pas déconnecté !")
                return json_response(resp.json(), status_code=403)
            else:
                return f(*args, **kwargs)
        return wrapped_f
    return wrapper
