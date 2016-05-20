#!/usr/bin/python3
# -!- encoding:utf8 -!-

from src.utils import ini

if not ini.init_config('mapif.ini'):
    print("Configuration file is missing. Server can't be started !")
    exit(-1)

from src import server

server.launch()
