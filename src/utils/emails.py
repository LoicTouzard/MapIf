import requests

from flask import escape

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

def send_email(to, subject, template, params):
    global _APIKEY_
    global _APIURL_
    # prepare mail
    try:
        email_html = ''
        email_html_body = ''
        # retrieve mapif automatic mail template
        with open(_EMAIL_TEMPLATE_DIR_ + 'mapif_mail.html') as f:
            email_html = f.read()
        # retrieve mail-specific content
        with open(_EMAIL_TEMPLATE_DIR_ + template) as f:
            email_html_body = f.read()
        # substitute parameters
        for key, value in params.items():
            email_html_body = email_html_body.replace('[[{0}]]'.format(key), value)
        # substitute mail-specific body in common template
        email_html = email_html.replace('[[email_html_body]]', email_html_body)
    except Exception as e:
        logger.log_error('[ERR]: send_mail exception! Details: {0}'.format(e))
    # try to send mail
    params = {
        'apikey': _APIKEY_,
        'bodyHtml': email_html,
        'to': to,
        'charset': _EMAIL_ENCODING_,
        'from': _SENDER_EMAIL_,
        'fromName': _SENDER_NAME_,
        'subject': '[MapIf] - '+subject
    }
    response = requests.get(_APIURL_, params=params)
    resp_json = response.json()
    if resp_json['success']:
        logger.mprint('Sent email successfully to {0}'.format(to))
    else:
        logger.log_error(resp_json['error'])

def send_password_reset_mail(email, firstname, reset_link):
    params = {
        'firstname': firstname,
        'reset_link': reset_link
    }
    send_email(email, 'Mot de passe oublié', 'password_reset.html', params)

