#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: slack_log_handler.py
#    date: 2017-09-23
#  author: paul.dautry
# purpose:
#       This class can be used to log events to a Slack channel.
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
import logging
import traceback
from core.modules   import ini
from core.modules   import request
#===============================================================================
# CLASS
#===============================================================================
class SlackLogHandler(logging.Handler):
    #---------------------------------------------------------------------------
    # __init__
    #---------------------------------------------------------------------------
    def __init__(self, webhook):
        # init parent class
        super(SlackLogHandler, self).__init__(logging.INFO)
        # save slack webhook
        self.webhook = webhook 
    #---------------------------------------------------------------------------
    # emit
    #---------------------------------------------------------------------------
    def emit(self, record):
        if self.webhook is not None:
            pretext = 'server time: `{0}`'.format(record.asctime) 
            if record.levelno == logging.INFO:
                title = 'INFO'
                color = '#00D000'
            elif record.levelno == logging.WARNING:
                title = 'WARNING'
                color = '#D16800'
            elif record.levelno == logging.ERROR:
                title = 'ERROR'
                color = '#D00000'
            elif record.levelno == logging.CRITICAL:
                title = 'CRITICAL'
                color = '#660066'
            value = record.message
            if record.exc_info is not None:
                typ = record.exc_info[0].__name__
                val = record.exc_info[1]
                tb = ''.join(traceback.format_tb(record.exc_info[2]))
                value += '\n```{0}{1}: {2}```'.format(tb, typ, val)
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
                        "mrkdwn_in": [ 
                            "pretext", 
                            "fields" 
                        ]
                    }
                ]
            }
            #print(json.dumps(pld, indent=4))
            # send payload
            r = request.post(self.webhook, 
                timeout=1.5, 
                data=json.dumps(pld), 
                headers={
                    'Content-Type':'application/json'
                })
#===============================================================================
# TESTS
#===============================================================================
def test():
    raise NotImplementedError