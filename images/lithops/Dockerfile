FROM registry.scontain.com/sconecuratedimages/python:3.13t-debian12.10-slim

LABEL SYSTEM="Lithops Singularity plus Metaspace over SCONE installation of Python 3.13t NO GIL support"
LABEL SPONSOR="NEARDATA Consortium is part of the Horizon Science Projects of EU Commission 101092644"
LABEL MAINTAINER="Scontain GmbH https://scontain.com/"
LABEL EMAIL="info@scontain.com"

ARG LT_VERSION="3.6.1"

###
# setting up system's time zone to avoid Lithops execution breaking
RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/locatime

###
# necessary to build system's font cache for Lithops usage
RUN apt update && apt install -y fontconfig && \
    fc-cache -fv

###
# preparing required directories for installation and usage
RUN mkdir -vp /app /lithops /extra/sources /root/.kube /python

###
# apt installations
RUN set -eux; \
        \
        apt-get update; \
        apt-get install -y \
                cl-cffi \
                libpq-dev \
                procps; \
        apt-mark showmanual >/tmp/savedAptMark; \
        apt-get install -y --no-install-recommends \
                zip \
                git \
                gcc \
                curl \
                wget

###
# Lithops installation
COPY ./files/$LT_VERSION/requirements-singularity-py13.txt      /extra/sources/requirements-singularity.txt
RUN set -eux; \
    \
# rust 1.87.0 was the stable version at the time of editing this file \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain=1.87.0; \
#RUN apt update && apt install -y gcc cl-cffi libpq-dev \
    cd /extra/sources && \
    pip install --no-deps -r /extra/sources/requirements-singularity.txt; \
    git clone https://github.com/lithops-cloud/lithops && \
    cd lithops && \
    git checkout ceebd0f2d377f583885e7a0c5bbb8bca75bf2d96


#
# 07apr patches by URV and workaround by mig to run with other Python than 3.8
COPY ./files/$LT_VERSION/patches_urv/jobrunner.py.txt       /extra/sources/lithops/lithops/worker/jobrunner.py
RUN set -eux; \
    \
    cd /extra/sources/lithops && \
    pip install -v --no-deps $PWD && \
    sed -i -e 's;#!/usr/local/bin/python3.13.native;#!/usr/local/bin/python3.13;g' /usr/local/bin/lithops && \
    sed -i -e 's/raise Exception((\"The indicated runtime/logger.debug((\"The indicated runtime/' /usr/local/lib/python3.13t/site-packages/lithops/invokers.py

###
# backend: k8s configuration
COPY files/$LT_VERSION/k8s--entry_point.py /usr/lib/python3.13/site-packages/lithops/serverless/backends/k8s/entry_point.py
COPY files/$LT_VERSION/k8s--config.py      /usr/lib/python3.13/site-packages/lithops/serverless/backends/k8s/config.py
COPY files/$LT_VERSION/k8s--k8s.py         /usr/lib/python3.13/site-packages/lithops/serverless/backends/k8s/k8s.py
COPY files/$LT_VERSION/invokers.py         /usr/lib/python3.13/site-packages/lithops/invokers.py

###
# backend: singularty startup
WORKDIR /app
COPY files/singularity/entry_point.py entry_point.py

###
# including demonstration programs
COPY files/hellolithops.py           /python/hellolithops.py
COPY files/multiprocessinglithops.py /python/multiprocessinglithops.py
COPY files/storagelithops.py         /python/storagelithops.py
COPY files/storageoslithops.py       /python/storageoslithops.py

###
# including sconectl configuration artifacts
COPY ./files/sconectl      /scone

ENV APP_HOME=/lithops

###
# setting up default Lithops entrypoint for other purposes
RUN cp -pRf /usr/local/lib/python3.13t/site-packages/lithops $APP_HOME/lithops 
RUN cp $APP_HOME/lithops/serverless/backends/singularity/entry_point.py $APP_HOME/lithopsentry.py

###
# removing temporary installation programs
RUN set -eux; \
    \
    PATH=$HOME/.cargo/bin:$PATH rustup self uninstall -y; \
    apt-mark auto '.*'; \
    apt-mark manual `cat /tmp/savedAptMark`; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    rm -rf /var/lib/apt/lists/*

ENV SCONE_LOG="ERROR"
ENV SCONE_ALLOW_DLOPEN="2"
ENV SCONE_FORK="1"
ENV SCONE_FORK_OS="1"
ENV SCONE_MPROTECT="0"
ENV SCONE_SYSLIBS="1"
ENV SCONE_NO_TIME_THREAD="1"
ENV SCONE_HEAP="3G"
ENV SCONE_MODE="SIM"

###
# default /proc white listed entries required by Python user module psutil
# INF: psutil is not required by Lithops; if it starts to cause too much problem
# of incompatibility with SCONE, it can be safely removed with "pip uninstall psutil"
# here or on runtime
ENV SCONE_PROCFS_WHITELIST=self/net/dev:self/statm:self/smaps

ENTRYPOINT ["/usr/local/bin/python3" ]
CMD ["/usr/local/bin/python3", "/python/hellolithops.py" ]
