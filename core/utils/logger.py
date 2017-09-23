#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: logger.py
#    date: 2017-09-22
# authors: paul.dautry, ...
# purpose:
#       Logging module.   
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
import os
import traceback
from core.utils import timer
from core.utils import ini
#===============================================================================
# GLOBALS
#===============================================================================
_LOGS_ = None
_LOG_PERF_ = None
_LOG_DIR_ = None
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# _create_log
#       creates a log file if inexistant 
#-------------------------------------------------------------------------------
def _create_log(logfile):
    if _LOG_DIR_:
        if not os.path.exists(_LOG_DIR_):
            os.makedirs(_LOG_DIR_)
        with open(_LOG_DIR_+logfile, 'w', encoding='utf-8') as f:
            f.write("""
#===============================================================================
# MapIf log file: {0}
# Created at: {1}
#===============================================================================

""".format(logfile, timer.get_date()))
#-------------------------------------------------------------------------------
# _log
#   Add a line to the log
# TODO : this call might have a very bad impact on mapif performance... 
#        => opening log each time you log a line is bad...
#       change from (open,write,close) to (write,flush)
#-------------------------------------------------------------------------------
def _log(logfile, content):
    if _LOG_DIR_:
        with open(_LOG_DIR_+logfile, 'a', encoding='utf-8') as f:
            f.write("{0} - {1}\n".format(timer.get_date(), content))
#-------------------------------------------------------------------------------
# log_perf
#   Logs performance of an operation in perf log
# TODO : use a decorator instead, it will be more developer friendly that way.
#-------------------------------------------------------------------------------
def log_perf(start_time, end_time, params):
    if _LOG_PERF_:
        delta = timer.get_diff(start_time, end_time)
        _log("execution time = {0} sec {1}".format(str(delta), params))
#-------------------------------------------------------------------------------
# log_error
#    Logs error in errors' log
#-------------------------------------------------------------------------------
def log_error(msg=None, ex=None):
    if _LOGS_:
        if msg:
            _log(_LOGS_['stderr'], msg)
        if ex:
            _log(_LOGS_['stderr'], "python traceback below :\n{0}".format(traceback.format_exc()))
#-------------------------------------------------------------------------------
# log_trace
#   Logs a trace in traces' log
#-------------------------------------------------------------------------------
def log_trace(msg):
    if _LOGS_:
        _log(_LOGS_['stdout'], msg)
#-------------------------------------------------------------------------------
# mprint
#   Prints a message to stdout and add a trace to traces log 
#-------------------------------------------------------------------------------
def mprint(msg):
    logline = "{0}[mapif] > {1}".format(timer.get_date(), msg)
    log_trace(logline)
    print(logline)
#-------------------------------------------------------------------------------
# init_logs
#   Initializes logging module, creating missing log files if needed
#-------------------------------------------------------------------------------
def init_logs():
    global _LOGS_
    global _LOG_PERF_
    global _LOG_DIR_
    try:
        _LOG_DIR_ = ini.config('LOGGER', 'log_dir', default='logs/')
        _LOGS_ = {
            'stdout': ini.config('LOGGER', 'std_log', default='mapif.log'),
            'perfout': ini.config('LOGGER', 'perf_log', default='mapif.perf.log'),
            'stderr': ini.config('LOGGER', 'err_log', default='mapif.err.log')
        }
        _LOG_PERF_ = ini.config('LOGGER','log_perf', default=False, boolean=True)
        for logfile in _LOGS_.values():
            _create_log(logfile)
        mprint("Logging module successfully initialized.")
    except Exception as e:
        mprint("Logging module initialization failed.")
        log_error("Logging module initialization failed.", e)
#===============================================================================
# TESTS
#===============================================================================
def test():
    print('LOGGER - TESTS NOT IMPLEMENTED')
