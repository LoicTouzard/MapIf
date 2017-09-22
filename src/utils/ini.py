#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: ini.py
#    date: 2017-09-22
# authors: paul.dautry, ...
# purpose:
#       Load configuration variables
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
import configparser
import os
#===============================================================================
# GLOBALS 
#===============================================================================
_CONFIG_ = None
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# init_config
#   Initializes configuration loading it from INI file
#-------------------------------------------------------------------------------
def init_config(filename):
    global _CONFIG_
    ok = False
    if not _CONFIG_:
        _CONFIG_ = configparser.ConfigParser()
        if len(_CONFIG_.read(filename, encoding='utf-8')) > 0:
            print('[mapif.ini](INFO)> Configuration file {0} successfully loaded !'.format(filename))
            ok = True
        else:
            print("[mapif.ini](ERR)> Configuration file {0} can't be loaded !".format(filename))
    else:
        print('[mapif.ini](ERR)> Configuration file has already been loaded !')
    return ok
#-------------------------------------------------------------------------------
# getenv
#   Returns a configuration value from an environnement variable
#-------------------------------------------------------------------------------
def getenv(env_var, default=None):
    return os.getenv(env_var, default)
#-------------------------------------------------------------------------------
# config
#   Tries to retrieve configuration from:
#       1. an environement variable 
#       2. then falls back to INI file
#       3. finally return default value if the previous operations failed.
#-------------------------------------------------------------------------------
def config(section, option, env_var=None, default=None, boolean=False):
    res = None
    if env_var:
        res = getenv(env_var)
    if not res:
        if _CONFIG_:
            if section in _CONFIG_.sections():
                if option in _CONFIG_[section]:
                    if boolean:
                        res = _CONFIG_[section].getboolean(option)
                    else:
                        res = _CONFIG_[section][option]
                else:
                    print("[mapif.ini](ERR)>  Missing option {0} in section {1} in configuration file !".format(option, section))
                    if default:
                        print("[mapif.ini](INFO)> Using default configuration value: {0}".format(default))
                        res = default
            else:
                print("[mapif.ini](ERR)> Missing section {0} in configuration file".format(section))
                if default:
                    print("[mapif.ini](INFO)> Using default configuration value: {0}".format(default))
                    res = default
        else:
            print("[mapif.ini](ERR)> Configuration file must be loaded to use config(section, option) function ! Call init_config(filename) before !")
            if default:
                print("[mapif.ini](INFO)> Using default configuration value: {0}".format(default))
                res = default
    return res
#===============================================================================
# TESTS
#===============================================================================
def test():
    out = 'Configuration loaded from mapif.ini\n'
    for section in _CONFIG_.sections():
        out += ' + {0}\n'.format(section)
        for option in _CONFIG_.options(section):
            out += '    - {0} = {1}\n'.format(option, _CONFIG_[section][option])
    print(out)