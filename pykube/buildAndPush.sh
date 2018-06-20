set -e
set -x
TAG="mlda065/mcapi"
sudo docker build -t $TAG ./ 
#sudo docker run -it --rm mlda065/mcapi
sudo docker push $TAG
