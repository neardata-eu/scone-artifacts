#!/bin/bash

set -e

d_MESH="$1"

test "x$d_MESH" == "x" && {
    echo "..:INF: Usage: $0 < new directory >"
    exit 1
} || {
    test -d $d_MESH && {
        echo "..:WARN: Directory $d_MESH already exists. Copying manifests and scripts. Configuration in 'mesh.txt' will not be touched" 
        ls -ld $d_MESH
        test -f mesh.txt && {
            ls -ld mesh.txt
        } || {
            echo "..:WARN: File 'mesh.txt' is missing from the user-side. Copy manually a new base file from this directory into $d_MESH"
        }
        cp -pv run.sh portforward.sh pods.sh persistentVolumeClaimsMesh.yaml.template mesh.yaml.template logs.sh getcas.py exec.sh describe.sh deletepod.sh command.sh check_prerequisites.sh build_helpers.inc.sh $d_MESH/
    } || {
        mkdir -v $d_MESH || exit 2
        ls -ld $d_MESH
        cp -pv run.sh portforward.sh pods.sh persistentVolumeClaimsMesh.yaml.template mesh.yaml.template mesh.txt logs.sh getcas.py exec.sh describe.sh deletepod.sh command.sh check_prerequisites.sh build_helpers.inc.sh $d_MESH/
    }
}


