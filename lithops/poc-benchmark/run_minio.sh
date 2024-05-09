#!/bin/bash

MINIO_ROOT_USER=${MINIO_ROOT_USER:=minioroot}
MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD:=n34r6a7a}

docker run -d --name miniostorage -i -t -p 9000:9000 -p 9001:9001 -p 9090:9090 --add-host host.docker.internal:host-gateway --env MINIO_ROOT_USER="$MINIO_ROOT_USER" --env MINIO_ROOT_PASSWORD="$MINIO_ROOT_PASSWORD" minio/minio:la test server /data --console-address ":9001"
