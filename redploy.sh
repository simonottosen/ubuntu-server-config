#!bin/bash
docker pull example/repository:latest
docker stop SAMPLE_APP
docker system prune -f
docker run -d --name=SAMPLE_APP example/repository:latest
