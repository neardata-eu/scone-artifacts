#!/bin/bash

set -e
set -x

BASE_IMAGE=yourdockerrepo/lithops:alpine_python310-lithops350.1.base
MADE_IMAGE=yourdockerrepo/lithops:alpine_python310-lithops350.2.scratch
DOCKERFILE=Dockerfile.lithops.python3.10.2.scratch
LT_VERSION="${LT_VERSION:=3.5.0}"

###
# if you want to clean Docker build cache, uncomment these 2 lines
#(docker image ls |grep -w none.*none |awk '{print $3}' |xargs docker rmi -f |cat -n |tail) || true
#test `docker builder ls |grep -E -v -e default -e ^NAME |wc -l` -gt 0 && docker builder prune -a -f 2>&1 |cat -n |tail || true

###
# Build intermediary image. Can be used to make modifications in installation
# The result will be used as basis for both SCONE and Vanilla Lithops in next stage
docker build --no-cache --progress plain --build-arg LT_VERSION=$LT_VERSION --build-arg BASE_IMAGE=$BASE_IMAGE -f $DOCKERFILE -t $MADE_IMAGE .
