#!/usr/bin/python3
# -!- encoding:utf8 -!-

from src import server
from src.utils import ini

if ini.init_config('mapif.ini'):
    server.launch()
else:
    print("Configuration file is missing. Server can't be started !")
