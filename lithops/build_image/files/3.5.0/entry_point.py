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

import pika
import os
import sys
import uuid
import json
import logging
import flask
import time
import requests
from functools import partial
from multiprocessing import Value, Process

from lithops.version import __version__
from lithops.utils import setup_lithops_logger, b64str_to_dict
from lithops.worker import function_handler
from lithops.worker.utils import get_runtime_metadata
from lithops.constants import JOBS_PREFIX
from lithops.storage.storage import InternalStorage

from lithops.serverless.backends.k8s import config

# mig 13nov2024: WA for hostname resolution
import subprocess as wapysubprocess

logger = logging.getLogger('lithops.worker')

proxy = flask.Flask(__name__)

JOB_INDEXES = {}

# mig 13nov2024 - Patch by Miguel @ SCONTAIN. Global variable with Master IP for inter-functions communication
master_ip_attested = ""


@proxy.route('/get-range/<jobkey>/<total_calls>/<chunksize>', methods=['GET'])
def get_range(jobkey, total_calls, chunksize):
    global JOB_INDEXES

    range_start = 0 if jobkey not in JOB_INDEXES else JOB_INDEXES[jobkey]
    range_end = min(range_start + int(chunksize), int(total_calls))
    JOB_INDEXES[jobkey] = range_end

    range = "-1" if range_start == int(total_calls) else f'{range_start}-{range_end}'
    remote_host = flask.request.remote_addr
    proxy.logger.info(f'Sending range "{range}" to Host {remote_host}')

    return range


def run_master_server():
    # Start Redis Server in the background
    # logger.info("Starting redis server in Master Pod")
    # os.system("redis-server --bind 0.0.0.0 --daemonize yes")
    # logger.info("Redis server started")

    # mig 31my2024: WA for hostname resolution
    #with open("patch.hosts.sh", "w") as f:
    #    f.write(f'echo "172.20.0.1 host.docker.internal" >> /etc/hosts\n')
    #    f.write(f'echo "172.20.0.1 miniostoragesco" >> /etc/hosts\n')
    #    f.write(f'echo "172.20.0.1 minio.neardata" >> /etc/hosts\n')
    #    f.write(f'echo "172.20.0.1 lithops" >> /etc/hosts\n')
    #    f.write(f'echo "172.20.0.1 lithops.neardata" >> /etc/hosts\n')
    #    f.write(f'echo "172.20.0.1 lithops-master" >> /etc/hosts\n')
    #    f.write(f'echo "172.20.0.1 lithops-master.neardata" >> /etc/hosts\n')
    #response= wapysubprocess.call(["chmod", "+x", "patch.hosts.sh"], stdout=wapysubprocess.DEVNULL, stderr=wapysubprocess.DEVNULL)
    #response= wapysubprocess.call(["sh", "-c", "./patch.hosts.sh"], stdout=wapysubprocess.DEVNULL, stderr=wapysubprocess.DEVNULL)
    #
    ###

    proxy.logger.setLevel(logging.DEBUG)
    #logger.debug(f"..:DBG:run_master_server():proxy.run(debug=True, host='0.0.0.0', port=config.MASTER_PORT[{config.MASTER_PORT}], use_reloader=False)")
    proxy.run(debug=True, host='0.0.0.0', port=config.MASTER_PORT, use_reloader=False)


def extract_runtime_meta(payload):
    logger.info(f"Lithops v{__version__} - Generating metadata")

    runtime_meta = get_runtime_metadata()

    internal_storage = InternalStorage(payload)
    status_key = '/'.join([JOBS_PREFIX, payload['runtime_name'] + '.meta'])
    logger.info(f"Runtime metadata key {status_key}")
    dmpd_response_status = json.dumps(runtime_meta)
    internal_storage.put_data(status_key, dmpd_response_status)


def run_job_k8s(payload):
    logger.info(f"Lithops v{__version__} - Starting kubernetes execution")

    os.environ['__LITHOPS_ACTIVATION_ID'] = str(uuid.uuid4()).replace('-', '')[:12]
    os.environ['__LITHOPS_BACKEND'] = 'k8s'

    total_calls = payload['total_calls']
    job_key = payload['job_key']
    chunksize = payload['chunksize']

    call_ids = payload['call_ids']
    data_byte_ranges = payload['data_byte_ranges']

    # mig 13nov2024 - Patch by Miguel @ SCONTAIN. Changed form to get Master IP for both environment or command line (when attested)
    logger.debug(f"..:DBG:MASTER_POD_IP from env:"+str(os.environ.get('MASTER_POD_IP'))+" and command line:"+master_ip_attested)
    print(f"..:DBG:MASTER_POD_IP from env:"+str(os.environ.get('MASTER_POD_IP'))+" and command line:"+master_ip_attested)
    with open('/entry_point.out', 'a', encoding="utf-8") as _f:
        _f.write(f"..:DBG:MASTER_POD_IP from env:"+str(os.environ.get('MASTER_POD_IP'))+" and command line:"+master_ip_attested+"\n")
    master_ip = os.environ.get('MASTER_POD_IP', master_ip_attested)
    # master_ip = master_ip_attested
    if os.environ.get('MASTER_POD_IP') == None:
        os.environ['MASTER_POD_IP'] = master_ip_attested

    ## mig 31my2024: WA for hostname resolution
    #with open("patch.hosts.sh", "w") as f:
    #    f.write(f'echo "172.20.0.1 host.docker.internal" >> /etc/hosts\n')
    #    f.write(f'echo "172.20.0.1 miniostoragesco" >> /etc/hosts\n')
    #    f.write(f'echo "172.20.0.1 minio.neardata" >> /etc/hosts\n')
    #    f.write(f'echo "172.20.0.1 lithops" >> /etc/hosts\n')
    #    f.write(f'echo "172.20.0.1 lithops.neardata" >> /etc/hosts\n')
    #    f.write(f'echo "{master_ip} lithops-master" >> /etc/hosts\n')
    #    f.write(f'echo "{master_ip} lithops-master.neardata" >> /etc/hosts\n')
    #response= wapysubprocess.call(["chmod", "+x", "patch.hosts.sh"], stdout=wapysubprocess.DEVNULL, stderr=wapysubprocess.DEVNULL)
    #response= wapysubprocess.call(["sh", "-c", "./patch.hosts.sh"], stdout=wapysubprocess.DEVNULL, stderr=wapysubprocess.DEVNULL)
    #
    ###

    job_finished = False
    while not job_finished:
        #logger.debug(f"..:DBG:entered:while not job_finished")
        #print(f"..:DBG:entered:while not job_finished")
        #with open('/entry_point.out', 'a', encoding="utf-8") as _f:
        #    _f.write(f"..:DBG:entered:while not job_finished\n")
        call_ids_range = None

        while call_ids_range is None:
            try:
                server = f'http://{master_ip}:{config.MASTER_PORT}'
                url = f'{server}/get-range/{job_key}/{total_calls}/{chunksize}'
                # mig 13nov2024 - Patch by Miguel @ SCONTAIN. Changed form to get Master IP for both environment or command line (when attested)
                #logger.debug(f"..:DBG:server={server}. executing next: res = requests.get(url[{url}], timeout=0.1)")
                #print(f"..:DBG:server={server}. executing next: res = requests.get(url[{url}], timeout=0.1)")
                #with open('/entry_point.out', 'a', encoding="utf-8") as _f:
                #    _f.write(f"..:DBG:server={server}. executing next: res = requests.get(url, timeout=0.1)\n")
                #
                ###
                res = requests.get(url, timeout=0.1)
                #print(f"..:DBG:res obtained...")
                #print(res)
                #print(f"..:DBG:res obtained...")
                #print(f"..:DBG:executing:call_ids_range = res.text")
                #print(f"..:DBG:executing:res.text:")
                #print(res.text)
                call_ids_range = res.text  # for example: 0-5
                #print(f"..:DBG:executing:call_ids_range:")
                #print(call_ids_range)
            except Exception:
                time.sleep(0.1)

        logger.info(f"Received range: {call_ids_range}")
        if call_ids_range == "-1":
            job_finished = True
            continue

        start, end = map(int, call_ids_range.split('-'))
        dbr = [data_byte_ranges[int(call_id)] for call_id in call_ids[start:end]]
        payload['call_ids'] = call_ids[start:end]
        payload['data_byte_ranges'] = dbr
        function_handler(payload)

    logger.info("Finishing kubernetes execution")


def run_job_k8s_rabbitmq(payload):
    logger.info(f"Lithops v{__version__} - Starting kubernetes execution")

    act_id = str(uuid.uuid4()).replace('-', '')[:12]
    os.environ['__LITHOPS_ACTIVATION_ID'] = act_id
    os.environ['__LITHOPS_BACKEND'] = 'k8s_rabbitmq'

    function_handler(payload)
    with running_jobs.get_lock():
        running_jobs.value += len(payload['call_ids'])

    logger.info("Finishing kubernetes execution")


def callback_work_queue(ch, method, properties, body):
    """Callback to receive the payload and run the jobs"""
    logger.info("Call from lithops received.")

    message = json.loads(body)
    tasks = message['total_calls']

    # If there are more tasks than cpus in the pod, we need to send a new message
    if tasks <= running_jobs.value:
        processes_to_start = tasks
    else:
        if running_jobs.value == 0:
            logger.info("All cpus are busy. Waiting for a cpu to be free")
            ch.basic_nack(delivery_tag=method.delivery_tag)
            time.sleep(0.5)
            return

        processes_to_start = running_jobs.value

        message_to_send = message.copy()
        message_to_send['total_calls'] = tasks - running_jobs.value
        message_to_send['call_ids'] = message_to_send['call_ids'][running_jobs.value:]
        message_to_send['data_byte_ranges'] = message_to_send['data_byte_ranges'][running_jobs.value:]

        message['total_calls'] = running_jobs.value
        message['call_ids'] = message['call_ids'][:running_jobs.value]
        message['data_byte_ranges'] = message['data_byte_ranges'][:running_jobs.value]

        ch.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=json.dumps(message_to_send),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

    logger.info(f"Starting {processes_to_start} processes")

    message['worker_processes'] = running_jobs.value
    with running_jobs.get_lock():
        running_jobs.value -= processes_to_start

    Process(target=run_job_k8s_rabbitmq, args=(message,)).start()

    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_rabbitmq_listening(payload):
    global running_jobs

    # Connect to rabbitmq
    params = pika.URLParameters(payload['amqp_url'])
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_qos(prefetch_count=1)

    # Shared variable to track completed jobs
    running_jobs = Value('i', payload['cpus_pod'])

    # Start listening to the new job
    channel.basic_consume(queue='task_queue', on_message_callback=callback_work_queue)

    logger.info("Listening to rabbitmq...")
    channel.start_consuming()


if __name__ == '__main__':
    action = sys.argv[1]
    encoded_payload = sys.argv[2]
    # mig 13nov2024 - Patch by Miguel @ SCONTAIN. Informing Master IP via command line
    with open('/entry_point.out', 'a', encoding="utf-8") as _f:
        _f.write(f"..:DBG:__main__ len(sys.argv)="+str(len(sys.argv))+"\n")
    if len(sys.argv) > 3:
        master_ip_attested = sys.argv[len(sys.argv)-1] # from [3]
        with open('/entry_point.out', 'a', encoding="utf-8") as _f:
            _f.write(f"..:DBG:__main__ len(sys.argv) > 3. master_ip_attested="+master_ip_attested+"\n")

    payload = b64str_to_dict(encoded_payload)
    setup_lithops_logger(payload.get('log_level', 'INFO'))

    switcher = {
        'get_metadata': partial(extract_runtime_meta, payload),
        'run_job': partial(run_job_k8s, payload),
        'run_master': run_master_server,
        'start_rabbitmq': partial(start_rabbitmq_listening, payload)
    }

    func = switcher.get(action, lambda: "Invalid command")
    func()
