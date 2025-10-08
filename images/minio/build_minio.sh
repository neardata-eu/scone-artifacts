#!/bin/bash

echo "..:INF: Usage: [ TARGET_IMAGE=organizationaldocker/minio:version ] $0 [ push ] # argument "push" will push the generated image to the \$TARGET_IMAGE"

set -ex

PUSH=0

TARGET_IMAGE=${TARGET_IMAGE:=yourdockerrepository/minio:master-head-scone-5.9.0}
DOCKERFILE=Dockerfile

docker build --progress plain -f $DOCKERFILE -t $TARGET_IMAGE .

if [[ "x$1" == "xpush" ]]; then
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

echo "
..:INF: you can inject credentials and other environment variables via attestation
.. for example:
MINIO_ROOT_USER=minioroot
MINIO_ROOT_PASSWORD=.........

.. the other MINIO_* environment variables are default to the system (as seen from the official image minio/minio:latest) and embedded in this base image.
.. however, they should be injected via attestation as well:
PATH=/go/bin:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MC_CONFIG_DIR=/tmp/.mc
MINIO_ACCESS_KEY_FILE=access_key
MINIO_SECRET_KEY_FILE=secret_key
MINIO_ROOT_USER_FILE=access_key
MINIO_ROOT_PASSWORD_FILE=secret_key
MINIO_KMS_SECRET_KEY_FILE=kms_master_key
MINIO_UPDATE_MINISIGN_PUBKEY=RWTx5Zr1tiHQLwG9keckT0c45M3AGeHD6IvimQHpyRywVWGbP1aVSGav
MINIO_CONFIG_ENV_FILE=config.env"
