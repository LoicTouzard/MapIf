INI_DIR=app-root/runtime/repo/
INI_FILE=mapif.ini
APP=mapif

becho() { echo -e "\033[34m[deploy_openshift]> ${1}\033[0m"; }

becho "calling git to push latest commit to openshift..."
git push openshift master
becho "done!"
becho "calling rhc to deploy app..."
sudo rhc deploy master -a ${APP}
becho "done!"
becho "calling rhc to send configuration file to openshift..."
sudo rhc scp ${APP} upload ${INI_FILE} ${INI_DIR}
becho "done!"
becho "calling rhc to restart application..."
sudo rhc app restart -a ${APP}
becho "done!"
becho "calling rhc to read logs after deployement..."
sudo rhc tail -a ${APP}
becho "done!"
