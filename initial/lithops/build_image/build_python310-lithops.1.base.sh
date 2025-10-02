#!/bin/bash

set -e
set -x

MADE_IMAGE=yourdockerrepo/lithops:alpine_python310-lithops350.1.base
DOCKERFILE=Dockerfile.lithops.python3.10.1.base
LT_VERSION="${LT_VERSION:=3.5.0}"

###
# if you want to clean Docker build cache, uncomment these 2 lines
#(docker image ls |grep -w none.*none |awk '{print $3}' |xargs docker rmi -f |cat -n |tail) || true
#test `docker builder ls |grep -E -v -e default -e ^NAME |wc -l` -gt 0 && docker builder prune -a -f 2>&1 |cat -n |tail || true

###
# Build first larger and base image. It is not necessary to push it
# It takes a long time to build. You can keep it in your workstation or push it for later rebuild the next stages
docker build --no-cache --progress plain --build-arg LT_VERSION=$LT_VERSION -f $DOCKERFILE -t $MADE_IMAGE .
