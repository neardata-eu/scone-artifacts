#!/bin/bash

source build_helpers.inc.sh

NS=$1

NS=${NS:="$(get_value CLUSTER_NAMESPACE $f_MESH)"}
NS=${NS:=default}

echo "..:INF:pods from namespace $NS"
kubectl get pods -n $NS
