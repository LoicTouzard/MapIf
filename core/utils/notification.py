#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: notification.py
#    date: 2017-09-23
#  author: paul.dautry
# purpose:
#   
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
import json
from core.utils import logger
from core.utils import ini
from core.utils import request
#===============================================================================
# GLOBALS / CONFIG
#===============================================================================
SLACK_WEBHOOK = None
LVL_ERR = 0
LVL_WRN = 1
LVL_INF = 2
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# init
#-------------------------------------------------------------------------------
def init():
    global SLACK_WEBHOOK
    SLACK_WEBHOOK = ini.config('NOTIFICATION', 'slack_webhook', 'MAPIF_SLACK_WEBHOOK')
    if SLACK_WEBHOOK is None:
        logger.mprint('No SLACK_WEBHOOK configured. You will not be notified.')
#-------------------------------------------------------------------------------
# __notify
#-------------------------------------------------------------------------------
def __notify(lvl, value):
    if SLACK_WEBHOOK is None:
        return
    if lvl is LVL_ERR: 
        title = "An error occurred!"
        pretext = ""
        color = '#D00000'
    elif lvl is LVL_WRN:
        title = "Don't you smell something ?"
        pretext = ""
        color = '#D16800'
    else: 
        title = "Breaking news!"
        pretext = ""
        color = '#00D000'
    # prepare payload
    pld = {
        "text": "",
        "attachments": [
            {
                "fallback": pretext,
                "pretext": pretext,
                "color": color,
                "fields": [
                    {
                        "title": title,
                        "value": value,
                        "short": False,
                    }
                ],
                "mrkdwn_in": [ "fields" ]
            }
        ]
    }
    # send payload
    r = request.post(SLACK_WEBHOOK, 
        timeout=2, 
        data=json.dumps(pld), 
        headers={'Content-Type':'application/json'})
    logger.mprint(r.text)
#-------------------------------------------------------------------------------
# notify_err
#-------------------------------------------------------------------------------
def notify_err(value):
    __notify(LVL_ERR, value)
#-------------------------------------------------------------------------------
# notify_wrn
#-------------------------------------------------------------------------------
def notify_wrn(value):
    __notify(LVL_WRN, value)
#-------------------------------------------------------------------------------
# notify_inf 
#-------------------------------------------------------------------------------
def notify_inf(value):
    __notify(LVL_INF, value)
#===============================================================================
# TESTS
#===============================================================================
def test():
    print('NOTIFICATION - TESTS NOT IMPLEMENTED')
