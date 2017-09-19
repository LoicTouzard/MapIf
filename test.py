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
from src.utils import db
from src.utils import ini
from src.utils import logger
from src.utils import nominatim
from src.utils import response
from src.utils import timer
from src.utils import validator
from src import mapif
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
