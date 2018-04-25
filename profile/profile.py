import functools
import time


def my_decorator(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        print(func.__name__, "started")
        timee = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, "finished in", str(time.time()-timee))
        return result
    return wrapped


@my_decorator
def foo():
    pass


@my_decorator
class Bar():
    def __init__(self):
        pass


foo()
Bar()