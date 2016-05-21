INI_DIR=app-root/runtime/repo/
INI_FILE=mapif.ini
APP=mapif

echo "[deploy_openshift]> pushing latest commit to openshift..."
git push openshift master
echo "[deploy_openshift]> done!"
echo "[deploy_openshift]> asking openshift to deploy app..."
sudo rhc deploy master -a ${APP}
echo "[deploy_openshift]> done!"
echo "[deploy_openshift]> sending configuration file to openshift..."
sudo rhc scp ${APP} upload ${INI_DIR}${INI_FILE} ${INI_DIR}
echo "[deploy_openshift]> done!"
echo "[deploy_openshift]> asking openshift to restart application..."
sudo rhc app restart -a ${APP}
echo "[deploy_openshift]> done!"
echo "[deploy_openshift]> printing logs after deployement..."
sudo rhc tail -a ${APP}
echo "[deploy_openshift]> done!"
