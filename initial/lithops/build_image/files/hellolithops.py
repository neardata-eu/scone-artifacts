from lithops import FunctionExecutor

def hello(name):
    return 'Hello {}!'.format(name)

with FunctionExecutor() as fexec:
    fut = fexec.call_async(hello, 'World')
    print(fut.result())

