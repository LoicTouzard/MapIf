#!/bin/python
# -!- encoding:utf-8 -!-

import os

_COLOR_MAP_={
    'red':31,
    'green':32,
    'yellow':33,
    'blue':34,
    'magenta':35,
    'cyan':36,
    'white':37
}
_PROMPT_='[deploy_patch]> '

def echo(msg, color='white'):
    print("\033[{0}m{1}{2}\033[0m".format(_COLOR_MAP_.get(color,37), _PROMPT_, msg))

_APP_URL_='mapif-insa.rhcloud.com'

_APP_ROOT_=os.getenv('OPENSHIFT_REPO_DIR')
if not _APP_ROOT_:
    echo('fatal error : missing environement variable !', 'red')
    exit(1)

# patch route in main.js -----------------------------------
_MAIN_JS_=_APP_ROOT_+'src/static/js/main.js'
content = ''
echo('patching main.js ...', 'green')
try:
    # read source from file
    with open(_MAIN_JS_, 'r', encoding='utf-8') as f:
        content = f.read()
    # patch source
    content = content.replace('localhost:5000', _APP_URL_)
    # write back patched source
    with open(_MAIN_JS_, 'w', encoding='utf-8') as f:
        f.write(content)
    # print ok message
    echo('done!', 'green')
except Exception, e:
    echo('failed!', 'red')
# ---------------------------------------------------------
