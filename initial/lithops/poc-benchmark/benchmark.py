import os

import requests

###
# LT
from lithops import FunctionExecutor
from lithops.multiprocessing import Pool
from lithops import Storage
from lithops.storage.cloud_proxy import os as oscloud

##
# to run %LITHOPS_REPO%/examples
# import and others
import lithops
from urllib.parse import urlparse
import pickle
from lithops.wait import get_result
import random
from lithops import multiprocessing as mp
from lithops.utils import setup_lithops_logger
import logging

#
def hello(name):
    return 'Hello {}!'.format(name)

def hello(name, phrase):
     return 'Hello {}! {}'.format(name, phrase)

def double(i):
    return i * 2

# 
def mult(x, y):
    return x * y

#
# call_async_class.py
class MyClass:
    def __init__(self, base) -> None:
        self.base = base

    def __call__(self, x, fn) -> int:
        return fn(self.base, x)

#
# context_manager.py
def my_map_function(id, x):
    print(f"I'm activation number {id}")
    return x + 7

#
# cloudobject.py
def my_function_put(text, storage):
    co1 = storage.put_cloudobject(f'Cloudobject test 1: {text}')
    co2 = storage.put_cloudobject(f'Cloudobject test 2: {text}')
    return [co1, co2]


def my_function_get(co, storage):
    data = storage.get_cloudobject(co)
    return data

#
# failed_futures.py
def my_map_function_ff(id, x):
    print(f"I'm activation number {id}")
    time.sleep(2)
    if id in [2, 4]:
        raise MemoryError()
    return x

#
# function_chaining.py
def my_func1(x):
    return x + 2, 5


def my_func2(x, y):
    return x + y, 5, 2


def my_func3(x, y, z):
    return x + y + z

#
# internal_execution.py
def my_map_function_ii(id, x):
    print(f"I'm activation number {id}")
    time.sleep(3)
    return x + 7


def my_function_ii(x):
    iterdata = range(x)
    fexec = lithops.FunctionExecutor()
    return fexec.map(my_map_function_ii, iterdata)

#
# map_reduce.py
def my_map_function_mr(x):
    time.sleep(x * 2)
    return x + 7


def my_reduce_function_mr(results):
    total = 0
    for map_result in results:
        total = total + map_result
    return total

#
# map_reduce_localhost.py
def my_map_function_mrobj(obj):
    print(f'I am processing the object from {obj.path}')
    counter = {}

    data = obj.data_stream.read()

    for line in data.splitlines():
        for word in line.decode('utf-8').split():
            if word not in counter:
                counter[word] = 1
            else:
                counter[word] += 1
    return counter

def my_reduce_function_mrobj(results):
    final_result = {}
    for count in results:
        for word in count:
            if word not in final_result:
                final_result[word] = count[word]
            else:
                final_result[word] += count[word]
    return final_result

#
# multiple_args_call_async.py
def my_function_mult(x, y):
    return x + y


def sum_list(list_of_numbers):
    total = 0
    for num in list_of_numbers:
        total = total + num
    return total


def sum_list_mult(list_of_numbers, x):
    total = 0
    for num in list_of_numbers:
        total = total + num
    return total * x

#
# serialize_futures.py
def my_map_function_sf(id, x):
    print(f"I'm activation number {id}")
    return x + 7

#
# pi_estimation.py
def is_inside_pi(n):
    count = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x * x + y * y < 1:
            count += 1
    return count

#
# pool_initializer.py
def work_pooli(num):
    global param1, param2
    return param1, param2


def initializer_function_pooli(arg1, arg2):
    global param1, param2
    param1 = arg1
    param2 = arg2

#
# pool.py
def hello_poolr(name):
    return 'Hello {}!'.format(name)


def square_poolr(x):
    return x * x


def divide_poolr(x, y):
    return x / y


def sleep_seconds_poolr(s):
    time.sleep(s)
    return f"has slept for {s} seconds"

#
##

import os.path
import sys
import time

#
###

username = os.getenv("USERNAME")
greeting = os.getenv('GREETING', 'Lithops has been ported to SCONE')

def do_benchmark_complete():
    print("got request")

    print('Edge client program execution has started\n'      )
    print('\n'      )

    print('Execution of Lithops process\n'      )
    print('\n'      )

    ini=time.time()
    print('HELLO WORLD\n'      )
    with FunctionExecutor() as fexec:
        fut = fexec.call_async(hello, (username, greeting))
        print(fut.result())
        resultlt=str(fut.result())
        print('Message from Lihtops process: %s\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('MULTIPROCESSING\n'      )
    with Pool() as pool:
        print('Message from Lihtops process: %s\n' % 'doubling values of array [1, 2, 3, 4]'     )
        result = pool.map(double, [1, 2, 3, 4])
        print(result)
        resultlt=', '.join(map(str, result))
        print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('STORAGE LITHOPS\n'      )
    if __name__ == "__main__":
        st = Storage()
        bucket='mybucket'
        fkey='test.txt'
        print('Message from Lihtops process: using bucket: %s\n' % bucket     )
        print('Message from Lihtops process: wrting file on it: %s\n' % fkey     )
        st.put_object(bucket=bucket,
                    key=fkey,
                    body=str('Hello '+username+'!'))

        result = st.get_object(bucket=bucket, key=fkey)
        # print(st.get_object(bucket='mybucket',
        #                     key='test.txt'))
        resultlt=str(result)
        print('Message from Lihtops process: getting content from file: %s\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('STORAGE CLOUD OS\n'      )
    if __name__ == "__main__":
        filepath = 'bar/foo.txt'
        with oscloud.open(filepath, 'w') as f:
            print('Message from Lihtops process: creating and removing "%s"\n' % filepath     )
            print('Message from Lihtops process: writing "%s" to file\n' % str('Hello '+username+'!')     )
            f.write(str('Hello '+username+'!'))

        dirname = oscloud.path.dirname(filepath)
        print(oscloud.listdir(dirname))
        print('Message from Lihtops process: listing files in directory "%s"\n' % oscloud.listdir(dirname)     )
        print('Message from Lihtops process: deleting "%s"\n' % filepath     )
        result = oscloud.remove(filepath)
        resultlt='success'
        if result == None:
            print('Message from Lihtops process: %s\n' % resultlt     )
        else:
            print('Message from Lihtops process: %s\n' % 'fail'     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('FUNCTION INVOCATION WITH FUNCTION AS PARAMETER FOR IN CLASS METHOD\n'      )
    print('PARAMETERS: FUNCTION = mult()\n'      )
    print('PARAMETERS: BASE FACTOR = 5\n'      )
    print('PARAMETERS: FACTOR a = 2\n'      )
    print('PARAMETERS: FACTOR b = 3\n'      )
    if __name__ == '__main__':
        fexec = lithops.FunctionExecutor()
        inst = MyClass(5)
        fexec.map(inst, [(2, mult), (3, mult)])
        result = fexec.get_result()
        resultlt=', '.join(map(str, result))
        print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('CONTEXT MANAGER\n'      )
    print('FUNCTION INVOCATION WITH FUNCTION AS PARAMETER FOR IN Lithops map() FUNCTION\n'      )
    print('PARAMETERS: FUNCTION = my_map_function()\n'      )
    print('PARAMETERS: ITERATION ARRAY [1, 2, 3, 4]\n'      )
    if __name__ == "__main__":
        iterdata = [1, 2, 3, 4]
        with lithops.FunctionExecutor() as fexec:
            fexec.map(my_map_function, iterdata)
            result = fexec.get_result()
            resultlt=', '.join(map(str, result))
            print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('CLOUD OBJECT WITH CONTEXT MANAGER\n'      )
    if __name__ == "__main__":
        with lithops.FunctionExecutor() as fexec:
            fexec.call_async(my_function_put, 'Hello World')
            cloudobjects = fexec.get_result()
            fexec.map(my_function_get, cloudobjects)
            result = fexec.get_result()
            resultlt=', '.join(map(str, result))
            print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('CLOUD OBJECT WITHOUT CONTEXT MANAGER\n'      )
    if __name__ == "__main__":
        fexec = lithops.FunctionExecutor()
        fexec.call_async(my_function_put, 'Hello World')
        cloudobjects = fexec.get_result()
        fexec.map(my_function_get, cloudobjects)
        result = fexec.get_result()
        resultlt=', '.join(map(str, result))
        print('Message from Lihtops process: [%s]\n' % resultlt     )
        fexec.clean()  # or fexec.clean(cs=cloudobjects)
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('FAILED FUTURES\n'      )
    print('PARAMETERS: FUNCTION = my_map_function_ff()\n'      )
    print('ITERATION ARRAY: ["a", "b", "c", "d", "e"]\n'      )
    if __name__ == "__main__":
        iterdata = ["a", "b", "c", "d", "e"]
        fexec = lithops.FunctionExecutor(log_level='DEBUG')
        futures = fexec.map(my_map_function_ff, iterdata)
        return_vals = fexec.get_result(fs=futures, throw_except=False)
        resultlt=', '.join(map(str, return_vals))
        print('Message from Lihtops process: intermediary returned values [%s]\n' % resultlt     )
        failed_callids = [int(f.call_id) for f in futures if f.error]
        if failed_callids:
            print('Message from Lihtops process: entering failed call ids\n'     )
            new_iterdata = [iterdata[i] for i in failed_callids]
            futures = fexec.map(my_map_function_ff, new_iterdata)
            new_return_vals = fexec.get_result(fs=futures, throw_except=False)
            for i, failed_callid in enumerate(failed_callids):
                return_vals[failed_callid] = new_return_vals[i]
                print('Message from Lihtops process: failed call id: %s\n' % str(failed_callid)     )
        resultlt=', '.join(map(str, return_vals))
        print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('FUNCTION CHAINING\n'      )
    print('SUCCESSIVE map() CHAIN OF EXECUTIONS. E.G.: map(f1, idata).map(f2).get_result()\n'      )
    print('PARAMETERS: FUNCTION = my_func1()\n'      )
    print('PARAMETERS: FUNCTION = my_func2()\n'      )
    print('PARAMETERS: FUNCTION = my_func3()\n'      )
    print('ITERATION ARRAY: [1, 2, 3]\n'      )
    if __name__ == "__main__":
        iterdata = [1, 2, 3]
        fexec = lithops.FunctionExecutor(log_level='INFO')
        res = fexec.map(my_func1, iterdata).map(my_func2).map(my_func3).get_result()
        resultlt=', '.join(map(str, res))
        print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('MAP REDUCE\n'      )
    print('REDUCER SPAWN AT 20% OF map() (DEFAULT)\n'      )
    print('PARAMETERS: FUNCTION = my_map_function_mr()\n'      )
    print('PARAMETERS: FUNCTION = my_reduce_function_mr()\n'      )
    print('ITERATION ARRAY: [1, 2, 3, 4, 5] WILL BE USED FOR THE FOLLOWING MAP/REDUCE EXECUTIONS\n'      )
    iterdata = [1, 2, 3, 4, 5]
    if __name__ == "__main__":
        fexec = lithops.FunctionExecutor()
        fexec.map_reduce(my_map_function_mr, iterdata, my_reduce_function_mr)
        result=fexec.get_result()
        resultlt=str(result)
        print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('MAP REDUCE\n'      )
    print('REDUCER SPAWN IMMEDIATELY\n'      )
    if __name__ == "__main__":
        fexec = lithops.FunctionExecutor()
        fexec.map_reduce(my_map_function_mr, iterdata, my_reduce_function_mr, spawn_reducer=0)
        result=fexec.get_result()
        resultlt=str(result)
        print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('MAP REDUCE\n'      )
    print('REDUCER SPAWN AT 80% OF map()\n'      )
    if __name__ == "__main__":
        fexec = lithops.FunctionExecutor()
        fexec.map_reduce(my_map_function_mr, iterdata, my_reduce_function_mr, spawn_reducer=80)
        result=fexec.get_result()
        resultlt=str(result)
        print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('OBJECTS MAP REDUCE\n'      )
    print('PARAMETERS: FUNCTION = my_map_function_mrobj()\n'      )
    print('PARAMETERS: FUNCTION = my_reduce_function_mrobj()\n'      )
    #             'https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/vocab.kos.txt',
    #             'https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/vocab.nips.txt',
    #             'https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/vocab.nytimes.txt',
    DATA_URLS = ['https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/vocab.enron.txt',
                 'https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/vocab.pubmed.txt']
    if __name__ == "__main__":
        iterdata = []
        for url in DATA_URLS:
            print('Downloading data from {}'.format(url))
            a = urlparse(url)
            file_path = '/tmp/{}'.format(os.path.basename(a.path))
            iterdata.append(file_path)
            if not os.path.isfile(file_path):
                r = requests.get(url, allow_redirects=True)
                open(file_path, 'wb').write(r.content)
            print(f"URL: {url}\n"     )
            ct=0
            with open(file_path, "rb") as f:
                ct = sum(1 for _ in f)
            print(f"has: {ct}\n"     )
        fexec = lithops.FunctionExecutor(backend='localhost', storage='localhost', log_level='DEBUG')
        fexec.map_reduce(my_map_function_mrobj, iterdata, my_reduce_function_mrobj, obj_chunk_number=2)
        result = fexec.get_result()
        ct=len(result)
        print(f"Result has {ct}\n"     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('ASYNCHRONOUS MULTIPLE PARAMETERS CALL\n'      )
    print('PARAMETERS: FUNCTION = my_function_mult()\n'      )
    print('PARAMETERS: FUNCTION = sum_list()\n'      )
    print('PARAMETERS: FUNCTION = sum_list_mult()\n'      )
    print('PARAMETERS: ARGUMENTS = (3, 6)\n'      )
    if __name__ == "__main__":
        args = (3, 6)
        fexec = lithops.FunctionExecutor()
        fexec.call_async(my_function_mult, args)
        result = fexec.get_result()
        print(f"Result has {result}\n"     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('ASYNCHRONOUS MULTIPLE PARAMETERS CALL\n'      )
    print('PARAMETERS: ARGUMENTS = {"x": 2, "y": 8}\n'      )
    if __name__ == "__main__":
        kwargs = {'x': 2, 'y': 8}
        fexec = lithops.FunctionExecutor()
        fexec.call_async(my_function_mult, kwargs)
        result = fexec.get_result()
        print(f"Result has {result}\n"     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('ASYNCHRONOUS MULTIPLE PARAMETERS CALL\n'      )
    print('PARAMETERS: ARGUMENTS = ([1, 2, 3, 4, 5], )\n'      )
    if __name__ == "__main__":
        args = ([1, 2, 3, 4, 5])
        fexec = lithops.FunctionExecutor()
        fexec.call_async(sum_list, args)
        result = fexec.get_result()
        print(f"Result has {result}\n"     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('ASYNCHRONOUS MULTIPLE PARAMETERS CALL\n'      )
    print('PARAMETERS: ARGUMENTS = ([1, 2, 3, 4, 5], 5)\n'      )
    if __name__ == "__main__":
        args = ([1, 2, 3, 4, 5], 5)
        fexec = lithops.FunctionExecutor()
        fexec.call_async(sum_list_mult, args)
        result = fexec.get_result()
        print(f"Result has {result}\n"     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('ASYNCHRONOUS MULTIPLE PARAMETERS CALL\n'      )
    print('PARAMETERS: ARGUMENTS = {"list_of_numbers": [1, 2, 3, 4, 5], "x": 3}\n'      )
    if __name__ == "__main__":
        kwargs = {'list_of_numbers': [1, 2, 3, 4, 5], 'x': 3}
        fexec = lithops.FunctionExecutor()
        fexec.call_async(sum_list_mult, kwargs)
        result = fexec.get_result()
        print(f"Result has {result}\n"     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('SERIALIZE FUTURES\n'      )
    print('PARAMETERS: FUNCTION = my_map_function_sf()\n'      )
    print('PARAMETERS: FILE = /tmp/futures.pickle\n'      )
    print('EXECUTION: A\n'      )
    rd=0
    if __name__ == "__main__":
        fexec = lithops.FunctionExecutor()
        futures = fexec.map(my_map_function_sf, range(5))
        with open('/tmp/futures.pickle', 'wb') as file:
            pickle.dump(futures, file)
        rd=1
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('SERIALIZE FUTURES\n'      )
    print('EXECUTION: B\n'      )
    if __name__ == "__main__":
        while rd != 1:
            print("Sleeping waiting for previous completion")
            time.sleep(1)
        with open('/tmp/futures.pickle', 'rb') as file:
            futures = pickle.load(file)
        result = get_result(futures)
        resultlt=', '.join(map(str, result))
        print('Message from Lihtops process: [%s]\n' % resultlt     )
        os.remove('/tmp/futures.pickle')                          
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('PI ESTIMATION\n'      )
    print('PARAMETERS: FUNCTION = is_inside_pi()\n'      )
    print('PARAMETERS: PARAMETER = 8 ACTIVATIONS\n'      )
    print('PARAMETERS: PARAMETER = 150000000 DENOMINATOR\n'      )
    try:
        if __name__ == '__main__':
            #np, n = 96, 150000000
            #np, n = 8, 150000000
            np, n = 6, 150000000
            part_count = [int(n / np)] * np
            pool = Pool(processes=np)
            count = pool.map(is_inside_pi, part_count)
            pi = sum(count) / n * 4
            result = "{}".format(pi)
            resultlt=result
            print('Message from Lihtops process: [%s]\n' % resultlt     )
    except Exception as e:
        print('Exception\n'     )
        print(e     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('POOL INITIALIZATION\n'      )
    print('PARAMETERS: FUNCTION = work_pooli()\n'      )
    print('PARAMETERS: FUNCTION = initializer_function_pooli()\n'      )
    print('PARAMETERS: PARAMETER = ("important global arg", 123456)\n'      )
    if __name__ == '__main__':
        with mp.Pool(initializer=initializer_function_pooli, initargs=('important global arg', 123456)) as p:
            res = p.map(work_pooli, [0] * 3)
            resultlt=', '.join(map(str, res))
            print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('POOL REMOTE\n'      )
    print('PARAMETERS: FUNCTION = hello_poolr()\n'      )
    print('PARAMETERS: FUNCTION = square_poolr()\n'      )
    print('PARAMETERS: FUNCTION = divide_poolr()\n'      )
    with Pool() as pool:
        if __name__ == '__main__':
            res = pool.apply(hello_poolr, ('World', ))
            resultlt=res
        print('Message from Lihtops process: [%s]\n' % resultlt     )
        end=time.time()
        print('Execution took: '+str(end-ini)+' seconds\n'      )
        print('\n'      )

        ini=time.time()
        print('POOL REMOTE\n'      )
        if __name__ == '__main__':
            res = pool.map(square_poolr, [1, 2, 3, 4, 5])
            resultlt=', '.join(map(str, res))
            print('Message from Lihtops process: [%s]\n' % resultlt     )
        end=time.time()
        print('Execution took: '+str(end-ini)+' seconds\n'      )
        print('\n'      )

        ini=time.time()
        print('POOL REMOTE\n'      )
        if __name__ == '__main__':
            res = pool.apply_async(square_poolr, (20,))
            st=str(res.ready())  # prints "False"
            print('Message from Lihtops process: execution state [%s]\n' % st     )
            print('Message from Lihtops process: wait till finish\n'      )
            res.wait()
            st=str(res.ready())  # prints "True"
            print('Message from Lihtops process: execution state [%s]\n' % st     )
            resultlt=str(res.get(timeout=5))  # prints "400"
            print('Message from Lihtops process: [%s]\n' % resultlt     )
        end=time.time()
        print('Execution took: '+str(end-ini)+' seconds\n'      )
        print('\n'      )

        ini=time.time()
        print('POOL REMOTE\n'      )
        if __name__ == '__main__':
            res = pool.starmap(divide_poolr, [(1, 2), (2, 3), (3, 4)])
            resultlt=', '.join(map(str, res))
            print('Message from Lihtops process: [%s]\n' % resultlt     )
        end=time.time()
        print('Execution took: '+str(end-ini)+' seconds\n'      )
        print('\n'      )

        ini=time.time()
        print('POOL REMOTE\n'      )
        if __name__ == '__main__':
            res = pool.apply_async(divide_poolr, (1, 0))
            res.wait()
            resultlt=str(res.successful())  # prints "False"
            print('Message from Lihtops process: [Successful: %s]\n' % resultlt     )
            try:
                resultlt=str(res.get()) 
                print('Message from Lihtops process: [%s]\n' % resultlt     )
            except Exception as e:
                resultlt=str(e)
                print('Message from Lihtops process: [%s]\n' % resultlt     )
        end=time.time()
        print('Execution took: '+str(end-ini)+' seconds\n'      )
        print('\n'      )

    print('Message from Lihtops process: %s\n' % 'end of Lithops process'     )


def do_benchmark_simpler():
    print("got request")

    print('Edge client program execution has started\n'      )
    print('\n'      )

    print('Execution of Lithops process\n'      )
    print('\n'      )

    ini=time.time()
    print('HELLO WORLD\n'      )
    with FunctionExecutor() as fexec:
        fut = fexec.call_async(hello, (username, greeting))
        print(fut.result())
        resultlt=str(fut.result())
        print('Message from Lihtops process: %s\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('MULTIPROCESSING\n'      )
    with Pool() as pool:
        print('Message from Lihtops process: %s\n' % 'doubling values of array [1, 2, 3, 4]'     )
        result = pool.map(double, [1, 2, 3, 4])
        print(result)
        resultlt=', '.join(map(str, result))
        print('Message from Lihtops process: [%s]\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('STORAGE LITHOPS\n'      )
    if __name__ == "__main__":
        st = Storage()
        bucket='mybucket'
        fkey='test.txt'
        print('Message from Lihtops process: using bucket: %s\n' % bucket     )
        print('Message from Lihtops process: wrting file on it: %s\n' % fkey     )
        st.put_object(bucket=bucket,
                    key=fkey,
                    body=str('Hello '+username+'!'))

        result = st.get_object(bucket=bucket, key=fkey)
        # print(st.get_object(bucket='mybucket',
        #                     key='test.txt'))
        resultlt=str(result)
        print('Message from Lihtops process: getting content from file: %s\n' % resultlt     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    ini=time.time()
    print('STORAGE CLOUD OS\n'      )
    if __name__ == "__main__":
        filepath = 'bar/foo.txt'
        with oscloud.open(filepath, 'w') as f:
            print('Message from Lihtops process: creating and removing "%s"\n' % filepath     )
            print('Message from Lihtops process: writing "%s" to file\n' % str('Hello '+username+'!')     )
            f.write(str('Hello '+username+'!'))

        dirname = oscloud.path.dirname(filepath)
        print(oscloud.listdir(dirname))
        print('Message from Lihtops process: listing files in directory "%s"\n' % oscloud.listdir(dirname)     )
        print('Message from Lihtops process: deleting "%s"\n' % filepath     )
        result = oscloud.remove(filepath)
        resultlt='success'
        if result == None:
            print('Message from Lihtops process: %s\n' % resultlt     )
        else:
            print('Message from Lihtops process: %s\n' % 'fail'     )
    end=time.time()
    print('Execution took: '+str(end-ini)+' seconds\n'      )
    print('\n'      )

    print('Message from Lihtops process: %s\n' % 'end of Lithops process'     )


#
###
if __name__ == "__main__":
    if sys.argv[1] == "complete":
        do_benchmark_complete()
    elif sys.argv[1] == "simpler":
        do_benchmark_simpler()
    else:
        do_benchmark_simpler()

