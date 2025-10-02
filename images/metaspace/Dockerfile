FROM yourdockerrepository/lithops:3.6.1-singularity-python3.13t-5.9.0

LABEL SYSTEM="Lithops Singularity plus Metaspace over SCONE installation of Python 3.13t NO GIL support"
LABEL SPONSOR="NEARDATA Consortium is part of the Horizon Science Projects of EU Commission 101092644"
LABEL MAINTAINER="Scontain GmbH https://scontain.com/"
LABEL EMAIL="info@scontain.com"

###
# Metaspace installation
###
# building metaspace Python module from source; it is not available by "pip"
#
# URV prepared a special fork from https://github.com/metaspace2020/metaspace/
# ... https://github.com/GEizaguirre/metaspace-py13
# ... to cover Python 3.13t (with optional GIL support). originally
# ... Metaspace was prepared for Python 3.8
#
# also, as it is not available by "pip", it is necessary to keep the sources
# ... inside the system, i.e. this image
#
# therefore it is better to clone it separately from Dockerfile and keept there
# ... in the building directory and COPY it to the image and build it
#
# only this directory metaspace-py13/metaspace/engine/ needs to exist on host to 
# ... build the module
# ... if you clone it, you can remove everything else
# ... it is not present in this repository, for it has ~50MB
# ... furthermore, it might be inconvenient to keep as git submodule
#
# the shell script ./build_metaspace.sh will check the directory's
# ... existence and clone it otherwise
# 
COPY metaspace-py13/metaspace/engine/  /extra/sources/metaspace
COPY check_modules.sh                  /extra/sources/metaspace/

SHELL ["/bin/bash", "-c"]

WORKDIR /extra/sources/metaspace

###
RUN set -eux; \
    \
### \
# apt installations \
    apt-get update; \
    apt-mark showmanual >/tmp/savedAptMark; \
    apt-get install -y --no-install-recommends \
            zip \
            git \
            gcc \
            make \
            curl \
            wget; \
    \
### \
# Rust installation is required for building some Python modules (as well as GCC is also required) \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain=1.87.0; \
    \
    mv -v  /usr/local/bin/python3.13 /usr/local/bin/python3.13.scone; \
    cp -pv /usr/local/bin/python3.13.native /usr/local/bin/python3.13; \
    \
    pip install --upgrade pip setuptools wheel && \
    source $HOME/.cargo/env && \
    chmod +x check_modules.sh && \
    ./check_modules.sh && \
    pip list && \
    pip list |egrep -v '^Package|^---' |awk '{print $1 "==" $2 }' >requirements-installed.txt && \
    sdiff requirements-py13.txt requirements-installed.txt || true; \
    \
    pip install -v -e $PWD; \
    \
### \
# removing temporary installation programs and resetting Python configuration \
    \
    rustup self uninstall -y; \
    apt-mark auto '.*'; \
    apt-mark manual `cat /tmp/savedAptMark`; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /tmp/savedAptMark; \
    mv -v  /usr/local/bin/python3.13.scone /usr/local/bin/python3.13; \
    ls -l /usr/local/bin/python3.13.native /usr/local/bin/python3.13

WORKDIR /app
