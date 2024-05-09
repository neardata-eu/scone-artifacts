# Lithops benchmark

### Obtaining access to systems
You will need access to SCONE Docker images

- registry.scontain.com/scone.cloud/cas:latest


Get access [here](https://sconedocs.github.io/registry/ "SCONE access").

## Installation

### LAS and CAS setup

LAS and CAS will have their service ports exported to avail themselves to the host system.
LAS has **18766** and CAS has **8081** and **18765**

#### Preparation:

`cd lascas/`
<br>
`mkdir cas_files-5.8.0`
<br>
`cp cas_files-5.8.0.kio/cas.toml cas_files-5.8.0.kio/cas-default-owner-config.toml cas_files-5.8.0/`

#### Installation and ownership:

`docker run -v $PWD/cas_files-5.8.0:/etc/cas -it --network host --rm --device /dev/sgx_enclave  --device /dev/sgx_provision  registry.scontain.com/scone.cloud/cas sh -c "set -m ; cd /etc/cas; export SCONE_LAS_ADDR=127.0.0.1:18766 ;  cas provision --owner-config /etc/cas/cas-default-owner-config.toml "`

Hit Ctrl+C to end it

Load the systems:

`docker-compose up -d`
<br>
`docker-compose ps`

---

### Redis

#### Install in Kubernetes cluster

`kubectl apply -f k8s-redis--deployment-dev.yaml -f k8s-redis--service-dev.yaml`
<br>
`kubectl logs services/redis |less`

#### Forward access to service

`nohup kubectl port-forward --address 0.0.0.0 services/redis 6379:6379 &`

---

### minIO

#### Install standalone container

`docker run -d --name miniostorage -i -t -p 9000:9000 -p 9001:9001 -p 9090:9090 --add-host host.docker.internal:host-gateway --env MINIO_ROOT_USER=minioroot --env MINIO_ROOT_PASSWORD=n34r6a7a minio/minio:latest server /data --console-address ":9001"`

#### Configure cloud storage

`docker exec -i -t miniostorage bash`

Execute inside the container

`mc alias set 'myminio' 'http://172.20.0.2:9000' 'minioroot' 'n34r6a7a'`
<br>
`mc admin user add myminio scone myscone123`
<br>
`mc admin group add myminio sconegroup scone`
<br>
`mc admin policy attach myminio readwrite --group sconegroup`

Test the user:

`pwd`
<br>
`mc alias set 'sconeminio' 'http://172.20.0.2:9000' 'scone' 'myscone123'`
<br>
`mc mb sconeminio/mybucket`
<br>
`ls -l /data/`
<br>
`echo 123 >scrap.txt`
<br>
`mc cp scrap.txt sconeminio/mybucket`
<br>
`mc ls sconeminio/mybucket`
<br>
`ls -l /data/mybucket/`

You may want to remove the administrator-level alias from list before executing the commands above: `mc alias remove myminio`; and also remove the user-level alias after: `mc alias remove sconeminio`

Naturally, the **`ls`** commands are not necessary, but a simple way to show that the cloud storage server persisted the files in disk

---

### Lithops

#### Prepare configuration

Lithops will be executed in two Docker Images: _Vanilla_, with regular Python, and _SCONE_, with "sconified" Python

Some configuration files are injected into the containers started, with some of them shared between them

- ./_etc_lithops_config--vanilla.txt # Lithops configuration, Vanilla.
- ./_etc_lithops_config--scone.txt # Lithops configuration, SCONE

> Edit accordingly both files above:
>	+ **`lithops: backend:`** and **`lithops: storage:`**
>	+ **`k8s: docker_user:`** and **`k8s: docker_password:`**

- ./_root_kube_config.txt # Kubernetes client configuration, Shared
> Get a copy from your home directory <u>$HOME/.kube/config</u> and save it here with the name above, or edit here accordingly:
> - **`clusters: cluster: certificate-authority-data:`**
> - **`users: user: client-certificate-data:`** and **`users: user: client-key-data:`**

- ./benchmark.py # Python program, Shared
- ./run.sh # Benchmark execution script, Shared
- ./env.sh # Environment variables for Python program, Shared

It is not necessary to change the remaining files, unless you want or need

#### Load Lithops clients

**Vanilla**. Execute the shell script: `./docker_run_vanilla_lithops.sh`. Container created <u>_lithopsclientalpinevan_</u>

**SCONE**. Execute the shell script: `./docker_run_scone_lithops.sh`. Container created <u>_lithopsclientalpinesco_</u>

Both scripts have environment variables that are passed as parameters to the `docker run` command

#### Access the terminal

**Vanilla**. Enter `docker exec -i -t lithopsclientalpinevan bash`

**SCONE**. Enter `docker exec -i -t lithopsclientalpinesco bash`

There are 2 sets of benchmarks: _simpler_ (hello, multiprocessing, storage os and storage cloud) and _complete_ (simpler, plus many others)

Run **`nohup /python/run.sh simpler &`**
<br>
It will save a log file: _exe_bench_simpler.out_

Run **`nohup /python/run.sh complete &`**
<br>
It will save a log file: _exe_bench_complete.out_
