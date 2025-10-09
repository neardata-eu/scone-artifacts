## Dataset for Demo
The dataset used for the demo is the [CIFAR10](https://www.cs.toronto.edu/~kriz/cifar.html) dataset.
Direct Downloadlink can be found [here](https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz).
The dataset is downloaded and stored in the `data\clientX` folders.

Downloading is done as part of the demos:

* `start_demo_no_sgx.sh`
* `start_sgx_demo_no_cas.sh`
* `start_sgx_demo_with_cas.sh`


## Preparations

### Build the containers

```bash
docker build -t fl_challenge:team_name -f Dockerfile .
docker build -t fl_challenge:team_name_sgx -f Dockerfile_scone .
```

### Scone/SGX stuff

As root:

```bash
echo 0 > /proc/sys/vm/mmap_min_addr
```

Login to the scone registry for the LAS image:

```bash
docker login registry.scontain.com:5050 -u rcrane -p MfhCxb5QXkQyaVhw2FCb
```

Adapt files for your host (`isgx`/`sgx_enclave`, local ip address).

Change all occurences of "141.76.44.249" to the host's ip-address:


`start_demo_no_sgx.sh`
`start_sgx_demo_no_cas.sh`
`start_sgx_demo_with_cas.sh`
`prepare_cas_session.sh`
`src/server/run_python_with_cas.sh `
`src/client/run_python_with_cas.sh`
`start_sgx_demo_with_cas.sh`


Change all occurences of 'sgx_enclave' to 'isgx' if necessary:

`prepare_cas_session.sh`
`docker-compose-sgx-cas.yaml`
`docker-compose-sgx.yaml`


Run the server first (as a test):

```bash
docker-compose -f docker-compose-sgx.yaml run server
```

                              
## Start demos


### vanilla federated learning demo

```bash
./start_demo_no_sgx.sh
```

### Sconified federated learning demo

```bash
./start_sgx_demo_no_cas.sh
```

```bash
./start_sgx_demo_with_cas.sh
```


## Other


For actual challenge setup change settings in docker-compose.yaml to:
This setting permits or forbits docker to create a connection to the world wide web.
```yaml
[...]
networks:
  challenge_net:
    internal: true
[...]
```
otherwise:
```yaml
[...]
networks:
  challenge_net:
    internal: false
[...]
```



