#!/bin/bash

source build_helpers.inc.sh

NS=$1
CT=$2
PT=$3

if [ ${#PT} -eq 0 ]; then NS=""; CT=$1; PT=$2; fi

NS=${NS:="$(get_value CLUSTER_NAMESPACE $f_MESH)"}
MS=${MS:="$(get_value MESH_PREFIX $f_MESH)"}

if [ -z "$MS" ]; then echo "..:ERR:must specify the mesh prefix"; exit 1; fi
if [ -z "$CT" ]; then echo "..:ERR:specify one container of: `kubectl get pods -n $NS |grep -w $MS |awk '{split($1,a,"-"); printf a[2] " "} END{print ""}'`"; exit 1; fi

set -x
nohup kubectl port-forward -n $NS --address 0.0.0.0 $(kubectl get pods -n $NS -o name |grep -w $MS-$CT) $PT:$PT &
