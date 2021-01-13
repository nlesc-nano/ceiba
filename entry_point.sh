#!/bin/bash

if [[ -z "${MONGO_USER}" ]]; then
    MONGO_USER=admin
fi

ceiba -m  172.17.02 -u "${MONGO_USER}" -p "${MONGO_PASSWORD}"  -f users.txt &
wait $!