#!/bin/bash

IMAGE=registry.scontain.com/amiguel/neardatapublic/lithops:alpine_python310-scone-lithops301

CONTAINERNAME=lithopsclientalpinesco

LITHOPSCONFIG=_etc_lithops_config--scone.txt

KUBECONFIG=_root_kube_config.txt

BENCHMARK=benchmark.py

RUN=run.sh
ENV=env.sh

docker run -d --name $CONTAINERNAME -i -t --add-host host.docker.internal:host-gateway -v $PWD/$LITHOPSCONFIG:/etc/lithops/config -v $PWD/$KUBECONFIG:/root/.kube/config -v $PWD/$BENCHMARK:/python/benchmark.py -v $PWD/$ENV:/python/env.sh -v $PWD/$RUN:/python/run.sh --device /dev/sgx_enclave:/dev/sgx_enclave --device /dev/sgx_provision:/dev/sgx_provision --entrypoint bash $IMAGE
