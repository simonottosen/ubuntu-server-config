#!/bin/sh
echo "cd /home/simonottosen/mediaserver" > ../pipe/deploy
echo "docker compose pull" > ../pipe/deploy
echo "git pull https://github.com/simonottosen/ubuntu-server-config.git" > ../pipe/deploy
echo "docker compose up -d --remove-orphans" > ../pipe/deploy
