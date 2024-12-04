#!/bin/bash

set -e
set -x

BASE_IMAGE=yourdockerrepo/lithops:alpine_python310-scone-lithops350
MADE_IMAGE=yourdockerrepo/lithops:alpine_python310-scone-lithops350.1
DOCKERFILE=Dockerfile.lithops.python3.10.4.patches
LT_VERSION="${LT_VERSION:=3.5.0}"

###
# if you want to clean Docker build cache, uncomment these 2 lines
#(docker image ls |grep -w none.*none |awk '{print $3}' |xargs docker rmi -f |cat -n |tail) || true
#test `docker builder ls |grep -E -v -e default -e ^NAME |wc -l` -gt 0 && docker builder prune -a -f 2>&1 |cat -n |tail || true

###
# Build SCONE Kubernetes prepared image
docker build --no-cache --progress plain --build-arg BASE_IMAGE=${BASE_IMAGE}.int --build-arg LT_VERSION=$LT_VERSION -f $DOCKERFILE -t $MADE_IMAGE .
docker push $MADE_IMAGE 2>&1 |tail -5
