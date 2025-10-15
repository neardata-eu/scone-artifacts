# Build images

Here you will find the applications ported to confidential computing on SCONE (i.e. _sconified_).

* [flowerml](./flowerml)
* [keycloak](./keycloak)
* [lithops](./lithops)
* [metaspace](./metaspace)
* [minio](./minio)
* [pravega-client](./pravega-client)

In each sub-directory you will find a shell script `build_%application%.sh` to build the corresponding application's Docker image.

You can make modifications in their Dockerfile or other artifacts to fit your needs.

First, you need to access to the SCONE's registry. Request [here](https://sconedocs.github.io/registry/ "Registry").
