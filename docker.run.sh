#!/usr/bin/env bash

CUR_NAME=file-service
CUR_IMAGE=jiss/file-service:${1:-local}

printf "\e[1mBUILDING ${CUR_IMAGE}...\e[0m\n"

docker build -t "${CUR_IMAGE}" . || {
    printf "\e[31mDOCKER IMAGE BUILD FAIL!\e[0m\n" 1>&2
    exit 1;
}

printf "\e[1mDOCKER IMAGE BUILD DONE.\e[0m\n"

printf "\e[1mDOCKER STARTING...\e[0m\n"

docker ps -a | grep "${CUR_NAME}" && docker rm -f "${CUR_NAME}"
docker run -d --name "${CUR_NAME}" -p 33003:33003 -v $(pwd)/handler:/usr/lib/file-service/handler "${CUR_IMAGE}"
