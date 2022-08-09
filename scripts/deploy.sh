#!/bin/sh
echo "cd /home/simonottosen/mediaserver" > /hostpipe/deploy
echo "docker compose pull" > /hostpipe/deploy
echo "git pull https://github.com/simonottosen/ubuntu-server-config.git" > /hostpipe/deploy
echo "docker compose up -d" > /hostpipe/deploy