#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: emails.py
#    date: 2017-09-22
# authors: david.wobrock, paul.dautry, ...
# purpose:
#       Mailing module based on Elasticemail API
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
import re
import html
from flask        import escape
from flask        import render_template
from core.modules import ini
from core.modules import logger
from core.modules import request
#===============================================================================
# GLOBALS
#===============================================================================
# See http://api.elasticemail.com/public/help#Email_Send for documentation
_APIURL_ = 'https://api.elasticemail.com/v2/email/send'
_APIKEY_ = None
_EMAIL_TEMPLATE_DIR_ = 'src/templates/emails/'
_EMAIL_ENCODING_ = 'utf-8'
_SENDER_EMAIL_ = 'noreply@mapif.com'
_SENDER_NAME_ = 'MapIf'
modlgr = logger.get('mapif.email')
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# init_emails
#-------------------------------------------------------------------------------
def init():
    global _APIKEY_
    try:
        _APIKEY_ = ini.config('EMAILS', 'elasticmail_apikey', default=None)
        if _APIKEY_ is None or _APIKEY_ == '':
            modlgr.warning('No Email APIKEY found')
        else:
            modlgr.debug('Email APIKEY: {0}'.format(_APIKEY_))
    except Exception as ex:
        modlgr.exception("Could not load ElasticEmail API KEY")
#-------------------------------------------------------------------------------
# send_email
#-------------------------------------------------------------------------------
def send_email(to, subject, template, template_params):
    global _APIKEY_
    global _APIURL_
    # prepare parameters
    template_params = {k: html.escape(v) for k, v in template_params.items()}
    # try to send mail
    email_html = render_template(template, **template_params)
    # print(len(email_html))
    email_html = re.sub(r">\s+<", r"><", email_html)
    # print(len(email_html))
    params = {
        'apikey': _APIKEY_,
        'bodyHtml': email_html,
        'to': to,
        'charset': _EMAIL_ENCODING_,
        'from': _SENDER_EMAIL_,
        'fromName': _SENDER_NAME_,
        'subject': '[MapIf] - '+subject
    }
    # print(params)
    response = request.get(_APIURL_, params=params)
    # print(response.url)
    # print(response)
    resp_json = response.json()
    # print(resp_json)
    if resp_json['success']:
        modlgr.debug('Sent email successfully to {0}'.format(to))
    else:
        modlgr.error(resp_json['error'])
#-------------------------------------------------------------------------------
# send_password_reset_mail
#-------------------------------------------------------------------------------
def send_password_reset_mail(email, firstname, token):
    params = {
        'firstname': firstname,
        'token': token,
        'email': email
    }
    send_email(email, 'Mot de passe oublié', 'emails/password_reset_simple.html', params)
#===============================================================================
# TESTS
#===============================================================================
def test():
    raise NotImplementedError
