#!/bin/bash

if [[ -z "${MONGO_PASSWORD}" ]]; then
    echo "There is not MONGO_PASSWORD env. variable defined!"
    exit 1
fi

docker-compose -f docker-compose.yml pull
docker-compose -f docker-compose.yml up -d