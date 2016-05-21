echo "[deploy_openshift]> pushing latest commit to openshift..."
git push openshift master
echo "[deploy_openshift]> done!"
echo "[deploy_openshift]> asking openshift to deploy app..."
sudo rhc deploy master -a mapif
echo "[deploy_openshift]> done!"
echo "[deploy_openshift]> sending configuration file to openshift..."
sudo rhc scp mapif upload mapif.ini ./
echo "[deploy_openshift]> done!"
echo "[deploy_openshift]> asking openshift to restart application..."
sudo rhc app restart -a mapif
echo "[deploy_openshift]> done!"
echo "[deploy_openshift]> printing logs after deployement..."
sudo rhc tail -a mapif
echo "[deploy_openshift]> done!"
