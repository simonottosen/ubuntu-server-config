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
git init
git pull https://github.com/simonottosen/ubuntu-server-config.git
chmod u+x scripts/deploy.sh
chmod u+x pipe/execpipe.sh
mkfifo pipe/deploy
crontab -l > mycron
echo "@reboot /home/simonottosen/mediaserver/pipe/execpipe.sh" >> mycron
crontab mycron
rm mycron
sudo zfs get all
sudo zfs set mountpoint=/media data
sudo chown -R $USER:$USER /media
sudo apt-get install webhook



#/dev/md127pi 
# sudo apt-get install xfsprogs



