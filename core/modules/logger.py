#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: logger.py
#    date: 2017-09-22
# authors: paul.dautry, ...
# purpose:
#       Logging module relying on Python logging module.   
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
import logging
import logging.handlers as handlers
#===============================================================================
# GLOBALS
#===============================================================================
ROOT_LGR = 'mapif'
# create formatter
FMT = '(%(asctime)s)[%(name)s:%(levelname)s]: %(message)s'
FMTR = logging.Formatter(FMT)
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# get
#   Retrieves logger having given name
#-------------------------------------------------------------------------------
def get(lgr_name):
    return logging.getLogger(lgr_name)
#-------------------------------------------------------------------------------
# init
#   Initializes logging module, creating missing log files if needed
#-------------------------------------------------------------------------------
def init():
    # set configuration values
    logs_dir = 'logs/'
    std_log = 'mapif.log'
    err_log = 'mapif.err.log'
    dbg_log = 'mapif.dbg.log'
    # make missing directories if needed
    os.makedirs(logs_dir, exist_ok=True)
    # create & configure handlers
    # -- std log file handler
    std_fh = handlers.RotatingFileHandler(os.path.join(logs_dir, std_log),
        maxBytes=1000*1024, backupCount=2)
    std_fh.setLevel(logging.INFO) # inf + err + crit
    std_fh.setFormatter(FMTR)
    # -- err log file handler
    err_fh = handlers.RotatingFileHandler(os.path.join(logs_dir, err_log),
        maxBytes=1000*1024, backupCount=2)
    err_fh.setLevel(logging.ERROR) # err + crit
    err_fh.setFormatter(FMTR)
    # -- dbg log file handler
    dbg_fh = handlers.RotatingFileHandler(os.path.join(logs_dir, dbg_log),
        maxBytes=1000*1024, backupCount=2)
    dbg_fh.setLevel(logging.DEBUG) # dbg + inf + err + crit
    dbg_fh.setFormatter(FMTR)
    # -- console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(FMTR)
    # create & configure mapif logger
    logr = logging.getLogger(ROOT_LGR)
    logr.setLevel(logging.DEBUG)
    logr.addHandler(std_fh)
    logr.addHandler(err_fh)
    logr.addHandler(dbg_fh)
    logr.addHandler(ch)
#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
def disable_debug():
    logr = logging.getLogger(ROOT_LGR)
    logr.setLevel(logging.INFO)
#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
def add_handler(handler):
    logr = logging.getLogger(ROOT_LGR)
    logr.addHandler(handler)
#===============================================================================
# TESTS
#===============================================================================
def test():
    print('LOGGER - TESTS NOT IMPLEMENTED')
