#!/bin/python
# -!- encoding:utf-8 -!-

import os

_APP_URL_='mapif-insa.rhcloud.com'

_APP_ROOT_=os.getenv('OPENSHIFT_REPO_DIR')
if not _APP_ROOT_:
    print('Fatal error : missing environement variable !')
    exit(1)

# patch route in main.js -----------------------------------
_MAIN_JS_=_APP_ROOT_+'src/static/js/main.js'
content = ''
with open(_MAIN_JS_, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('localhost:5000', _APP_URL_)

with open(_MAIN_JS_, 'w', encoding='utf-8') as f:
    f.write(content)
# ---------------------------------------------------------
