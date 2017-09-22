#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: response.py
#    date: 2017-09-22
# authors: paul.dautry, ...
# purpose:
#       Defines response class which represents a standardized API response 
#       format.
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
import json
from src.utils import logger
#===============================================================================
# CLASSES 
#===============================================================================
#-------------------------------------------------------------------------------
# Response
#-------------------------------------------------------------------------------
class Response:
    def __init__(self, has_error = True, content = {}, code=None):
        self.has_error = has_error
        self.content = content
        self.code = code
    #---------------------------------------------------------------------------
    # json
    #---------------------------------------------------------------------------
    def json(self):
        return {
            'has_error': self.has_error, 
            'content': self.content, 
            'code': self.code
        }
#===============================================================================
# TESTS
#===============================================================================
def test():
    out = 'NEGATIVE RESPONSE TEST\n'+json.dumps(Response(True, 'an error occured !').json(), indent=4)
    print(out)
    out = 'POSITIVE RESPONSE TEST\n'+json.dumps(Response(False, 'everything is OK.').json(), indent=4)
    print(out)
    