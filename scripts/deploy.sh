#!/bin/sh

cd /home/simonottosen/mediaserver
docker compose pull
git pull https://github.com/simonottosen/ubuntu-server-config.git
docker compose up -d 