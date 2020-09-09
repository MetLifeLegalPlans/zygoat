#!/bin/bash

nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2&

timeout 15 sh -c "until docker info 2>/dev/null; do echo .; sleep 1; done"

COMPOSE_HTTP_TIMEOUT=200 docker-compose up -d --build
