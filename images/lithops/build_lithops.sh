#!/bin/bash

echo "..:INF: Usage: [ TARGET_IMAGE=organizationaldocker/lithops:version ] $0 [ push ] # argument "push" will push the generated image to the \$TARGET_IMAGE"

set -eux

PUSH=0

TARGET_IMAGE=${TARGET_IMAGE:=yourdockerrepository/lithops:3.6.1-singularity-python3.13t-5.9.0}
DOCKERFILE=Dockerfile

docker build --progress plain -f $DOCKERFILE -t $TARGET_IMAGE .

if [[ "x$2" == "xpush" ]]; then
    PUSH=1
fi

###
# tagging for SCONECTL
REPO=${TARGET_IMAGE%%:*}
TAG=${TARGET_IMAGE#*:}
DEBUG1=${REPO}:${TAG}_debug_latest
DEBUG2=${REPO}:debug_${TAG}

docker tag $TARGET_IMAGE $DEBUG1
docker tag $TARGET_IMAGE $DEBUG2
if [ $PUSH -eq 1 ]; then
    docker push $TARGET_IMAGE 2>&1 |tail -5
    docker push $DEBUG1 2>&1  |tail -5
    docker push $DEBUG2 2>&1 |tail -5
fi
