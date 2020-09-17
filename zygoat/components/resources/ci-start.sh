#!/bin/bash

apt-get install -y jq

nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2&

timeout 15 sh -c "until docker info 2>/dev/null; do echo .; sleep 1; done"

export SECRETS_OUTPUT="$(aws secretsmanager get-secret-value --secret-id docker-hub-credentials --query SecretString --output text)"

export USERNAME="$(echo $SECRETS_OUTPUT | jq -r .username)"
export PASSWORD="$(echo $SECRETS_OUTPUT | jq -r .password)"

docker login -u "$USERNAME" -p "$PASSWORD"

COMPOSE_HTTP_TIMEOUT=200 docker-compose up -d --build
