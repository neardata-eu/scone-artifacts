#!/usr/bin/env bash

set -e


export RED='\e[31m'
export BLUE='\e[34m'
export ORANGE='\e[33m'
export NC='\e[0m' # No Color

###
# comment these lines if you want colored log output
export RED=''
export BLUE=''
export ORANGE=''
export NC='' # No Color

###
# print an error message on an error exit
trap 'last_command=$current_command; current_command=$BASH_COMMAND; echo "..:DBG:executing $current_command"' DEBUG
trap 'if [ $? -ne 0 ]; then echo -e "${RED}\"${last_command}\" command failed - exiting.${NC}"; fi' EXIT

###
# display message and exit when error occurs
error_exit() {
  trap '' EXIT
  echo -e "${RED}$1${NC}" 
  exit 1
}


###
# * header helper file to place helper functions and environment variables
# - there is a "get_value()" function: `get_value VARIABLE CONFIGURATION_FILE`
#   that obtains a value from a configuration key=value file
# - there is an environment variable `f_MESH` pointing to mesh.txt
#   that is a configuration key=value file used to setup the mesh of services
source build_helpers.inc.sh

###
# * environment variables required by the configuration and deployment process
#   they can get values from parent terminal session
# - some of them may assume a default value or get it from the configuration file
#   specified in f_MESH (declared in header helper file)
# - in order to track changes, prefer to use the configuration file instead of
#   setting on terminal
# * NOTICE: the function get_value "VARIABLE" "CONFIGURATION_FILE" will fail if either
# there is no VARIABLE or if there is more than one of it
#
# * APP_NAMESPACE       - contains the CAS session name. should be obtained from file "relase.sh"
# * APP_IMAGE_REPO:     - repository where to push the images produced or to pull
# * SCONECTL_REPO:      - client image to execute SCONE related configurations
# * VERSION:            - version of SCONE libraries and images
# * SCONECTL_VERSION:   - version specifically for SCONECTL
# * RELEASE:            - prefix name to configure the mesh of services in the cluster
# * DEFAULT_NAMESPACE   - namespace on which the mesh of services will be configured
# * PVC_IDENTIFICATION  - resource identification for PVC
export APP_NAMESPACE=${APP_NAMESPACE:=""}
export APP_IMAGE_REPO=${APP_IMAGE_REPO:="$(get_value PUSH_IMAGE_REPO $f_MESH)"} # Must be defined!
export SCONECTL_REPO=${SCONECTL_REPO:="registry.scontain.com/sconectl"}
export VERSION=${VERSION:="5.8.0"}
export SCONECTL_VERSION=${SCONECTL_VERSION:="5.8.0"}
export RELEASE=${RELEASE:="$(get_value MESH_PREFIX $f_MESH)"}
export DEFAULT_NAMESPACE=${DEFAULT_NAMESPACE:="$(get_value CLUSTER_NAMESPACE $f_MESH)"}
export PVC_IDENTIFICATION=${PVC_IDENTIFICATION:="$(get_value PVC_IDENTIFICATION $f_MESH)"}


###
# setting ./run.sh parameters flags and other global variables
help_flag="--help"
ns_flag="--namespace"
verbose_flag="-v"
verbose=""
debug_flag="--debug"
debug_short_flag="-d"
debug=""
clean_flag="--clean"
clean=0
cas_location="--cas"
cas_source=""
cas_url=""
cas_key=""
cas_session_encryption_key=""
cas_mode=""
check_cas=0
keycloak_keystore=""
keycloak_client_keystore_password=""


ns="$DEFAULT_NAMESPACE"
repo="$APP_IMAGE_REPO"
release="${RELEASE:=keycloak}"


###
# help message
usage ()
{
  echo ""
  echo "Usage:"
  echo "    run.sh [$clean_flag] $cas_location <[ public | private | operator ]> [$verbose_flag] [$help_flag]"
  echo ""
  echo ""
  echo "Builds the application described in service.yaml.template and mesh.yaml.template and deploys"
  echo "it into your kubernetes cluster."
  echo ""
  echo "Options:"
  echo "    $clean_flag"
  echo "                  Deletes previous release.sh file and target/ directory"
  echo "                  A backup is kept in bkp_target/ directory"
  echo "    $cas_location   | cas location"
  echo "                  Can be 'public' or 'private'; details configured in file \"$f_MESH\""
  echo "    $verbose_flag"
  echo "                  Enable verbose output"
  echo "    $debug_flag | $debug_short_flag"
  echo "                  Create debug image instead of a production image"
  echo "    $help_flag"
  echo "                  Output this usage information and exit."
  echo ""
  echo "By default this uses the latest release of the SCONE Elements images. To use image from a different"
  echo "repository (e.g., a local cache), set SCONECTL_REPO to the repo you want to use instead."
  return
}


##### Parsing arguments

while [[ "$#" -gt 0 ]]; do
  case $1 in
    ${verbose_flag})
      verbose="-vvvvvvvv"
      shift # past argument
      ;;
    ${debug_flag} | ${debug_short_flag})
      debug="--mode=debug"
      shift # past argument
      ;;
    ${clean_flag})
      clean=1
      shift # past argument
      ;;
    ${cas_location})
      echo pos 1 $1
      echo pos 2 $2
      case $2 in
        public)
          cas_url="$(get_value PUB_CAS_URL $f_MESH)"
          cas_tolerance="$(get_value PUB_CAS_TOLERANCE $f_MESH)"
          check_cas=0
          cas_source=$2
          shift # past argument
          ;;
        private)
          cas_url="$(get_value PRIV_CAS_URL $f_MESH)"
          cas_namespace="$(get_value PRIV_CAS_NAMESPACE $f_MESH)"
          cas_key="$(get_value PRIV_CAS_KEY $f_MESH)"
          cas_tolerance="$(get_value PRIV_CAS_TOLERANCE $f_MESH)"
          cas_mode="$(get_value PRIV_CAS_MODE $f_MESH)"
          cas_session_encryption_key="$(get_value PRIV_CAS_SESSION_ENCRYPTION_KEY $f_MESH)"
          check_cas=1
          cas_source=$2
          shift # past argument
          ;;
        operator)
          cas_url="$(get_value OPER_CAS_URL $f_MESH)"
          cas_namespace="$(get_value OPER_CAS_NAMESPACE $f_MESH)"
          cas_key="$(get_value OPER_CAS_KEY $f_MESH)"
          cas_tolerance="$(get_value OPER_CAS_TOLERANCE $f_MESH)"
          cas_mode="$(get_value PRIV_CAS_MODE $f_MESH)"
          cas_session_encryption_key="$(get_value PRIV_CAS_SESSION_ENCRYPTION_KEY $f_MESH)"
          check_cas=1
          cas_source=$2
          shift # past argument
          ;;
        *)
          usage
          error_exit "Error: Unknown $cas_location passed: $2. It is either 'public', 'private' or 'operator'";
          ;;
      esac
      shift # past argument
      ;;
    $help_flag)
      usage
      exit 0
      ;;
    *)
      usage
      error_exit "Error: Unknown parameter passed: $1";
      ;;
  esac
done

if [ ! -n "${cas_url}" ]; then
    usage
    error_exit "..:ERR: $cas_location was not defined";
fi

if [ ! -n "${ns}" ]; then
    namespace_arg=""
else
    namespace_arg="${ns_flag} ${ns} "
fi


###
# preliminary checks
if [  "${RELEASE}" == "" ]; then
    usage
    error_exit  "Error: You must specify a release in configuration file '$f_MESH' using 'MESH_PREFIX' key."
fi

if [  "${repo}" == "" ]; then
    usage
    error_exit  "Error: You must specify a repository in configuration file '$f_MESH' using 'PUSH_IMAGE_REPO' key."
fi
export APP_IMAGE_REPO="${repo}"

sudo echo "..:INF:check sudo before continuing" || error_exit  "..:ERR: failed to run 'sudo'."

echo -e "${BLUE}Checking that we have access to the base container image${NC}"

docker inspect ${SCONECTL_REPO}/sconecli:latest > /dev/null 2> /dev/null || docker pull ${SCONECTL_REPO}/sconecli:latest > /dev/null 2> /dev/null || { 
    echo -e "${RED}You must get access to image '${SCONECTL_REPO}/sconecli:latest'.${NC}" 
    error_exit "Please send email info@scontain.com to ask for access"
}


###
# * maintain a backup copy of current configuration to rollback if necessary
#   sudo is necessary because sconectl sets directory owner to 'root'
# * rollback:
# ... - assert that no ./target/ is present
# ... - sudo cp -pRf bkp_target/target.%YYYYmmddHHMMSS%[.cleaned] ./target
# ... - mv ./target/release.sh ./
mkdir bkp_target 2>/dev/null || true
ls -ld bkp_target
if [ $clean -eq 1 ]; then
    d_sfx=`date '+%Y%m%d%H%M%S'`
    test -d target && sudo cp -pRf ./target bkp_target/target.$d_sfx.cleaned || true
    cp -pv release.sh bkp_target/target.$d_sfx.cleaned || true
    echo "Info: removing previous working files"
    sudo rm -rf release.sh target/
  else
    # gets current APP_NAMESPACE containing session name registered in CAS
    source release.sh 2>/dev/null || true # get release name
    d_sfx=`date '+%Y%m%d%H%M%S'`
    if [ -d ./target ]; then
      sudo cp -pRf ./target bkp_target/target.$d_sfx
      ls -ld bkp_target/target.$d_sfx
    fi
fi

if [ -z "$APP_NAMESPACE" ] ; then
    # stores new session name referred by APP_NAMESPACE to later retrival from release.sh
    export APP_NAMESPACE="$RELEASE-$RANDOM-$RANDOM"
    echo -e "export APP_NAMESPACE=$APP_NAMESPACE\n" >> release.sh
else 
    echo "CAS Namespace already defined: $APP_NAMESPACE"
fi
echo "Using APP_NAMESPACE is:$APP_NAMESPACE"


###
# Check to make sure all prerequisites are installed
export CAS=$cas_url
export CAS_NAMESPACE=$cas_namespace
a=0
if [ $check_cas -eq 1 ]; then
    while ! ./check_prerequisites.sh; do
        sleep 10;
        a=$[a+1];
        test $a -eq 10 && error_exit "..:ERR: failed to run ./check_prerequisites.sh" || true;
    done
fi

if [ "$cas_source" == "operator" ]; then
    source <(kubectl provision cas "$CAS" -n "${CAS_NAMESPACE:-default}" --print-public-keys || exit 1)
    echo "..:DBG:kubectl provision cas $CAS -n ${CAS_NAMESPACE:-default} --print-public-keys"
    kubectl provision cas "$CAS" -n "${CAS_NAMESPACE:-default}" --print-public-keys
    test $cas_key == $CAS_KEY && true || echo "..:WRN:CAS_KEY is different from the provided in configuration. Resetting to the freshest from CAS. old:$cas_key, new:$CAS_KEY" && cas_key="$CAS_KEY"
    test $cas_session_encryption_key == $CAS_SESSION_ENCRYPTION_KEY && true || echo "..:WRN:CAS_SESSION_ENCRYPTION_KEY is different from the provided in configuration. Resetting to the freshest from CAS. old:$cas_session_encryption_key new:$CAS_SESSION_ENCRYPTION_KEY" && cas_session_encryption_key="$CAS_SESSION_ENCRYPTION_KEY"
fi

if [ "$cas_source" == "private" ]; then
    set -x
    nohup kubectl port-forward service/$CAS 8081:8081 --namespace "${CAS_NAMESPACE}" --address=0.0.0.0 &
    sleep 5
    sconectl --quiet scone cas attest -CGS --only_for_testing-debug --only_for_testing-ignore-signer --only_for_testing-trust-any localhost
    sconectl scone cas list
    export CAS_KEY="$(sconectl --quiet scone cas show-identification --cas-key-hash localhost |grep -viE -e warning -e ^$)"
    export CAS_SOFTWARE_KEY="$(sconectl --quiet scone cas show-identification --cas-software-key-hash |grep -viE -e warning -e ^$)"
    kill `ps -ef |grep port-forward.*8081 |grep -v grep |awk '{print $2}'`
    REPORT=$(printf "`kubectl get cas $CAS -o json |jq .status.dcapReport`")
    REPORT=${REPORT:1:-1}
    export CAS_SESSION_ENCRYPTION_KEY="$(echo "$REPORT" | jq -r  ."additional_data"."non_critical"."session_encryption_key")"
    export CAS_CERT="$(echo "$REPORT" | jq  ."additional_data"."non_critical"."cert_chain" |tr -d '"' |tr -d ^$)"
    set +x
fi


###
# * applications and CAS configuration environment variables to put in 'mesh.yaml'
# * KC_VERSION:                         - Keycloak version
# * JAVA_VERSION:                       - Java version in Keycloak image
# * KEYCLOAK_KEYSTORE:                  - client keystore binary format to configure the secret in Keycloak's policy
# * KEYCLOAK_CLIENT_KEYSTORE_PASSWORD   - client keystore access password
# * KEYCLOAK_HTTP_PORT                  - insecure Keycloak client service port; often necessary for compatibility
# * KEYCLOAK_HTTPS_PORT                 - confidential Keycloak client service port
# * SFX_PKCS_SESSION                    - suffix to identify the auxiliary policy containing the database access credentials in PKCS#12 format
##

###
# CAS setup
export CAS_URL="cas_url: ${cas_url}.${cas_namespace}"
export CAS_KEY="cas_key: ${cas_key}"
export CAS_TOLERANCE="tolerance: ${cas_tolerance}"
export CAS_MODE="mode: ${cas_mode}"
export CAS_SESSION_ENCRYPTION_KEY="cas_encryption_key: ${cas_session_encryption_key}"

###
# Images
export MARIADB_IMAGE=$(get_value MARIADB_MESH_IMAGE $f_MESH)

export KEYCLOAK_IMAGE=$(get_value KEYCLOAK_MESH_IMAGE $f_MESH)
export KEYCLOAK_IMAGE_UNDERLINE=$(echo "$KEYCLOAK_IMAGE" |sed 's/\//_/g; s/:/_/g; s/-/_/g; s/\./_/g;')

export PKCS12_IMAGE=$(get_value PKCS12_MESH_IMAGE $f_MESH)

export MINIO_IMAGE=$(get_value MINIO_MESH_IMAGE $f_MESH)
export MINIO_IMAGE_UNDERLINE=$(echo "$MINIO_IMAGE" |sed 's/\//_/g; s/:/_/g; s/-/_/g; s/\./_/g;')

export LITHOPS_IMAGE=$(get_value LITHOPS_MESH_IMAGE $f_MESH)
export LITHOPS_IMAGE_UNDERLINE=$(echo "$LITHOPS_IMAGE" |sed 's/\//_/g; s/:/_/g; s/-/_/g; s/\./_/g;')

###
# Enclave hashes
export KEYCLOAK_SCONE_MIN_HEAP=$(get_value KEYCLOAK_SCONE_MIN_HEAP $f_MESH)
export KEYCLOAK_SCONE_HEAP=$(get_value KEYCLOAK_SCONE_HEAP $f_MESH)
export KEYCLOAK_SCONE_STACK=$(get_value KEYCLOAK_SCONE_STACK $f_MESH)
export KEYCLOAK_SCONE_LOG=ERROR
export KEYCLOAK_SCONE_EDMM_MODE=$(get_value KEYCLOAK_SCONE_EDMM_MODE $f_MESH)
export KEYCLOAK_HASH=123abc
if [ "$KEYCLOAK_SCONE_EDMM_MODE" == "enable" ]; then
    export KEYCLOAK_HASH=`docker run --rm -i -t --entrypoint bash --env SCONE_EDMM_HASH=1 --env SCONE_MIN_HEAP=$KEYCLOAK_SCONE_MIN_HEAP --env SCONE_HEAP=$KEYCLOAK_SCONE_HEAP --env SCONE_STACK=$KEYCLOAK_SCONE_STACK $KEYCLOAK_IMAGE -c "/usr/bin/java"`
else
    export KEYCLOAK_HASH=`docker run --rm -i -t --entrypoint bash --env SCONE_HASH=1 --env SCONE_MIN_HEAP=$KEYCLOAK_SCONE_MIN_HEAP --env SCONE_HEAP=$KEYCLOAK_SCONE_HEAP --env SCONE_STACK=$KEYCLOAK_SCONE_STACK $KEYCLOAK_IMAGE -c "/usr/bin/java"`
fi

export MINIO_SCONE_MIN_HEAP=$(get_value MINIO_SCONE_MIN_HEAP $f_MESH)
export MINIO_SCONE_HEAP=$(get_value MINIO_SCONE_HEAP $f_MESH)
export MINIO_SCONE_ALLOW_DLOPEN=$(get_value MINIO_SCONE_ALLOW_DLOPEN $f_MESH)
export MINIO_SCONE_LOG=ERROR
export MINIO_SCONE_EDMM_MODE=$(get_value MINIO_SCONE_EDMM_MODE $f_MESH)
export MINIO_SCONE_STACK=$(get_value MINIO_SCONE_STACK $f_MESH)
export MINIO_SCONE_FORK=$(get_value MINIO_SCONE_FORK $f_MESH)
export MINIO_SCONE_FORK_OS=$(get_value MINIO_SCONE_FORK_OS $f_MESH)
export MINIO_SCONE_SYSLIBS=$(get_value MINIO_SCONE_SYSLIBS $f_MESH)
export MINIO_HASH=123abc
export MINIO_SCONE_MODE=$(get_value MINIO_SCONE_MODE $f_MESH)
if [ "$MINIO_SCONE_EDMM_MODE" == "enable" ]; then
    export MINIO_HASH=`docker run --rm -i -t --entrypoint bash --env SCONE_EDMM_HASH=1 --env SCONE_MIN_HEAP=$MINIO_SCONE_MIN_HEAP --env SCONE_HEAP=$MINIO_SCONE_HEAP --env SCONE_STACK=$MINIO_SCONE_STACK --env SCONE_FORK=$MINIO_SCONE_FORK --env SCONE_FORK_OS=$MINIO_SCONE_FORK_OS --env SCONE_ALLOW_DLOPEN=$MINIO_SCONE_ALLOW_DLOPEN --env SCONE_SYSLIBS=$MINIO_SCONE_SYSLIBS $MINIO_IMAGE -c "/usr/bin/minio"`
else
    export MINIO_HASH=`docker run --rm -i -t --entrypoint bash --env SCONE_HASH=1 --env SCONE_MIN_HEAP=$MINIO_SCONE_MIN_HEAP --env SCONE_HEAP=$MINIO_SCONE_HEAP --env SCONE_STACK=$MINIO_SCONE_STACK --env SCONE_FORK=$MINIO_SCONE_FORK --env SCONE_FORK_OS=$MINIO_SCONE_FORK_OS --env SCONE_ALLOW_DLOPEN=$MINIO_SCONE_ALLOW_DLOPEN --env SCONE_SYSLIBS=$MINIO_SCONE_SYSLIBS $MINIO_IMAGE -c "/usr/bin/minio"`
fi

export LITHOPS_SCONE_MIN_HEAP=$(get_value LITHOPS_SCONE_MIN_HEAP $f_MESH)
export LITHOPS_SCONE_HEAP=$(get_value LITHOPS_SCONE_HEAP $f_MESH)
export LITHOPS_SCONE_ALLOW_DLOPEN=$(get_value LITHOPS_SCONE_ALLOW_DLOPEN $f_MESH)
export LITHOPS_SCONE_LOG=ERROR
export LITHOPS_SCONE_EDMM_MODE=$(get_value LITHOPS_SCONE_EDMM_MODE $f_MESH)
export LITHOPS_SCONE_STACK=$(get_value LITHOPS_SCONE_STACK $f_MESH)
export LITHOPS_SCONE_FORK=$(get_value LITHOPS_SCONE_FORK $f_MESH)
export LITHOPS_SCONE_FORK_OS=$(get_value LITHOPS_SCONE_FORK_OS $f_MESH)
export LITHOPS_SCONE_SYSLIBS=$(get_value LITHOPS_SCONE_SYSLIBS $f_MESH)
export LITHOPS_HASH=123abc
export LITHOPS_SCONE_MODE=$(get_value LITHOPS_SCONE_MODE $f_MESH)
if [ "$LITHOPS_SCONE_EDMM_MODE" == "enable" ]; then
    export LITHOPS_HASH=`docker run --rm -i -t --entrypoint bash --env SCONE_EDMM_HASH=1 --env SCONE_MIN_HEAP=$LITHOPS_SCONE_MIN_HEAP --env SCONE_HEAP=$LITHOPS_SCONE_HEAP --env SCONE_STACK=$LITHOPS_SCONE_STACK --env SCONE_FORK=$LITHOPS_SCONE_FORK --env SCONE_FORK_OS=$LITHOPS_SCONE_FORK_OS --env SCONE_ALLOW_DLOPEN=$LITHOPS_SCONE_ALLOW_DLOPEN --env SCONE_SYSLIBS=$LITHOPS_SCONE_SYSLIBS $LITHOPS_IMAGE -c "/usr/local/bin/python3.13"`
else
    export LITHOPS_HASH=`docker run --rm -i -t --entrypoint bash --env SCONE_HASH=1 --env SCONE_MIN_HEAP=$LITHOPS_SCONE_MIN_HEAP --env SCONE_HEAP=$LITHOPS_SCONE_HEAP --env SCONE_STACK=$LITHOPS_SCONE_STACK --env SCONE_FORK=$LITHOPS_SCONE_FORK --env SCONE_FORK_OS=$LITHOPS_SCONE_FORK_OS --env SCONE_ALLOW_DLOPEN=$LITHOPS_SCONE_ALLOW_DLOPEN --env SCONE_SYSLIBS=$LITHOPS_SCONE_SYSLIBS $LITHOPS_IMAGE -c "/usr/local/bin/python3.13"`
fi

###
# Hostnames and network settings
export DOMAIN_NAME=$(get_value DNS_DOMAIN $f_MESH)
export KEYCLOAK_FQDN_HOSTNAME="$(get_value KEYCLOAK_HOSTNAME $f_MESH).$DOMAIN_NAME"
export MINIO_FQDN_HOSTNAME="$(get_value MINIO_HOSTNAME $f_MESH).$DOMAIN_NAME"
export LITHOPS_FQDN_HOSTNAME="$(get_value LITHOPS_HOSTNAME $f_MESH).$DOMAIN_NAME"

export MARIADB_CONTAINER_NAME="${RELEASE}-$(get_value MARIADB_HOSTNAME $f_MESH)"
export KEYCLOAK_CONTAINER_NAME="${RELEASE}-$(get_value KEYCLOAK_HOSTNAME $f_MESH)"
export MINIO_CONTAINER_NAME="${RELEASE}-$(get_value MINIO_HOSTNAME $f_MESH)"
export LITHOPS_CONTAINER_NAME="${RELEASE}-$(get_value LITHOPS_HOSTNAME $f_MESH)"

export MARIADB_SERVICE_NAME="$(get_value MARIADB_HOSTNAME $f_MESH)"
export KEYCLOAK_SERVICE_NAME="$(get_value KEYCLOAK_HOSTNAME $f_MESH)"
export MINIO_SERVICE_NAME="$(get_value MINIO_HOSTNAME $f_MESH)"
export LITHOPS_SERVICE_NAME="$(get_value LITHOPS_HOSTNAME $f_MESH)"

###
# Keycloak settings
export KC_VERSION=$(get_value KC_VERSION $f_MESH)
export JAVA_VERSION=$(get_value JAVA_VERSION $f_MESH)
export KEYCLOAK_ADDITIONAL_PARAMS=$(get_value KEYCLOAK_ADDITIONAL_PARAMS $f_MESH)
export KEYCLOAK_HTTP_PORT=$(get_value KEYCLOAK_HTTP_PORT $f_MESH)
export KEYCLOAK_HTTPS_PORT=$(get_value KEYCLOAK_HTTPS_PORT $f_MESH)
export KEYCLOAK_JAVA_XMS=$(get_value KEYCLOAK_JAVA_XMS $f_MESH)
export KEYCLOAK_JAVA_XMX=$(get_value KEYCLOAK_JAVA_XMX $f_MESH)
export KEYCLOAK_JAVA_META=$(get_value KEYCLOAK_JAVA_METASPACESIZE $f_MESH)
export KEYCLOAK_JAVA_MAXMETA=$(get_value KEYCLOAK_JAVA_MAXMETASPACESIZE $f_MESH)
export KEYCLOAK_ADMIN_USERNAME=$(get_value KEYCLOAK_ADMIN_USERNAME $f_MESH)
export KEYCLOAK_ADMIN_PASSWORD=$(get_value KEYCLOAK_ADMIN_PASSWORD $f_MESH)
export KEYCLOAK_DB_MANAGER=$(get_value KEYCLOAK_DB_MANAGER $f_MESH)
export SFX_PKCS_SESSION=$(get_value SUFIX_PKCS12_SESSION $f_MESH)

###
# minIO settings
export MINIO_SERVICE_PORT=$(get_value MINIO_SERVICE_PORT $f_MESH)
export MINIO_CONSOLE_PORT=$(get_value MINIO_CONSOLE_PORT $f_MESH)
export MINIO_SERVICE_ADDRESS=$(get_value MINIO_SERVICE_ADDRESS $f_MESH)
export MINIO_CONSOLE_ADDRESS=$(get_value MINIO_CONSOLE_ADDRESS $f_MESH)

###
# Lithops settings
export LITHOPS_PYTHON_GIL=$(get_value LITHOPS_PYTHON_GIL $f_MESH)
export LITHOPS_CLUSTER_REPLICAS=$(get_value LITHOPS_CLUSTER_REPLICAS $f_MESH)
export LITHOPS_REQUESTS_MEMORY=$(get_value LITHOPS_REQUESTS_MEMORY $f_MESH)
export LITHOPS_REQUESTS_CPU=$(get_value LITHOPS_REQUESTS_CPU $f_MESH)
export LITHOPS_LIMITS_MEMORY=$(get_value LITHOPS_LIMITS_MEMORY $f_MESH)
export LITHOPS_LIMITS_CPU=$(get_value LITHOPS_LIMITS_CPU $f_MESH)
export LITHOPS_RABBITMQ_USER=$(get_value LITHOPS_RABBITMQ_USER $f_MESH)
export LITHOPS_RABBITMQ_PASSWORD=$(get_value LITHOPS_RABBITMQ_PASSWORD $f_MESH)
export LITHOPS_RABBITMQ_ADDRESS=$(get_value LITHOPS_RABBITMQ_ADDRESS $f_MESH)
export LITHOPS_RABBITMQ_URL=$(get_value LITHOPS_RABBITMQ_URL $f_MESH)


echo -e "${BLUE}build application and pushing policies:${NC} apply -f mesh.yaml"
echo -e "${BLUE}  - this fails, if you do not have access to the SCONE CAS namespace"
echo -e "  - update the namespace '${ORANGE}policy.namespace${NC}' to a unique name in '${ORANGE}mesh.yaml${NC}'"

###
# Storage setup
envsubst < persistentVolumeClaimsMesh.yaml.template > persistentVolumeClaimsMesh.yaml
kubectl apply -f persistentVolumeClaimsMesh.yaml

export RND=$RANDOM
SCONE="\$SCONE" envsubst < mesh.yaml.template > mesh.yaml

sconectl apply --cas-config $HOME/.cas -f mesh.yaml --set-version "$VERSION" --release "$RELEASE" $verbose $debug

echo -e "${BLUE}Executing a 'dry-run' simulated installation to verify for errors before proceding${NC}"

###
# * test the validity of the manifests produced before unistalling current configuration
helm upgrade --dry-run --install $namespace_arg ${release} target/helm/ >/dev/null || false

echo -e "${BLUE}Uninstalling application in case it was previously installed:${NC} helm uninstall ${namespace_arg} ${RELEASE}"
echo -e "${BLUE} - this requires that 'kubectl' gives access to a Kubernetes cluster${NC}"

helm uninstall $namespace_arg ${release} 2> /dev/null || true

echo -e "${BLUE}install application:${NC} helm install ${namespace_arg} ${RELEASE} target/helm/"

helm install $namespace_arg ${release} target/helm/ || \
helm upgrade $namespace_arg --install ${release} target/helm/ 

echo -e "${BLUE}Check the logs by executing:${NC} kubectl logs ${namespace_arg} ${RELEASE}<TAB>"
echo -e "${BLUE}Uninstall by executing:${NC} helm uninstall ${namespace_arg} ${RELEASE}"

echo -e "${BLUE}Getting Keycloak CA certificate to import into your system:${NC}"
kubectl port-forward service/$CAS 8081:8081 --namespace "${CAS_NAMESPACE}" --address=0.0.0.0 &
sleep 1
python3 getcas.py 127.0.0.1 $APP_NAMESPACE/secrets Keycloak_CA_Cert
kill `ps -ef |grep port-forward.*8081 |grep -v grep |awk '{print $2}'`

echo FINISHED
echo -e "${BLUE}Check the logs by executing:${NC} kubectl logs ${namespace_arg}"
echo -e "${BLUE}Uninstall by executing:${NC} helm uninstall ${RELEASE}"

