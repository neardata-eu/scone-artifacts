# Demonstration programs

Here you will find programs and configurations that can be used with the sconified applications. Some of them might have been already shipped with the images when built.

## Lithops
For Lithops only executions, in mode `backend: localhost`, you can execute them straightforwardly.
If you use another backend (like `singularity` or `k8s`), you need the `.lithops_config` in the same working directory the program is.

* hellolithops.py
* multiprocessinglithops.py
* storagelithops.py
* storageoslithops.py
* .lithops_config


## Metaspace
For Metaspace with Lithops as engine, you don't need `.lithops_config`; instead, the files `ds-config*.json` and `sm-config*.json`.

* test-local.py
* test-singularity.py
* process-payload.py
* ds-config-local.json
* sm-config-local.json
* sm-config-singularity
* mol_db1.tsv

## Keycloak
* kc-client-injection.py
* kc-multiprocessinglithops.py
* kc-uc-code-injection-automated.py
* kc-uc-code-injection-browser.py

## x509 credentials
You may need x509 certificate and private key to perform some tasks. Here is how to generate them:
```bash
export NEARDATACLICERTSUBJ="/C=EU/ST=ES/L=Tarragona/O=NEARDATA/OU=Use Cases/CN=Genomics"
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes -subj "$NEARDATACLICERTSUBJ"
```