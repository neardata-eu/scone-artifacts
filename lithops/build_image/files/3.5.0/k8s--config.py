#
# (C) Copyright Cloudlab URV 2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

DEFAULT_CONFIG_KEYS = {
    'runtime_timeout': 600,  # Default: 10 minutes
    'master_timeout': 600,  # Default: 10 minutes
    'runtime_memory': 512,  # Default memory: 512 MB
    'runtime_cpu': 1,  # 1 vCPU
    'max_workers': 100,
    'worker_processes': 1,
    'docker_server': 'docker.io'
}

# mig 13nov2024 - Patch by Miguel @ SCONTAIN. New SCONE related configuration
SCONE_CONFIG_KEYS = {
    'scone_master_requests_cpu': '0.1',
    'scone_master_requests_memory': '384Mi',
    'scone_master_limits_cpu': '2',
    'scone_master_limits_memory': '2048Mi',
    'scone_master_limits_sgx': '1',
    'scone_master_heap'            : '256M',
    'scone_master_mode'            : 'AUTO',
    'scone_master_allow_dl_open'   : '0',
    'scone_master_fork'            : '0',
    'scone_master_syslibs'         : '0',
    'scone_master_procfs_whitelist' : 'self/net/dev:self/statm:self/smaps',

    'scone_worker_requests_cpu': '0.1',
    'scone_worker_requests_memory': '768Mi',
    'scone_worker_limits_cpu': '2',
    'scone_worker_limits_memory': '2048Mi',
    'scone_worker_limits_sgx': '1',
    'scone_worker_heap'            : '512M',
    'scone_worker_mode'            : 'AUTO',
    'scone_worker_allow_dl_open'   : '0',
    'scone_worker_fork'            : '0',
    'scone_worker_syslibs'         : '0',
    'scone_worker_procfs_whitelist' : 'self/net/dev:self/statm:self/smaps',

    'scone_cas_addr'        : '172.20.0.1',
    'scone_las_addr'        : '172.20.0.1',
    'scone_config_id'       : '',

    'k8s_master_ip'   : '0.0.0.0'
}

DEFAULT_GROUP = "batch"
DEFAULT_VERSION = "v1"
MASTER_NAME = "lithops-master"
MASTER_PORT = 8080

FH_ZIP_LOCATION = os.path.join(os.getcwd(), 'lithops_k8s.zip')


DOCKERFILE_DEFAULT = """
RUN apt-get update && apt-get install -y \
        zip redis-server curl \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade --ignore-installed setuptools six pip \
    && pip install --upgrade --no-cache-dir --ignore-installed \
        flask \
        pika \
        boto3 \
        ibm-cloud-sdk-core \
        ibm-cos-sdk \
        redis \
        requests \
        PyYAML \
        kubernetes \
        numpy \
        cloudpickle \
        ps-mem \
        tblib \
        psutil

ENV PYTHONUNBUFFERED TRUE

# Copy Lithops proxy and lib to the container image.
ENV APP_HOME /lithops
WORKDIR $APP_HOME

COPY lithops_k8s.zip .
RUN unzip lithops_k8s.zip && rm lithops_k8s.zip
"""

JOB_DEFAULT = """
apiVersion: batch/v1
kind: Job
metadata:
  name: lithops-worker-name
  namespace: default
  labels:
    type: lithops-worker
    version: lithops_vX.X.X
    user: lithops-user
spec:
  # mig 13nov2024 - Patch by Miguel @ SCONTAIN. Doubling the timeouts
  activeDeadlineSeconds: 1200
  ttlSecondsAfterFinished: 120
  parallelism: 1
  # mig 13nov2024 - Patch by Miguel @ SCONTAIN. Rerun if failed at most 6 times
  backoffLimit: 6
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: "lithops"
          image: "<INPUT>"
          # imagePullPolicy: IfNotPresent
          # mig 13nov2024 SCONTAIN. Above was already commented
          imagePullPolicy: Always
          # mig 18nov2024 SCONTAIN. to test
          command: ["python3"]
          #command: ["/usr/bin/strace"]
          args:
          #  - "-f"
          #  - "python3"
            - "/lithops/lithopsentry.py"
            - "$(ACTION)"
            - "$(DATA)"
            - "$(MASTER_POD_IP)"
          env:
            - name: ACTION
              value: ''
            - name: DATA
              value: ''
            - name: MASTER_POD_IP
              value: ''
              # mig 13nov2024 - Patch by Miguel @ SCONTAIN. SCONE related variables
            - name: SCONE_HEAP
              value: ''
              # '768M'
            - name: SCONE_MODE
              value: ''
              # 'AUTO'
            - name: SCONE_ALLOW_DLOPEN
              value: ''
              # '2'
            - name: SCONE_FORK
              value: ''
              # '1'
            - name: SCONE_SYSLIBS
              value: ''
              # '1'
            - name: SCONE_PROCFS_WHITELIST
              value: ''
              # 'self/net/dev:self/statm:self/smaps'
            - name: SCONE_CAS_ADDR
              value: ''
              # '172.20.0.1'
            - name: SCONE_LAS_ADDR
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP
            - name: SCONE_CONFIG_ID
              value: ''
              # 'Lithops-Benchmark-D41-123-45678-90120/benchmark'
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          resources:
            # mig 14apr2024 - Patch by Miguel @ SCONTAIN. Increased initial memory and cpu and memory limits
            requests:
              cpu: '0.2'
              memory: 4096Mi
            limits:
              cpu: '8'
              memory: 8192Mi
              sgx.k8s.io/sgx: "1"
      imagePullSecrets:
        - name: lithops-regcred
"""

POD = """
apiVersion: v1
kind: Pod
metadata:
  name: lithops-worker
spec:
  containers:
    - name: "lithops-worker"
      image: "<INPUT>"
      # mig 13nov2024 SCONTAIN
      imagePullPolicy: Always
      command: ["python3"]
      args:
        - "/lithops/lithopsentry.py"
        - "--"
        - "--"
      # mig 14apr2024 - Patch by Miguel @ SCONTAIN. Increased initial memory and cpu and memory limits
#      resources:
#        requests:
#          cpu: '1'
#          memory: '512Mi'
      resources:
        # mig 14apr2024 - Patch by Miguel @ SCONTAIN. Increased initial memory and cpu and memory limits
        requests:
          cpu: '0.2'
          memory: 4096Mi
        limits:
#          cpu: '8'
#          memory: 8192Mi
          sgx.k8s.io/sgx: "1"
  imagePullSecrets:
    - name: lithops-regcred
"""


def load_config(config_data):
    for key in DEFAULT_CONFIG_KEYS:
        if key not in config_data['k8s']:
            config_data['k8s'][key] = DEFAULT_CONFIG_KEYS[key]

    if 'runtime' in config_data['k8s']:
        runtime = config_data['k8s']['runtime']
        registry = config_data['k8s']['docker_server']
        if runtime.count('/') == 1 and registry not in runtime:
            config_data['k8s']['runtime'] = f'{registry}/{runtime}'

    if config_data['k8s'].get('rabbitmq_executor', False):
        config_data['k8s']['amqp_url'] = config_data['rabbitmq']['amqp_url']

    # mig 13nov2024 - Patch by Miguel @ SCONTAIN. New SCONE related configuration
    for key in SCONE_CONFIG_KEYS:
        if key not in config_data['k8s']:
            config_data['k8s'][key] = SCONE_CONFIG_KEYS[key]
