# Confidential Mesh of Services
Here you will find how to setup and deploy a confidential mesh of services in a Kubernetes cluster.
The nodes must have support to **[TEE](https://sconedocs.github.io/glossary/#tee "Trusted Execution Environment")**.

> ### Obtaining access to systems
> You will need access to SCONE Docker images registry.
Get access [here](https://sconedocs.github.io/registry/ "SCONE access").

---------
## Installation of the confidential computation baseline
We are using SCONE Operator to administer the attestation systems lifecycle (LAS, CAS, and SGX Plugin).

The applications are administered with SCONECTL Client.

### SCONE Operator
The SCONE Operator installation, also called "reconciliation", 
installation program will deploy 
**[LAS](https://sconedocs.github.io/LASIntro/ "LAS for Development and Production")** and 
**[SGX Plugin](https://sconedocs.github.io/helm_sgxdevplugin/ "Kubernetes SGX Plugin (sgxdevplugin)")** 
into the 
**[Kubernetes](https://sconedocs.github.io/k8s_concepts/ "SCONE and Kubernetes")** cluster, together with the `kubectl provision` client plugin, used to administer the cluster confidential systems.

Very briefly, this is the command to install the SCONE Operator:
```bash
export VERSION=latest # SCONE version of your choice, e.g. 5.8.0, 5.9.0, 6.0.0 etc.
curl -fsSL https://raw.githubusercontent.com/scontain/SH/master/$VERSION/operator_controller | bash -s - --reconcile --update --plugin --verbose --dcap-api "$DCAP_KEY" --secret-operator  --username $REGISTRY_USERNAME --access-token $REGISTRY_ACCESS_TOKEN --email $REGISTRY_EMAIL

```

Refer to the complete set of instructions [here](https://sconedocs.github.io/2_operator_installation/ "Deploying & Reconciling the SCONE Operator").


### SCONECTL Client
**[SCONECTL](https://sconedocs.github.io/sconectl/ "SCONECTL")** is a command line interface program installed in the administrator's workstation.

Services are setup in Meshfiles YAML manifests, with a complete set of features to convert cloud-native applications into cloud-confidential applications, or deploy already ported applications to SCONE.

Refer to **[here](https://sconedocs.github.io/install_sconectl/ "Installing sconectl")** for a complete set of instructions regarding installation and dependencies.


## Mesh configuration

### Core configuration file
There are too many settings and they are placed in a **bash-like** configuration file called **`mesh.txt`**. The values are set in a **`key=value`** fashion.

SCONECTL will deploy into the cluster the services described in a file named `mesh.yaml`, that is built from [**`mesh.yaml.template`**](./mesh.yaml.template "mesh.yaml.template") using the configurations from [**`mesh.txt`**](./mesh.txt "mesh.txt").
Some settings will compose the attestation policies.
For example:
```bash
PRIV_CAS_NAMESPACE=default
PRIV_CAS_URL=neardata-cas-v1
...
CLUSTER_NAMESPACE=default
PVC_IDENTIFICATION=storage-abc
MESH_PREFIX=services-corp
...
MINIO_SCONE_MIN_HEAP=50M
MINIO_SCONE_HEAP=7G
MINIO_SCONE_STACK=8M
...
KEYCLOAK_ADDITIONAL_PARAMS=--features=preview --features=passkeys
KEYCLOAK_JAVA_XMS=256m
KEYCLOAK_JAVA_XMX=2048m
KEYCLOAK_JAVA_METASPACESIZE=96M
KEYCLOAK_JAVA_MAXMETASPACESIZE=256m
```

Everything after '**`=`**' is a value; no need to add double-quote '**`"`**' to denote string, unless the '**`"`**' is to be considered a value too.

## Services installation

### Fresh start or artifacts update
You can execute the script [**`new_mesh.sh`**](./new_mesh.sh "new_mesh.sh"), it will copy the configuration standard artifacts to the directory specified (created if not present). Example:
```bash
./new_mesh.sh genomics_mesh
```

Once the `mesh.txt` is already there, it will not overwrite it, thus keeping the current configuration.

### Services deployment
Once you had finished the configuration in `mesh.txt`, you can execute the [**`run.sh`**](./run.sh "run.sh") shell script. It will generate a `mesh.yaml` file to be installed by `sconectl`. All configurations are saved in the subdirectory `./target`. If there is a configuration deployed, the current `./target` directory will be moved to `./bkp_target/*` with its timestamp.
Example:
```bash
./run.sh [--clean] --cas [operator | private | public]
```

The configurations will read from the current `./target` if there is one and modify accordingly.
The parameter **`--clean`** will backup the present `./target` and create a brand new installation.

The parameter **`--cas`** accepts one of three values: **`operator`**, if the CAS was installed with SCONE Operator; **`private`**, if you are using a CAS installed in a standalone Docker or in a Docker Compose; and **`public`**, if you are using one of our public demonstration CAS servers.

There are other handy shell scripts to aid the services administration in the cluster. For example: `./pods.sh` brings the `kubectl get pods` from the mesh's namespace; similarly with `./describe.sh`, `logs.sh` and so on.

