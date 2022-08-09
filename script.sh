sudo apt -y update
sudo apt -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common apt zfsutils-linux
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
mkdir mediaserver
cd mediaserver
curl https://transfer.sh/ATz0zb/docker-compose.yml >> docker-compose.yml
mkdir config
mkdir config/letsencrypt
cd config/letsencrypt
curl https://transfer.sh/AgRtO7/acme.json >> acme.json
cd ..
cd ..
docker-compose up
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -
echo deb https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list
sudo apt -y update
sudo apt -y install plexmediaserver
sudo mkdir -p plexmedia/{movies,series}
sudo chown -R plex: plexmedia
sudo zfs get all
sudo zfs set mountpoint=/media data
sudo chown -R $USER:$USER /media
sudo apt-get install webhook

#/dev/md127pi 
# sudo apt-get install xfsprogs
