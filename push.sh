#!/usr/bin/env bash

USERNAME=${1:-xezzed}

docker build -t travian-bot .
docker tag travian-bot:latest ${USERNAME}/travian-bot
docker push ${USERNAME}/travian-bot