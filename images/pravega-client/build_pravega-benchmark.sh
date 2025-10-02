#!/bin/bash

echo "..:INF: Usage: [ TARGET_IMAGE=organizationaldocker/pravega:client ] $0 [ push ] # argument "push" will push the generated image to the \$TARGET_IMAGE"

set -eux

PUSH=0

TARGET_IMAGE=${TARGET_IMAGE:=yourdockerrepository/pravega:rust-benchmark-5.9.0-rc.7}
DOCKERFILE=Dockerfile.benchmark

docker build --progress plain -f $DOCKERFILE -t $TARGET_IMAGE .

if [[ "x$2" == "xpush" ]]; then
    PUSH=1
fi

###
if [ $PUSH -eq 1 ]; then
    docker push $TARGET_IMAGE 2>&1 |tail -5
fi
