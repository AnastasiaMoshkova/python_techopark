import functools
import time


def profile(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        print(func.__name__, "started")
        timee = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, "finished in", str(time.time()-timee))
        return result
    return wrapped

def profile_all(klass):
    for attr_name in ['get_name']:
        method = getattr(klass, attr_name)
        setattr(klass, attr_name, my_decorator(method))
    return klass


@profile
def foo():
    pass


@profile
class Bar():
    def __init__(self):
        pass


@profile_all
class Foo():
    def __init__(self,name):
        self._name=name
    def get_name(self):
        return self._name


foo()
Bar()
Foo("name").get_name()
