#!/bin/bash

set -e
set -x

BASE_IMAGE=registry.scontain.com/amiguel/neardatapublic/golang:1.22.0-alpine3.19-scone5.8.0-130-g3bda21683-vasyl-golang-updates-procfs
MADE_IMAGE=yourdockerrepo/minio:release_git
LATEST_IMAGE=yourdockerrepo/minio:latest
DOCKERFILE=Dockerfile.minio.sign

###
# if you want to clean Docker build cache, uncomment these 2 lines
#(docker image ls |grep -w none.*none |awk '{print $3}' |xargs docker rmi -f |cat -n |tail) || true
#test `docker builder ls |grep -E -v -e default -e ^NAME |wc -l` -gt 0 && docker builder prune -a -f 2>&1 |cat -n |tail || true

###
# Build first larger and base image. It is not necessary to push it
# It takes a long time to build. You can keep it in your workstation or push it for later rebuild the next stages
docker build --no-cache --progress plain --build-arg BASE_IMAGE=$BASE_IMAGE -f $DOCKERFILE -t $MADE_IMAGE .
docker push $MADE_IMAGE 2>&1 |tail -5

docker tag $MADE_IMAGE $LATEST_IMAGE

docker push $LATEST_IMAGE 2>&1 |tail -5
