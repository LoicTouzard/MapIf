#!/bin/bash
# -------------------------------------------------------------------
#       CONFIGURATION
# -------------------------------------------------------------------
INI_DIR=app-root/runtime/repo/
INI_FILE=mapif.ini
APP=mapif
BRANCH=master
# -------------------------------------------------------------------
#       FUNCTIONS
# -------------------------------------------------------------------
colecho() { echo -e "\033[${1}m[deploy_openshift]> ${2}\033[0m"; }
becho() { colecho 34 "${1}"; }
gecho() { colecho 32 "${1}"; }
recho() { colecho 31 "${1}"; }
ok() { gecho "done."; }
ko() { recho "failed!"; }
# -------------------------------------------------------------------
#       MAIN SCRIPT
# -------------------------------------------------------------------
becho "calling git to push latest commit to openshift..."
(git push openshift ${BRANCH} && ok) ||ko
becho "calling rhc to stop app..."
(sudo rhc app stop -a ${APP} && ok) ||ko
becho "calling rhc to deploy app..."
(sudo rhc deploy ${BRANCH} -a ${APP} && ok) ||ko
becho "calling rhc to send configuration file to openshift..."
(sudo rhc scp ${APP} upload ${INI_FILE} ${INI_DIR} && ok) ||ko
#becho "calling rhc to restart application..."
#(sudo rhc app restart -a ${APP} && ok) ||ko
becho "calling rhc to read logs after deployement..."
(sudo rhc tail -a ${APP} && ok) ||ko
