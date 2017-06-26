#!/usr/bin/env bash

printf "\e[1mBUILDING jiss/file-service version ${1:-local}...\e[0m\n"

docker build -t jiss/file-service:${1:-local} . || {
    printf "\e[31mDOCKER IMAGE BUILD FAIL!\e[0m\n" 1>&2
    exit 1;
}

printf "\e[1mDOCKER IMAGE BUILD DONE.\e[0m\n"

printf "\e[1mDOCKER STARTING...\e[0m\n"

docker ps -a | grep file-service && docker rm -f file-service
docker run -d --name file-service -p 33003:33003 -v $(pwd)/handler:/usr/lib/file-service/handler jiss/file-service:${1:-local}
