#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: request.py
#    date: 2017-09-23
#  author: paul.dautry
# purpose:
#   Interface to perform web requests relying on requests module with failsafe 
#   protections. 
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
import requests
from core.utils import logger
#===============================================================================
# GLOBALS
#===============================================================================
DFLT_TIMEOUT=2 # 2 seconds of default timeout
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# get
#-------------------------------------------------------------------------------
def get(url, params, timeout=DFLT_TIMEOUT):
    try:
        return requests.get(url, params=params, timeout=timeout)
    except Exception as e:
        logger.log_error("request.get(): failed.", e)
    return None
#-------------------------------------------------------------------------------
# post
#-------------------------------------------------------------------------------
def post(url, data, timeout=DFLT_TIMEOUT):
    try:
        return requests.post(url, data=data, timeout=timeout)
    except Exception as e:
        logger.log_error("request.post(): failed.", e)
    return None
#===============================================================================
# TESTS
#===============================================================================
def test():
    print('REQUEST - TESTS NOT IMPLEMENTED')
