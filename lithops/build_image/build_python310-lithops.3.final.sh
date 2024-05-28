#!/bin/bash

set -e
set -x

BASE_IMAGE=yourdockerrepo/lithops:alpine_python310-lithops301.2.scratch
MADE_IMAGE=yourdockerrepo/lithops:alpine_python310-scone-lithops301
VNLA_IMAGE=yourdockerrepo/lithops:alpine_python310-vanilla-lithops301
DOCKERFILE=Dockerfile.lithops.python3.10.3.sign
LT_VERSION="${LT_VERSION:=3.0.1}"

###
# if you want to clean Docker build cache, uncomment these 2 lines
#(docker image ls |grep -w none.*none |awk '{print $3}' |xargs docker rmi -f |cat -n |tail) || true
#test `docker builder ls |grep -E -v -e default -e ^NAME |wc -l` -gt 0 && docker builder prune -a -f 2>&1 |cat -n |tail || true

###
# Enforce Lithops version in this image
#pip uninstall --yes lithops || true
#pip install --upgrade lithops==$LT_VERSION

lithops runtime build -b k8s -f Dockerfile.lithops.github ${BASE_IMAGE}.int
#docker tag $MADE_IMAGE ${MADE_IMAGE}.lt-${LT_VERSION}
#docker push ${MADE_IMAGE}.lt-${LT_VERSION} 2>&1 |tail -5

###
# Build SCONE signed image
docker build --no-cache --progress plain --build-arg BASE_IMAGE=${BASE_IMAGE}.int --build-arg LT_VERSION=$LT_VERSION -f $DOCKERFILE -t $MADE_IMAGE .
docker push $MADE_IMAGE 2>&1 |tail -5

###
# Save a copy before Lithops final installation step
docker tag $MADE_IMAGE ${MADE_IMAGE}.sign
docker push ${MADE_IMAGE}.sign 2>&1 |tail -5


docker tag $BASE_IMAGE ${VNLA_IMAGE}
docker push ${VNLA_IMAGE} 2>&1 |tail -5

lithops runtime build -b k8s -f Dockerfile.lithops.github $VNLA_IMAGE
