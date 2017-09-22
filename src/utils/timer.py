#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: timer.py
#    date: 2017-09-22
# authors: paul.dautry, ...
# purpose:
#       Defines useful time-related functions.
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
#===============================================================================
# FUNCTIONS 
#===============================================================================
#-------------------------------------------------------------------------------
# get_time
#   Returns a timestamp in UNIX style
#-------------------------------------------------------------------------------
def get_time():
    return time.time()
#-------------------------------------------------------------------------------
# get_date
#   Returns a timestamp formated in a string
#-------------------------------------------------------------------------------
def get_date():
    return str(time.strftime("(%d-%m-%Y %H:%M:%S)"))
#-------------------------------------------------------------------------------
# get_diff
#   Computes a time delta
#-------------------------------------------------------------------------------
def get_diff(start_time, end_time):
    return end_time - start_time
#===============================================================================
# TESTS 
#===============================================================================------------
def test():
    print('TIMER TEST - get_time() returned {0}'.format(get_time()))
    print('TIMER TEST - get_date() returned {0}'.format(get_date()))
    print('TIMER TEST - get_diff(10, 35) returned {0}'.format(get_diff(10, 35)))