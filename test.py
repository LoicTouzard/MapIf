#!/usr/bin/python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: test.py
#    date: 2017-09-19
#  author: paul.dautry
# purpose:
#   Module (incomplete :/) testing
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#===============================================================================
# IMPORTS
#===============================================================================
from core.modules import ini
from core.modules import db
from core.modules import logger
from core.modules import nominatim
from core.modules import validator
from core.classes import response
from core import mapif
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------
def main():
    ini.test()
    db.test()
    logger.test()
    nominatim.test()
    response.test()
    timer.test()
    validator.test()
    mapif.test()
    exit(0)
#===============================================================================
# SCRIPT
#===============================================================================
if __name__ == '__main__':
    main()
