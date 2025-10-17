# Description of _mesh.txt_

* **PUB_CAS_***
	- Public demonstration CAS setup. Parameter "**_--cas public_**" in **`run.sh`**
* **PUB_CAS_URL**
	- FQDN CAS address
* **PUB_CAS_TOLERANCE**
	- Tolerance parameters for that CAS installation to be trusted.
	- Can be "_--only_for_testing-trust-any --only_for_testing-debug  --only_for_testing-ignore-signer -C -G -S_"

* **PRIV_CAS_***
	- Private CAS setup. Parameter "**_--cas private_**" in **`run.sh`**
* **PRIV_CAS_NAMESPACE**
	- Kubernetes namespace where CAS is installed
	- Works as domain name, in conjunction with `PRIV_CAS_URL`
* **PRIV_CAS_URL**
	- Hostname
* **PRIV_CAS_KEY**
	- CAS installation credentials to be trusted
	- Obtained from CAS's log
* **PRIV_CAS_TOLERANCE**
	- Tolerance parameters for that CAS installation to be trusted

* **OPER_CAS_***
	- SCONE Operator CAS setup. Parameter "**_--cas operator_**" in **`run.sh`**
* **OPER_CAS_NAMESPACE**
	- Kubernetes namespace where CAS is installed
	- Works as domain name, in conjunction with `OPER_CAS_URL`
* **OPER_CAS_URL**
	- Hostname
* **OPER_CAS_KEY**
	- CAS installation credentials to be trusted
	- Obtained from CAS's log
* **OPER_CAS_TOLERANCE**
	- Tolerance parameters for that CAS installation to be trusted

* **PRIV_CAS_MODE**
	- How policies and manifests are saved in the cluster, to protect from interference
	- Can be either _SignedManifest_, or _EncryptedManifest_
* **PRIV_CAS_SESSION_ENCRYPTION_KEY**
	- Cryptographic key for signing or encrypting
* Both **PRIV_CAS_MODE** and **PRIV_CAS_SESSION_ENCRYPTION_KEY** are available to both "private" and "operator" installations

---------
* **CLUSTER_NAMESPACE**
	- Namespace where services are installed
	- If the '_default_' namespace is being used, it has to be explicitly defined
* **PVC_IDENTIFICATION**
	- The PVC identification refers to specific means to differentiate from others, especially when there is more than one mesh of the same services deployed in the same cluster namespace
* **MESH_PREFIX**
	- Prefix composing the Pods names

---------
* **PUSH_IMAGE_REPO**
	- Used when an image is produced on runtime by SCONECTL

---------
* **MARIADB_MESH_IMAGE**
	- Database service image supporting Keycloak

---------
* **MINIO_MESH_IMAGE**
	- Cloud storage service image
* **MINIO_SCONE_MIN_HEAP**
	- SCONE minimum heap when EDMM support is available
* **MINIO_SCONE_HEAP**
	- SCONE enclave total memory. Currently, 7G
* **MINIO_SCONE_STACK**
	- SCONE enclave stack memory. Currently, 8M
* **MINIO_SCONE_EDMM_MODE**
	- Memory mechanics when EDMM support is available
* **MINIO_SCONE_ALLOW_DLOPEN**
	- Dynamically linked libraries. Possible values: 0, 1, or 2. Prefer using **1**
* **MINIO_SERVICE_PORT**
	- Application listening for requests on port. Default, 9000
* **MINIO_CONSOLE_PORT**
	- Application administration console on port. Default, 9001
* **MINIO_SERVICE_ADDRESS**
	- Application listening for requests on address and port. Default, :9000
	- Note the "**:**" has to be written. If all IP's or names are to be used, left-hand side is blank
* **MINIO_CONSOLE_ADDRESS**
	- Application administration console on address and port. Default, :9001
	- Note the "**:**" has to be written. If all IP's or names are to be used, left-hand side is blank

---------
* **JAVA_VERSION**
	- Java installation. Currently, 21
* **KEYCLOAK_MESH_IMAGE**
	- Identity and access manager application image
* **PKCS12_MESH_IMAGE**
	- Python image of Keycloak's initialization container
	- Used to create PKCS-12 credentials for database access
* **KC_VERSION**
	- Keycloak version
* **KEYCLOAK_ADMIN_USERNAME**
	- Administrative temporary user
* **KEYCLOAK_ADMIN_PASSWORD**
	- Administrative temporary password
* **KEYCLOAK_DB_MANAGER**
	- Database vendor
* **KEYCLOAK_HTTP_PORT**
	- Insecure Keycloak client service port; often necessary for compatibility and only used from localhost
	- Can be disabled
* **KEYCLOAK_HTTPS_PORT**
	- confidential Keycloak client service port
* **SUFIX_PKCS12_SESSION**
	- Suffix to identify the auxiliary policy containing the database access credentials in PKCS#12 format
* **KEYCLOAK_ADDITIONAL_PARAMS**
	Additional command-line parameters to load the applicatin. If, for example, you want to enable "Passkeys" support, you have to set both "_--features=preview --features=passkeys_"
* **KEYCLOAK_JAVA_XMS**
	- JVM memory parameter -Xms
* **KEYCLOAK_JAVA_XMX**
	- JVM memory parameter -Xmx
* **KEYCLOAK_JAVA_METASPACESIZE**
	- JVM classes metadata parameter -XX:MetaspaceSize
* **KEYCLOAK_JAVA_MAXMETASPACESIZE**
	- JVM classes metadata parameter -XX:MaxMetaspaceSize
* **KEYCLOAK_SCONE_MIN_HEAP**
	- SCONE minimum heap when EDMM support is available
* **KEYCLOAK_SCONE_HEAP**
	- SCONE enclave total memory. Currently, 12G
* **KEYCLOAK_SCONE_STACK**
	- SCONE enclave stack memory. Currently, 8M
* **KEYCLOAK_SCONE_EDMM_MODE**
	- Memory mechanics when EDMM support is available

---------
* **LITHOPS_MESH_IMAGE**
	- Function as a Service application image
* **LITHOPS_CLUSTER_REPLICAS**
	- Number of standing Pod replicas
* **LITHOPS_REQUESTS_MEMORY**
	- Initial memory reserved for the Pod
* **LITHOPS_REQUESTS_CPU**
	- Initial memory reserved for the Pod
* **LITHOPS_LIMITS_MEMORY**
	- Limit memory reserved for the Pod
* **LITHOPS_LIMITS_CPU**
	- Limit memory reserved for the Pod
* **LITHOPS_SCONE_LOG**
	- SCONE_LOG parameter
* **LITHOPS_PYTHON_GIL**
	- Disable/Enable GIL support. Currently, 0
* **LITHOPS_SCONE_HEAP**
	- SCONE enclave total memory. Currently, 7G
* **LITHOPS_SCONE_STACK**
	- SCONE enclave stack memory. Currently, 8M
* **LITHOPS_SCONE_MODE**
	- SCONE_MODE to run the application. Values are HW, to use TEE, or SIM, simulation
* **LITHOPS_SCONE_MIN_HEAP**
	- SCONE minimum heap when EDMM support is available
* **LITHOPS_SCONE_EDMM_MODE**
	- Memory mechanics when EDMM support is available
* **LITHOPS_SCONE_FORK**
	- Disable/Enable `fork()` system call support in SCONE. Currently, 1
* **LITHOPS_SCONE_FORK_OS**
	- Disable/Enable `fork()` system call optimization in Simulation mode in SCONE. Currently, 1
* **LITHOPS_SCONE_ALLOW_DLOPEN**
	- Dynamically linked libraries. Possible values: 0, 1, or 2. Prefer using **1**
* **LITHOPS_SCONE_SYSLIBS**
	- Allow the application to use system libraries. Currently, 1
* **LITHOPS_RABBITMQ_USER**
	- RabbitMQ application user
* **LITHOPS_RABBITMQ_PASSWORD**
	- RabbitMQ application password
* **LITHOPS_RABBITMQ_ADDRESS**
	- RabbitMQ messaging server address
* **LITHOPS_RABBITMQ_URL**
	- Queue URL

---------
* **DNS_DOMAIN**
	- DNS suffix to be accessible by the services and external users
* **MARIADB_HOSTNAME**
	- Database hostname.
* **KEYCLOAK_HOSTNAME**
	- Identity and access manager hostname
* **MINIO_HOSTNAME**
	- Cloud object storage hostname
* **LITHOPS_HOSTNAME**
	- Function as a Service hostname
