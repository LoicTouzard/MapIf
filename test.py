#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                    IMPORTS & GLOBALS
# ------------------------------------------------------------------------------------------

from src.utils import db
from src.utils import ini
from src.utils import logger
from src.utils import nominatim
from src.utils import response
from src.utils import timer
from src.utils import validator
from src import mapif

# ------------------------------------------------------------------------------------------
#                                    IMPORTS & GLOBALS
# ------------------------------------------------------------------------------------------

db.test()
ini.test()
logger.test()
nominatim.test()
response.test()
timer.test()
validator.test()
mapif.test()