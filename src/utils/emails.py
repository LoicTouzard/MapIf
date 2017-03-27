import requests
import re
import html

from flask import escape
from flask import render_template

from src.utils import ini
from src.utils import logger

# See http://api.elasticemail.com/public/help#Email_Send for documentation
_APIURL_ = 'https://api.elasticemail.com/v2/email/send'
_APIKEY_ = None
_APP_ROOT_=''
_EMAIL_TEMPLATE_DIR_ = 'src/templates/emails/'
_EMAIL_ENCODING_ = 'utf-8'
_SENDER_EMAIL_ = 'noreply@mapif.com'
_SENDER_NAME_ = 'MapIf'


def init_emails(app_root):
    global _APIKEY_
    global _APP_ROOT_
    _APP_ROOT_ = app_root
    try:
        _APIKEY_ = ini.config('EMAILS', 'elasticmail_apikey', default=None)
        if _APIKEY_ is None or _APIKEY_ == '':
            logger.mprint('No Email APIKEY found')
        else:
            logger.mprint('Email APIKEY: {0}'.format(_APIKEY_))
    except Exception as ex:
        logger.mprint("Could not load ElasticEmail API KEY")

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
    response = requests.get(_APIURL_, params=params)
    # print(response.url)
    # print(response)
    resp_json = response.json()
    # print(resp_json)
    if resp_json['success']:
        logger.mprint('Sent email successfully to {0}'.format(to))
    else:
        logger.log_error(resp_json['error'])

def send_password_reset_mail(email, firstname, reset_link):
    params = {
        'firstname': firstname,
        'reset_link': reset_link
    }
    send_email(email, 'Mot de passe oublié', 'emails/password_reset_simple.html', params)

