#!/bin/python
# -!- encoding:utf-8 -!-

import os, json

_DEBUG_ = False

_COLOR_MAP_ = {
    'red':31,
    'green':32,
    'yellow':33,
    'blue':34,
    'magenta':35,
    'cyan':36,
    'white':37
}
_PROMPT_ = '[deploy_patch]> '

def echo(msg, color='white'):
    print("\033[{0}m{1}{2}\033[0m".format(_COLOR_MAP_.get(color,37), _PROMPT_, msg))

_APP_ROOT_ = os.getenv('OPENSHIFT_REPO_DIR')
if not _APP_ROOT_:
    if _DEBUG_:
        _APP_ROOT_ = ''
    else:
        echo('fatal error : missing environement variable !', 'red')
        exit(1)

# patch settings.json -----------------------------------
_SETTINGS_FILE_ = _APP_ROOT_ + 'src/static/settings.json'
try:
    with open(_SETTINGS_FILE_, 'r') as f:
        settings = json.load(f)
    if _DEBUG_:
        print(json.dumps(settings, indent=4))
    settings['DEBUG'] = False
    settings['PROTOCOL'] = 'https'
    settings['SERVER_ADDR'] = 'mapif-insa.rhcloud.com'
    if _DEBUG_:
        print(json.dumps(settings, indent=4))
    else:
        with open(_SETTINGS_FILE_, 'w') as f:
            f.write(json.dumps(settings))
except Exception as e:
    echo('fatal error : {0}'.format(e))
# ---------------------------------------------------------
