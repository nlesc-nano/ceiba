#!/bin/bash

if [[ -z "${MONGO_PASSWORD}" ]]; then
    echo "There is not MONGO_PASSWORD env. variable defined!"
    exit 1
fi

docker-compose pull
docker-compose up -d