import requests

from src.utils import ini
from src.utils import logger

# See http://api.elasticemail.com/public/help#Email_Send for documentation
_APIURL_ = 'https://api.elasticemail.com/v2/email/send'
_APIKEY_ = None


def init_emails():
    global _APIKEY_
    try:
        _APIKEY_ = ini.config('EMAILS', 'elasticmail_apikey', default=None)
        if _APIKEY_ is None or _APIKEY_ == '':
            logger.mprint('No Email APIKEY found')
        else:
            logger.mprint('Email APIKEY: {0}'.format(_APIKEY_))
    except Exception as ex:
        logger.mprint("Could not load ElasticEmail API KEY")


def send_password_reset_mail(email, reset_link):
    global _APIKEY_
    global _APIURL_

    email_html = 'Salut,<br>\
Alors comme ça tu as oublié ton mot de passe hein... Bravo.<br>\
<a href="{0}">Voici un petit lien pour que tu puisses en saisir un nouveau.<a/>'.format(reset_link)

    params = {
        'apikey': _APIKEY_,
        'bodyHtml': email_html,
        'to': email,
        'charset': 'utf-8',
        'from': 'noreply@mapif.com',
        'fromName': 'MapIf',
        'subject': '[MapIf] Mot de passe oublié'
    }
    response = requests.get(_APIURL_, params=params)
    resp_json = response.json()
    if resp_json['success']:
        logger.mprint('Sent email successfully to {0}'.format(email))
    else:
        logger.log_error(resp_json['error'])
