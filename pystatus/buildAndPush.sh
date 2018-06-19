set -e
set -x
sudo docker build -t mlda065/mcstatus ./
sudo docker push mlda065/mcstatus
