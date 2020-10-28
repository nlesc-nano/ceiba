#!/bin/bash

if [[ -z "${MONGO_USER}" ]]; then
    MONGO_USER=admin
fi

insilico-server -m  172.17.02 -u "${MONGO_USER}" -p "${MONGO_PASSWORD}"
