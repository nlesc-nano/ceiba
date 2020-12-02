#!/bin/bash

if [[ -z "${MONGO_PASSWORD}" ]]; then
    echo "There is not MONGO_PASSWORD env. variable defined!"
    exit 1
fi

docker-compose -f "${DOCKER_COMPOSE_FILE}" pull
docker-compose -f "${DOCKER_COMPOSE_FILE}" up -d