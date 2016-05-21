echo "Pushing latest commit to openshift..."
git push openshift master
echo "done!"
echo "Asking openshift to deploy app..."
sudo rhc deploy master -a mapif
echo "done!"
echo "Sending configuration file to openshift..."
sudo rhc scp mapif upload mapif.ini app-root/runtime/repo/
echo "done!"
echo "Asking openshift to restart application..."
sudo rhc app restart -a mapif
echo "done!"
