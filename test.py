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
from core.utils import db
from core.utils import ini
from core.utils import logger
from core.utils import nominatim
from core.utils import response
from core.utils import timer
from core.utils import validator
from core import mapif
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------
def main():
    db.test()
    ini.test()
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
