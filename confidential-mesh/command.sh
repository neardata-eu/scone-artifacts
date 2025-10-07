#!/bin/bash

source build_helpers.inc.sh

CT=$1

if [ -z "$CT" ]; then NS=""; CT=${CT:=$1}; MS=${MS:=$2}; fi

NS=${NS:="$(get_value CLUSTER_NAMESPACE $f_MESH)"}
MS=${MS:="$(get_value MESH_PREFIX $f_MESH)"}

if [ -z "$MS" ]; then echo "..:ERR:must specify the mesh prefix"; exit 1; fi
if [ -z "$CT" ]; then echo "..:ERR:specify one container of: `kubectl get pods -n $NS |grep -w $MS |awk '{split($1,a,"-"); printf a[2] " "} END{print ""}'`"; exit 1; fi

kubectl exec -n $NS -i -t `kubectl get pods -n $NS -o name |grep -w $MS-$CT` -- bash -c "${@: -1}"
